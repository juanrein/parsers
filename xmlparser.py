import argparse
"""

This line is called the XML prolog: <?xml version="1.0" encoding="UTF-8"?>
The XML prolog is optional. If it exists, it must come first in the document.

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

White-space is Preserved in XML

Element:
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

Atributes:
    XML Attribute Values Must Always be Quoted
    Either single or double quotes can be used.

    If the attribute value itself contains double quotes you can use single quotes, like in this example:
    <gangster name='George "Shotgun" Ziegler'>
    or you can use character entities:
    <gangster name="George &quot;Shotgun&quot; Ziegler">

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

def parseAttributes(s):
    """
    attribuutti="arvo" attribuutti2="arvo2">
    """
    attributes = {}
    i = 0
    while s[i] != ">":
        start_i = i
        while s[i] != "=":
            i += 1
        name = s[start_i:i]
        #pass whitespace
        while s[i] == " ":
            i += 1
        i += 1 #pass '='
        #pass whitespace
        while s[i] == " ":
            i += 1

        if s[i] == "'":
            quoteChar = "'"
        else:
            quoteChar = '"'
        
        #pass quotechar
        i += 1
        start_i = i
        while s[i] != quoteChar:
            i += 1
        value = s[start_i:i]
        #pass quotechar
        i += 1
        #pass whitespace
        while s[i] == " ":
            i += 1

        attributes[name] = value

    return attributes


def parseStartTag(s):
    """
    starttag name and attributes as dictionary
    raises:
        errors if not properly formed
    Returns (tagname, attributes: {name: value})
    """
    if s[0] != "<":
        raise ValueError("missing <")
    if s[-1] != ">":
        raise ValueError("missing >")
        
    attributes = {}

    parts = s.split(" ", maxsplit=1)  
    if len(parts) == 1: #no attributes, > at the end
        tagname = parts[0][1:-1]
    else:
        tagname = parts[0][1:]

        attributes = parseAttributes(parts[1])

    chechIsTagName(tagname)


    return tagname,attributes 


def parseEndTag(s):
    """
    tagname
    """

    if not s.startswith("</"):
        raise ValueError("missing </")
    if s[-1] != ">":
        raise ValueError("missing >")

    chechIsTagName(s[2:-1])

    return s[2:-1]


class Node:
    def __init__(self):
        self.tagname = ""
        self.childNodes = []
        self.attributes = {}
        self.text = ""

    def __str__(self):
        attr = " ".join(map(lambda x: x[0] + '="' + x[1] + '"', self.attributes.items()))
        
        cds =  "".join(map(str, self.childNodes))

        return f"<{self.tagname} {attr}>{self.text}{cds}</{self.tagname}>"

def parseNode(xml):
    """
    Returns:
        (tagname: str, attributes: dict, between_tags: str, after_tag: str)
    """
    s = xml.strip()
    if s[0] != "<":
        raise ValueError("missing <")

    i = 0
    while s[i] != ">":
        i += 1
    i+=1
    tagname, attributes = parseStartTag(s[0:i])

    #start index of endtag
    end_i = s.find("</" + tagname + ">", i)
    #index of > of this tag
    tag_end_i = end_i + len(tagname) + 3
    endtag = parseEndTag(s[end_i:(tag_end_i)])

    between_tags = s[i:end_i]
    after_tags = s[tag_end_i:]

    return (tagname, attributes, between_tags, after_tags)


xml = """
    <elementti attribuutti="arvo" attribuutti2="arvo2">
        <alielementti>Tekstiä</alielementti>
        <alielementti>Tekstiä2</alielementti>
    </elementti>
    """

def main():
    parser = argparse.ArgumentParser("xml parser")
    parser.add_argument("file", help='file to read to xml tree')

    args = parser.parse_args()

    with open(args.file) as f:
        print(f.read)


