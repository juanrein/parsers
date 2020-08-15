import unittest
from xmlparser import parseEndTag, parseStartTag, parseAttributes

"""
py -m unittest tests.py

"""
class Testit(unittest.TestCase):
    def test_parseTag(self):
        self.assertEqual(parseEndTag('</elementti>'), "elementti")
        self.assertEqual(parseStartTag('<elementti attribuutti="arvo" attribuutti2="arvo2">'), 
            ('elementti', {'attribuutti': 'arvo', 'attribuutti2': 'arvo2'}))
        self.assertEqual(parseStartTag('<elementti>'), ("elementti", {}))
        self.assertEqual(parseStartTag('<_eleäämentti.-.>'), ("_eleäämentti.-.", {}))
        self.assertEqual(
            parseStartTag("""<gangster name='George "Shotgun" Ziegler'>"""),
            ("gangster", {"name": 'George "Shotgun" Ziegler'}))
