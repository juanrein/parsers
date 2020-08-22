package regex;


public class Star extends RegExp {

	private RegExp exp;
	
	public Star(RegExp exp) {
		this.exp = exp;
	}
	
	
	/**
	 * check if matches 0 or more times
	 * if doesn't match leaves stringIterator unaffected
	 * 
	 */
	@Override
	protected boolean matches(StringIterator it) {
		it.save();
		//matches 0 times
		if (!this.exp.matches(it)) {
			it.restore();
			if (this == RegExp.last) {
				if (it.hasNext())
					return false;
				return true;
			}
			if (this.next == null) { //inside other expression
				return true;
			}
			return this.next.matches(it);
		}
		it.save();
		//matches atleast 1 time
		while (this.exp.matches(it)) {it.save();}
		it.restore();
		
		if (this.next == null) {
			if (this == RegExp.last) {
				if (it.hasNext())
					return false;
				return true;
			}
			//inside wrapper
			return true;
		}
		
		return this.next.matches(it);			
	}
	

	@Override
	public String toString() {
		if (this.next == null)
			return this.exp.toString() + "* ";
		return this.exp.toString() + "*" + this.next.toString();
	}

}
