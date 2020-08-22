package regex;

public abstract class RegExp {

	protected RegExp next = null;
	protected static RegExp last = null;
	
	public boolean matches(String input) {
		return matches(new StringIterator(input));
	}
	
	protected abstract boolean matches(StringIterator stringIterator);
	
}
