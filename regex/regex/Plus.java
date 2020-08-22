package regex;

public class Plus extends RegExp {
	private RegExp exp;
	
	public Plus(RegExp exp) {
		this.exp = exp;
	}
	
	
	//check if matches one or more times
	@Override
	protected boolean matches(StringIterator it) {
		it.save();
		if (!this.exp.matches(it)) {
			it.restore();
			return false;
		}
		it.save();
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
			return this.exp.toString() + "+";
		return this.exp.toString() + "+" + this.next.toString();
	}

}
