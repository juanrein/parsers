import argparse
import re 
from elements import StartTag, EndTag, SelfClosingTag, TextNode, Prolog, Node

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


def parse_node(elements, start_i, end_i):
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

            children = parse_node(elements, i+1, end_j-1)
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

    if not isValidTagName(tag):
        return None

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
    """
    xml string to list of StartTag, EndTag, SelfClosingTag, TextNode
    Params:
        s: str xml string
    Returns:
        List of elements
    Raises:
        ValueError: if not properly formed xml
    """
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
        
        children = parse_node(tokens, start_i+1, end_i-1)
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
