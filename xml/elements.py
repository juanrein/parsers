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