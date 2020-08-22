package regex;


public class Literal extends RegExp {

	char c;
	public Literal(char c) {
		this.c = c;
	}

	/**
	 * test if char matches if doesn't match stringIterator doesn't change
	 */
	@Override
	protected boolean matches(StringIterator iterator) {
		if (!iterator.hasNext())
			return false;
		
		if (iterator.peek() != c && c != '.')
			return false;
		
		iterator.next();

		if (this.next == null) {
			if (this == RegExp.last) {
				if (iterator.hasNext())
					return false;
				return true;
			}
			//inside wrapper
			return true;
		}
		
		return this.next.matches(iterator);			
	}

	@Override
	public String toString() {
		if (this.next == null)
			return c+"";
		return c +this.next.toString();
	}
}
