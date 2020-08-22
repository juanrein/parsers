package test;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

import regex.RegExp;
import regex.RegExpBuilder;
import regex.RegExpParseException;

class TestRegex {

	private final RegExpBuilder builder = new RegExpBuilder();
	
	@Test
	void testEmptyPattern() {
		RegExp exp = builder.parse("");
		assertTrue(exp.matches(""));
		assertFalse(exp.matches("aabbca"));
	}
	
	@Test
	void testEmptyMatch() {
		RegExp exp = builder.parse("abcd");
		assertFalse(exp.matches(""));
	}
	
	@Test
	void testLiterals() {
		RegExp exp = builder.parse("a");
		assertTrue(exp.matches("a"));
		assertFalse(exp.matches("abcde"));
		assertFalse(exp.matches("b"));
		assertFalse(exp.matches("afgfadg"));
	}
	
	@Test
	void testLiterals2() {
		RegExp exp = builder.parse("abcd");
		assertTrue(exp.matches("abcd"));
		assertFalse(exp.matches("abcde"));
		assertFalse(exp.matches("a"));
		assertFalse(exp.matches("afgfadg"));
	}
	
	@Test
	void testGroup() {
		RegExp exp = builder.parse("(abcd)");
		assertTrue(exp.matches("abcd"));
		assertFalse(exp.matches("ad"));
	}

	@Test
	void testMultiGroup() {
		RegExp exp = builder.parse("(a(bcd))");
		assertTrue(exp.matches("abcd"));
		assertFalse(exp.matches("ad"));
	}
	
	@Test
	void testStar() {
		RegExp exp = builder.parse("a*");
		assertTrue(exp.matches("aaaa"));
		assertTrue(exp.matches("a"));
		assertTrue(exp.matches(""));
		
		assertFalse(exp.matches("aabb"));
	}
	
	@Test
	void testPlus() {
		RegExp exp = builder.parse("a+");
		assertTrue(exp.matches("aaaa"));
		assertTrue(exp.matches("a"));
		
		assertFalse(exp.matches(""));
		assertFalse(exp.matches("aadfad"));
		
	}

	@Test
	void testOptional() {
		RegExp exp = builder.parse("a?");
		assertTrue(exp.matches("a"));
		assertTrue(exp.matches(""));
		
		assertFalse(exp.matches("ff"));
		assertFalse(exp.matches("aa"));
		
	}
	
	@Test
	void testChoice() {
		RegExp exp = builder.parse("a|b|c");
		assertTrue(exp.matches("a"));
		assertTrue(exp.matches("b"));
		assertTrue(exp.matches("c"));
		
		assertFalse(exp.matches("d"));
		assertFalse(exp.matches("aa"));
		
	}
	

	@Test
	void testChoice2() {
		RegExp exp = builder.parse("kissa|koira|kettu");
		assertTrue(exp.matches("kissa"));
		assertTrue(exp.matches("koira"));
		assertTrue(exp.matches("kettu"));
		
		assertFalse(exp.matches("d"));
		assertFalse(exp.matches("aaaaa"));
		assertFalse(exp.matches(""));
		assertFalse(exp.matches("kissaa"));
	}
	
	@Test
	void testDot() {
		RegExp exp = builder.parse("kiss.");
		assertTrue(exp.matches("kissa"));
		assertTrue(exp.matches("kisse"));
		assertTrue(exp.matches("kiss."));
		
		assertFalse(exp.matches(""));
		assertFalse(exp.matches("koira"));
		assertFalse(exp.matches("a"));
		assertFalse(exp.matches("kissaa"));
	}
	
	@Test
	void testAll() {
		RegExp exp = builder.parse("a+b?c*");
		assertTrue(exp.matches("aabcccc"));
		assertTrue(exp.matches("a"));
		assertTrue(exp.matches("aabccccc"));
		
		assertFalse(exp.matches(""));
		assertFalse(exp.matches("abbcd"));
		assertFalse(exp.matches("bc"));
	}
	
	@Test
	void testWildcard() {
		RegExp exp = builder.parse("(abcd)*");
		assertTrue(exp.matches(""));
		assertTrue(exp.matches("abcdabcd"));
		assertTrue(exp.matches("abcd"));
		
		assertFalse(exp.matches("abcdabc"));
		assertFalse(exp.matches("abcdabcda"));
	}
	
	@Test
	void testChain() {
		RegExp exp = builder.parse("(abcd)*aa(bc)+|qwe");
		assertTrue(exp.matches("abcdaabc"));
		assertTrue(exp.matches("aabc"));
		assertTrue(exp.matches("aabcbc"));
		assertTrue(exp.matches("abcdabcdaabc"));
		assertTrue(exp.matches("qwe"));
		
		assertFalse(exp.matches("abcdaabcqwe"));
		assertFalse(exp.matches("abcdaa"));
		assertFalse(exp.matches("1234"));
		assertFalse(exp.matches(""));
		assertFalse(exp.matches("abcda"));
	}
	
	@Test 
	void testParseError() {
		assertThrows(RegExpParseException.class, () -> builder.parse("(()"));
		assertThrows(RegExpParseException.class, () -> builder.parse("())"));
		assertThrows(RegExpParseException.class, () -> builder.parse(")("));
		assertThrows(RegExpParseException.class, () -> builder.parse("()))))(((()))"));
		assertThrows(RegExpParseException.class, () -> builder.parse("abcd(abcd)*ab("));
		
	}
	
}
