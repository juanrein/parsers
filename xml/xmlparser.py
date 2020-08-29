import argparse
import re 


"""
TODO:
entity references:
    &lt;	<	less than
    &gt;	>	greater than
    &amp;	&	ampersand 
    &apos;	'	apostrophe
    &quot;	"	quotation mark

comment:
    <!-- This is a comment -->

    Two dashes in the middle of a comment are not allowed:
    <!-- This is an invalid -- comment -->
"""

class SelfClosingTag:
    """
    <element />
    self closing tag
    Empty elements can have attributes.
    """
    def __init__(self, tagname = None, attributes = None):
        if attributes is None:
            self.attributes = {}
        else:
            self.attributes = attributes
    
        self.tagname = tagname


class StartTag:
    def __init__(self, tagname = None, attributes = None):
        if attributes is None:
            self.attributes = {}
        else:
            self.attributes = attributes
        self.tagname = tagname


class EndTag:
    def __init__(self, tagname = None):
        self.tagname = tagname
    

class Prolog:
    """
    This line is called the XML prolog: <?xml version="1.0" encoding="UTF-8"?>
    The XML prolog is optional. If it exists, it must come first in the document.
    """
    def __init__(self, version="1.0", encoding="UTF-8"):
        if version is None:
            self.version = "1.0"
        else:
            self.version = version
        if encoding is None:
            self.encoding = "UTF-8"
        else:
            self.encoding = encoding

    def __str__(self):
        return f'<?xml version="{self.version}" encoding="{self.encoding}"?>'



class TextNode:
    def __init__(self, text = None):
        self.text = text

    def __str__(self):
        return self.text


class Node:
    """
    XML documents must contain one root element that is the parent of all other elements

    Element names must start with a letter or underscore
    Element names cannot start with the letters xml (or XML, or Xml, etc)
    Element names can contain letters, digits, hyphens, underscores, and periods
    Element names cannot contain spaces

    All XML Elements Must Have a Closing Tag

    XML tags are case sensitive. The tag <Letter> is different from the tag <letter>.
    Opening and closing tags must be written with the same case

    An element with no content is said to be empty.
    <element></element>
    You can also use a so called self-closing tag:
    <element />

    element can have text content and child nodes
    """
    def __init__(self, selfClosing = False):
        self.selfClosing = selfClosing
        self.tagname = ""
        self.childNodes = []
        self.attributes = {}

    def __str__(self):
        attr = " ".join(map(lambda x: x[0] + '="' + x[1] + '"', self.attributes.items()))
        
        cds =  "".join(map(str, self.childNodes))

        if self.selfClosing:
            if len(attr) > 0:
                return f"<{self.tagname} {attr} />"
            return f"<{self.tagname} />"
        else:
            if len(attr) > 0:
                return f"<{self.tagname} {attr}>{cds}</{self.tagname}>"
            return f"<{self.tagname}>{cds}</{self.tagname}>"

    @staticmethod
    def parse(elements, start_i, end_i):
        """
            start_i    end_i
        <tag>................</tag>
        """
        nodes = []

        i = start_i
        while i <= end_i:
            if isinstance(elements[i], TextNode):
                nodes.append(elements[i])
                i += 1
            elif isinstance(elements[i], StartTag):
                end_j = findEnd(elements, i)
                n = Node()
                n.tagname = elements[i].tagname
                n.attributes = elements[i].attributes

                children = Node.parse(elements, i+1, end_j-1)
                n.childNodes = children

                nodes.append(n)

                i = end_j+1
            elif isinstance(elements[i], SelfClosingTag):
                n = Node(True)
                n.tagname = elements[i].tagname
                n.attributes = elements[i].attributes
                nodes.append(n)
                i += 1
            elif isinstance(elements[i], EndTag):
                i += 1
            else:
                raise ValueError("unknown element", elements[i])

        return nodes

def isValidTagName(s):
    """
    must start with a letter or underscore
    cannot start with the letters xml (or XML, or Xml, etc)
    can contain letters, digits, hyphens, underscores, and periods
    cannot contain spaces
    """
    if s.lower().startswith("xml"):
        return False
    return re.match("[^\W\d][\w\-_.]*", s)


def parse_starttag(s, selfClosing = False):
    """
    StartTag from string like <element a="b" c='d'>
    or <element a="b" c='d' /> 
    Params:
        s: str has to match from the beginning of the string
        selfClosing: bool should the ending be > or />
    Returns:
        None if not a starttag
        (StartTag,i)
            i: int end of the starttag substring + 1 
    """
    identifier_pattern = "[^\W\d][\w\-_.]*"
    attr_pattern = f"""({identifier_pattern})\s*=\s*"([^"]*)"|({identifier_pattern})\s*=\s*'([^']*)'"""
    attrs_pattern = f"""(?P<attr>(\s+({attr_pattern}))*)"""
    if selfClosing:
        ending_pattern = "/>"
    else:
        ending_pattern = ">"
    tag_pattern = f"""<(?P<tag>{identifier_pattern})\s*{attrs_pattern}\s*(?P<end>{ending_pattern})"""
    m = re.match(tag_pattern, s)
    if not m:
        return None

    tag = m.group("tag")
    if not isValidTagName(tag):
        return None

    attr_group = m.group("attr")
    attrs = re.findall(attr_pattern, attr_group)
    
    attributes = {}
    for attr in attrs:
        #4-tuple either "", "", key, value or key, value, "", ""
        if len(attr[0]) > 0:
            key = attr[0]
            value = attr[1]
        else:
            key = attr[2]
            value = attr[3]
        attributes[key] = value

    if selfClosing:
        return SelfClosingTag(tag, attributes), m.end("end")
    return StartTag(tag, attributes), m.end("end")

def parse_selfclosing(s):
    return parse_starttag(s, True)


def parse_endtag(s):
    endtag = "</(?P<tag>[^\W\d][\w\-_.]*)>"
    m = re.match(endtag, s)
    if not m:
        return None
    tag = m.group("tag")

    """ if not isValidTagName(tag):
        return None """

    endtag = EndTag(tag)
    return endtag, m.end()

def parse_text(s):
    text = "([^<]+)(<)"
    m = re.match(text, s, flags=re.DOTALL)
    if not m:
        return None
    t = m.group(1)
    
    return TextNode(t), m.end()-1


def parse_prolog(s):
    identifier_pattern = "[^\W\d][\w\-_.]*"
    attr_pattern = f"""({identifier_pattern})\s*=\s*"([^"]*)"|({identifier_pattern})\s*=\s*'([^']*)'"""
    attrs_pattern = f"""(?P<attr>(\s+({attr_pattern}))*)"""

    prolog = f'<\?xml\s*{attrs_pattern}\s*(?P<end>\?>)'
    m = re.match(prolog, s)
    if not m:
        return None
    attr = m.group("attr")
    attrs = re.findall(attr_pattern, attr)

    attributes = {}
    for attr in attrs:
        #4-tuple either "", "", key, value or key, value, "", ""
        if len(attr[0]) > 0:
            key = attr[0]
            value = attr[1]
        else:
            key = attr[2]
            value = attr[3]
        attributes[key] = value
    version = attributes.get("version")
    encoding = attributes.get("encoding")

    return Prolog(version, encoding), m.end("end")
    
def parse_fail(s):
    raise ValueError("unknown token at: " + s)

def tokenize(s):
    tokens = []
    i = 0
    fs = [parse_prolog, parse_starttag, parse_selfclosing, parse_endtag, parse_text, parse_fail]
    while i < len(s):
        for f in fs:
            t = f(s[i:])
            if t:
                e, end_i = t
                i += end_i
                tokens.append(e)
                break

    return tokens


def findEnd(elements, start_i):
    """
    index of endtag for elements[start_i]
    """
    end_i = start_i + 1
    while end_i < len(elements):
        if isinstance(elements[end_i], EndTag) and elements[end_i].tagname == elements[start_i].tagname:
            break
        end_i += 1

    if end_i >= len(elements):
        raise ValueError("missing endtag")

    return end_i

class XMLDocument:
    def __init__(self, root, prolog = None):
        self.root = root
        self.prolog = prolog

    def __str__(self):
        if self.prolog:
            return f"{self.prolog}\n{self.root}"
        return str(self.root)

    @staticmethod
    def parse(xml):
        tokens = tokenize(xml)
                
        #skip anything before root node
        start_i = 0
        while start_i < len(tokens) and not isinstance(tokens[start_i], StartTag):
            start_i += 1

        end_i = findEnd(tokens, start_i)

        root = Node()
        root.tagname = tokens[start_i].tagname
        root.attributes = tokens[start_i].attributes
        
        children = Node.parse(tokens, start_i+1, end_i-1)
        root.childNodes = children

        doc = XMLDocument(root)
        if isinstance(tokens[0], Prolog):
            doc.prolog = tokens[0]
        return doc


    @staticmethod
    def parseFile(file):
        doc = None
        with open(file) as f:
            data = f.read()
            doc = XMLDocument.parse(data)
        return doc


def main():
    parser = argparse.ArgumentParser("xml parser")
    parser.add_argument("file", help='file to read to xml tree')

    args = parser.parse_args()

    print(XMLDocument.parseFile(args.file))


if __name__ == "__main__":
    main()
