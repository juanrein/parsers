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

class Node:
    def __init__(self):
        self.tagname = ""
        self.childNodes = []
        self.attributes = {}
        self.text = ""

    def __str__(self):
        attr = " ".join(map(lambda x: x[0] + '="' + x[1] + '"', self.attributes.items()))
        
        cds =  "".join(map(str, self.childNodes))

        return f"<{self.tagname}{attr}>{self.text}{cds}</{self.tagname}>"

    @classmethod
    def parseNode(cls, s):
        node = Node()
        node.tagname = "elementti"
        node.attributes = {"attribuutti": "arvo", "attribuutti2": "arvo2"}
        cn1 = Node()
        cn1.tagname = "alielementti"
        cn1.text = "Tekstiä"
        cn2 = Node()
        cn2.tagname = "alielementti"
        cn2.text = "Tekstiä2"

        node.childNodes = [cn1, cn2]

        return node

print(Node.parseNode("""
    <elementti atribuutti="arvo" attribuutti2="arvo2">
        <alielementti>Tekstiä</alielementti>
        <alielementti>Tekstiä2</alielementti>
    </elementti>
"""))

def main():
    parser = argparse.ArgumentParser("xml parser")
    parser.add_argument("file", help='file to read to xml tree')

    args = parser.parse_args()

    with open(args.file) as f:
        print(f.read)


