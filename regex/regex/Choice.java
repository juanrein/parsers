package regex;

import java.util.ArrayList;

public class Choice extends RegExp {

	private ArrayList<RegExp> choices = new ArrayList<RegExp>();
	


	/**
	 * test if one of choices matches 
	 */
	@Override
	protected boolean matches(StringIterator it) {
		for (RegExp choice : choices) {
			it.save();
			if (choice.matches(it)) {
				if (this == RegExp.last) {
					if (it.hasNext()) 
						return false;
					return true;
				}
				if (this.next == null) {
					return true;
				}
				return this.next.matches(it);
			}	
			it.restore();
		}
		it.restore();
		return false;
	}
	
	public void addChoice(RegExp exp) {
		this.choices.add(exp);
	}
	
	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		for (int i=0; i<this.choices.size()-1; i++) {
			sb.append(this.choices.get(i).toString() + "|");
		}
		sb.append(this.choices.get(this.choices.size()-1));
		if (this.next == null)
			return sb.toString();
		return sb.toString() + this.next.toString();
	}

}
