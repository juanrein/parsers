from xmlparser import XMLDocument
from elements import Node

doc = XMLDocument.parseFile("data/test.xml")

def getElementsByTagName(doc, tagname):
    stack = [doc.root]
    elements = []

    while len(stack) > 0:
        e = stack[-1]
        if hasattr(e, "__next__"):
            try:
                c = next(e)
                stack.append(c)
            except StopIteration:
                stack.pop()
                parent = stack.pop()
                if parent.tagname == tagname:
                    elements.append(parent)
        elif isinstance(e, Node) and len(e.childNodes) > 0:
            stack.append(iter(e.childNodes))
        else:
            if hasattr(e, "tagname") and e.tagname == tagname:
                elements.append(e)                
            stack.pop()

    return elements

def traverseF(doc, f):
    """
    Apply function f to each of the element in document
    """
    stack = [doc.root]

    while len(stack) > 0:
        e = stack[-1]
        #is an iterator
        if hasattr(e, "__next__"):
            try:
                c = next(e)
                stack.append(c)
            except StopIteration:
                stack.pop()
                parent = stack.pop()
                f(parent)
        elif isinstance(e, Node) and len(e.childNodes) > 0:
            stack.append(iter(e.childNodes))
        else:
            f(e)            
            stack.pop()

if __name__ == "__main__":
    tags = []    
    def addTag(e):
        if isinstance(e, Node):
            tags.append(e.tagname)
        
    traverseF(doc, addTag)

    print(tags)