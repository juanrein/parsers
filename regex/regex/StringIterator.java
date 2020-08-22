package regex;

import java.util.Stack;

public class StringIterator {
	private String string;
	private int index = 0;
	private Stack<Integer> states = new Stack<Integer>();
	
	public StringIterator(String string) {
		this.string = string;
		states.push(0);
	}

	private StringIterator(String string, int index) {
		this.string = string;
		this.index = index;
	}
	
	public char next() {
		char c = string.charAt(index);
		index++;
		return c;
	}

	public boolean hasNext() {
		return index < string.length();
	}
	
	/**
	 * get the current character without removing it
	 * @return char at current position of iterator
	 */
	public char peek() {
		return string.charAt(index);
	}
	
	
	public StringIterator clone() {
		return new StringIterator(string, index);
	}
	
	/**
	 * saves the current location of the iterator to be used again
	 */
	public void save() {
		states.push(this.index);
	}
	
	/**
	 * restores iterator back to location it was when it was last saved or start
	 * if not saved before
	 */
	public void restore() {
		this.index = states.pop();
	}

}
