import unittest
from xmlparser import parse_prolog, parse_starttag,parse_selfclosing,parse_endtag,parse_text, isValidTagName
from elements import Prolog, StartTag, EndTag, SelfClosingTag, TextNode
"""
py -m unittest tests.py
"""
class Testit(unittest.TestCase):
    def testParseProlog(self):
        first,i = parse_prolog('<?xml version="1.0" encoding="UTF-8" ?>')
        second = Prolog("1.0", "UTF-8")
        self.assertEqual(first.version, second.version)
        self.assertEqual(first.encoding, second.encoding)
        self.assertEqual(i, 39)

    def testParseProlog2(self):
        first,i = parse_prolog('<?xml   encoding = "UTF-8"?>')
        second = Prolog("1.0", "UTF-8")
        self.assertEqual(first.version, second.version)
        self.assertEqual(first.encoding, second.encoding)
        self.assertEqual(i, 28)

    def testParseStartTag(self):
        first, i = parse_starttag("<element>Text</element>")
        second = StartTag("element", {})
        self.assertEqual(first.tagname, second.tagname)
        self.assertEqual(first.attributes, second.attributes)
        self.assertEqual(i, 9)

    def testParseStartTag2(self):
        first, i = parse_starttag("<element  attribute = 'value'>Text</element>")
        second = StartTag("element", {"attribute": "value"})
        self.assertEqual(first.tagname, second.tagname)
        self.assertEqual(first.attributes, second.attributes)
        self.assertEqual(i, 30)

    def testParseStartTag3(self):
        first = parse_starttag("""<element attribute='value">""")
        second = None
        self.assertEqual(first, second)

    def testParseStartTag4(self):
        first,i = parse_starttag("""<_element attribute="value" attr2="valval2">""")
        second = StartTag("_element", {"attribute": "value", "attr2": "valval2"})
        self.assertEqual(first.tagname, second.tagname)
        self.assertEqual(first.attributes, second.attributes)
        self.assertEqual(i, 44)

    def testParseEndTag(self):
        first,i = parse_endtag("</element>")
        second = EndTag("element")
        self.assertEqual(first.tagname, second.tagname)
        self.assertEqual(i, 10)

    def testParseText(self):
        first, i = parse_text("Text</element>")
        second = TextNode("Text")
        self.assertEqual(first.text, second.text)
        self.assertEqual(i, 4)

    def testIsValidTagName(self):
        self.assertTrue(isValidTagName("element"))
        self.assertTrue(isValidTagName("ele_m-e.nt"))
        self.assertTrue(isValidTagName("_"))
        
        self.assertFalse(isValidTagName("1element"))
        self.assertFalse(isValidTagName(""))
        self.assertFalse(isValidTagName("XML"))

    def testSelfClosing(self):
        first, i = parse_selfclosing("<element attr='value' />Text<start></start>")
        second = SelfClosingTag("element", {"attr": "value"})
        self.assertEqual(first.tagname, second.tagname)
        self.assertEqual(first.attributes, second.attributes)
        self.assertEqual(i, 24)