import unittest
from xmlparser import SelfClosingTag, StartTag

"""
py -m unittest tests.py

"""
class Testit(unittest.TestCase):
    def test_parseSelfClosingTag(self):
        first,i = SelfClosingTag.parse("<element /><start>Hello</start", 0)
        second = SelfClosingTag("element", {})
        self.assertEqual(first.tagname, second.tagname)
        self.assertEqual(first.attributes, second.attributes)
        self.assertEqual(i, 11)

    def test_parseSelfClosingTagNotStart(self):
        first,i = SelfClosingTag.parse("<start>Hello<element /></start", 12)
        second = SelfClosingTag("element", {})
        self.assertEqual(first.tagname, second.tagname)
        self.assertEqual(first.attributes, second.attributes)
        self.assertEqual(i, 23)

    def test_parseSelfClosingTagAttr(self):
        first,i = SelfClosingTag.parse("""<element attr="value" />""", 0)
        second = SelfClosingTag("element", {"attr": "value"})
        self.assertEqual(first.tagname, second.tagname)
        self.assertEqual(first.attributes, second.attributes)
        self.assertEqual(i, 24)

    def test_parseSelfClosingTagMultAttr(self):
        first,i = SelfClosingTag.parse("""<element attr="value" attr2="value2" />""", 0)
        second = SelfClosingTag("element", {"attr": "value", "attr2": "value2"})
        self.assertEqual(first.tagname, second.tagname)
        self.assertEqual(first.attributes, second.attributes)
        self.assertEqual(i, 39)

    def test_parseSelfClosingTagSingleQuote(self):
        first,i = SelfClosingTag.parse("""<element attr='value' />""", 0)
        second = SelfClosingTag("element", {"attr": "value"})
        self.assertEqual(first.tagname, second.tagname)
        self.assertEqual(first.attributes, second.attributes)
        self.assertEqual(i, 24)

    def test_parseSelfClosingTagDoubleQuoteInMiddle(self):
        first,i = SelfClosingTag.parse("""<element attr='val"ue' />""", 0)
        second = SelfClosingTag("element", {"attr": 'val"ue'})
        self.assertEqual(first.tagname, second.tagname)
        self.assertEqual(first.attributes, second.attributes)
        self.assertEqual(i, 25)


    def testParseStartTag(self):
        first,i = StartTag.parse("""<element></element>""", 0)
        second = StartTag("element", {})
        self.assertEqual(first.tagname, second.tagname)
        self.assertEqual(first.attributes, second.attributes)
        self.assertEqual(i, 9)
