package regex;

public class Group extends RegExp {

	private RegExp exp;
	
	public Group(RegExp exp) {
		this.exp = exp;
	}
	
	@Override
	protected boolean matches(StringIterator it) {
		it.save();
		if (this.exp.matches(it)) {
			if (this == RegExp.last) {
				if (it.hasNext())
					return false;
				return true;
			}
			if (this.next == null)
				return true;
			return this.next.matches(it);
		}
		it.restore();
		return false;
	}
	
	@Override
	public String toString() {
		if (this.next == null)
			return "(" + this.exp.toString() + ")";
		return "(" + this.exp.toString() + ")" + this.next.toString();
	}

	public void setExp(RegExp groupExp) {
		this.exp = groupExp;
	}


}
