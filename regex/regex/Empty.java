package regex;

public class Empty extends RegExp {

	@Override
	protected boolean matches(StringIterator stringIterator) {
		if (stringIterator.hasNext())
			return false;
		return true;
	}

}
