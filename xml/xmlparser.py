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


def chechIsTagName(s):
    """
    must start with a letter or underscore
    cannot start with the letters xml (or XML, or Xml, etc)
    can contain letters, digits, hyphens, underscores, and periods
    cannot contain spaces
    """
    if len(s) == 0:
        raise ValueError("Empty tagname " + s)

    if not (s[0].isalpha() or s[0] == "_"):
        raise ValueError("Tagname must start with a letter or underscore " + s)

    if len(s) >= 3 and s[0:3].lower() == "xml":
        raise ValueError("Tagname cannot start with xml " + s)

    for i in range(1, len(s)):
        if not(s[i].isalpha() or s[i].isdigit() or s[i] == "-" or s[i] == "_" or s[i] == "."):
            raise ValueError("Tagname can only contain letters, digits, hyphens, underscores and periods " + s)

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

    @staticmethod
    def parse(s, start_i):
        """
        <element />
        <element attr="value" />
        Params:
            s string to search
            start_i index to start
        raises:
            errors if not properly formed
        Returns (SelfClosingTag, end_index + 1)
        """
        if s[start_i] != "<":
            raise ValueError("missing <")

        tag = SelfClosingTag()

        stack = []
        attr = ""
        for i in range(start_i+1, len(s)):
            if s[i] + s[i+1] == "/>":
                chechIsTagName(tag.tagname)
                return tag, i+2
            if s[i] == ">":
                raise ValueError("missing />")
            elif s[i] == "=":
                attr = "".join(stack)
                stack = []
            elif s[i] == " ":
                if not tag.tagname:
                    tag.tagname = "".join(stack)
                    stack = []
            elif s[i] == "'":
                if "'" in stack:
                    val = "".join(stack[1:])
                    tag.attributes[attr] = val
                    stack = []
                else:
                    stack.append(s[i])                    
            elif s[i] == '"':
                if '"' in stack:
                    val = "".join(stack[1:])
                    tag.attributes[attr] = val
                    stack = []
                else:
                    stack.append(s[i])
            else:
                stack.append(s[i])          

        if i+1 >= len(s):
            raise ValueError("missing />")



class StartTag:
    def __init__(self, tagname = None, attributes = None):
        if attributes is None:
            self.attributes = {}
        else:
            self.attributes = attributes
        self.tagname = tagname

    @staticmethod
    def parseAttributes(s, start_iter_i):
        """
        attribuutti="arvo" attribuutti2="arvo2">
        XML Attribute Values Must Always be Quoted
        Either single or double quotes can be used.

        If the attribute value itself contains double quotes you can use single quotes, like in this example:
        <gangster name='George "Shotgun" Ziegler'>
        """
        attributes = {}
        i = start_iter_i
        while s[i] != ">":
            start_i = i
            while i < len(s) and s[i] != "=":
                i += 1
            name = s[start_i:i]
            #pass whitespace
            while i < len(s) and s[i] == " ":
                i += 1
            i += 1 #pass '='
            #pass whitespace
            while i < len(s) and s[i] == " ":
                i += 1

            if s[i] == "'":
                quoteChar = "'"
            else:
                quoteChar = '"'
            
            #pass quotechar
            i += 1
            start_i = i
            while i < len(s) and s[i] != quoteChar:
                i += 1
            value = s[start_i:i]
            #pass quotechar
            i += 1
            #pass whitespace
            while i < len(s) and s[i] == " ":
                i += 1

            attributes[name] = value

        return attributes, i + 1

    @staticmethod
    def parse(s, start_i):
        """
        Params:
            s string to search
            start_i index to start
        raises:
            errors if not properly formed starttag
        Returns (StartTag, end_index + 1)
        """
        if s[start_i] != "<":
            raise ValueError("missing <")

        i = start_i + 1
        while i < len(s) and s[i] not in [" ", ">"]:
            i += 1

        tag = StartTag()

        tag.tagname = s[start_i+1:i]

        if i >= len(s):
            raise ValueError("missing >")
        #has attributes
        if s[i] == " ":
            attributes, i = StartTag.parseAttributes(s, i+1)
            tag.attributes = attributes

            chechIsTagName(tag.tagname)
            return tag, i

        chechIsTagName(tag.tagname)
        return tag, i+1

class EndTag:
    def __init__(self, tagname = None):
        self.tagname = tagname
    
    @staticmethod
    def parse(s, start_i):
        """
        tagname
        """
        if not s[start_i:].startswith("</"):
            raise ValueError("missing </")

        i = start_i
        while i < len(s) and s[i] != ">":
            i += 1
            
        if i >= len(s):
            raise ValueError("missing >")

        tag = EndTag()
        tag.tagname = s[start_i+2:i]

        chechIsTagName(tag.tagname)

        return tag, i+1

def parseKV(s, start_i, end_i, k):
    """
    Parse value from string like
    key="value"
    Params:
        s: string from to search
        start_i: index to start the search
        end_i: index to stop the search
        k: the key to search
    Returns:
        value
    """
    i = s.find(k, start_i, end_i)
    if i == -1:
        raise ValueError(k + " not found")

    i += len(k) + 1
    if s[i] == '"':
        seperator = '"'
    elif s[i] == "'":
        seperator = "'"
    else:
        raise ValueError("missing '")  
    j = i+1
    while j < len(s) and s[j] != seperator:
        j += 1
    return s[i+1:j]

class Prolog:
    """
    This line is called the XML prolog: <?xml version="1.0" encoding="UTF-8"?>
    The XML prolog is optional. If it exists, it must come first in the document.
    """
    def __init__(self, version="1.0", encoding="UTF-8"):
        self.version = version
        self.encoding = encoding

    def __str__(self):
        return f'<?xml version="{self.version}" encoding="{self.encoding}"?>'

    @staticmethod
    def parse(s, start_i):
        """
        012345
        <?xml version="1.0" encoding="UTF-8"?>
        """
        if not s[start_i:].startswith("<?xml"):
            raise ValueError("missing <?xml")
        
        end_i = s.find("?>", start_i+5)
        if end_i == -1:
            raise ValueError("missing ?>")

        prolog = Prolog()
        try:
            prolog.version = parseKV(s, start_i, end_i, "version")
        except:
            pass
        try:
            prolog.encoding = parseKV(s, start_i, end_i, "encoding")
        except:
            pass
        return prolog, end_i+2


class TextNode:
    def __init__(self, text = None):
        self.text = text

    def __str__(self):
        return self.text
        
    @staticmethod
    def parse(s, start_i):
        i = start_i
        while i < len(s) and s[i] != "<":
            i += 1

        return TextNode(s[start_i:i]), i



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


def tokenize(xml, start_i, elements):
    """
    Parses xml string to starttags, endtags and text nodes, prologs
    """
    if start_i >= len(xml):
        return

    fs = [Prolog.parse, SelfClosingTag.parse, StartTag.parse, EndTag.parse, TextNode.parse]
    for f in fs:
        try:
            e, i = f(xml, start_i)
            elements.append(e)
            tokenize(xml, i, elements)
            return
        except:
            pass
    
    raise ValueError("can't parse ", xml)



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
        elements = []
        tokenize(xml, 0, elements)
                
        #skip anything before root node
        start_i = 0
        while start_i < len(elements) and not isinstance(elements[start_i], StartTag):
            start_i += 1

        end_i = findEnd(elements, start_i)

        root = Node()
        root.tagname = elements[start_i].tagname
        root.attributes = elements[start_i].attributes
        
        children = Node.parse(elements, start_i+1, end_i-1)
        root.childNodes = children

        doc = XMLDocument(root)
        if isinstance(elements[0], Prolog):
            doc.prolog = elements[0]
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
