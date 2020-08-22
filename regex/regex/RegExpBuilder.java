package regex;

import java.util.ArrayList;
import java.util.regex.Pattern;

public class RegExpBuilder {

	
	/**
	 * joins expression into one, clears arraylist, sets last if top level
	 * @param rs 
	 * @return expression 
	 */
	private RegExp join(ArrayList<RegExp> rs, boolean isTopLevel) {
		if (rs.size() == 1) {
			RegExp exp = rs.remove(0);
			if (isTopLevel)
				RegExp.last = exp;
			return exp;
		}
		RegExp temp = rs.get(0);
		RegExp root = temp;
		
		for (int i=1; i<rs.size(); i++) {
			temp.next = rs.get(i);
			temp = temp.next;
		}
		if (isTopLevel)
			RegExp.last = temp;
		rs.clear();
		return root;
	}
	
	
	/**
	 * parses given input into a regex pattern
	 * @param input pattern string to parse
	 * @param isTopLevel whether this is a top level expression or part of other expression
	 * @return regex object
	 */
	private RegExp parse(String input, boolean isTopLevel) {
		if (input.length() == 0)
			return null;
		int layers = 0;
		
		ArrayList<RegExp> rs = new ArrayList<RegExp>();
		Choice choice = null;
		StringBuilder current = new StringBuilder();
		
		//parse one layer
		for (int i=0; i<input.length(); i++) {
			char c = input.charAt(i);
			switch (c) {
			case '*':
				if (layers > 0) {//inside expression
					current.append(c);
				} else { //top level
					RegExp exp = rs.remove(rs.size()-1);
					Star star = new Star(exp);
					rs.add(star);					
				}
				break;
			case '+':
				if (layers > 0) {//inside expression
					current.append(c);
				} else { //top level
					RegExp exp = rs.remove(rs.size()-1);
					Plus plus = new Plus(exp);
					rs.add(plus);					
				}
				break;
			case '?':
				if (layers > 0) {//inside expression
					current.append(c);
				} else { //top level
					RegExp exp = rs.remove(rs.size()-1);
					Optional optional = new Optional(exp);
					rs.add(optional);					
				}
				break;
			case '|':
				if (layers > 0) { //inside expression
					current.append(c);
				} else { //top level
					if (choice == null) {
						choice = new Choice();
					} 
					RegExp exp = join(rs,isTopLevel);
					choice.addChoice(exp);
				}
				break;
			case '(':		
				if (layers > 0) { //inside expression
					current.append(c);
				} else { //top level
					current = new StringBuilder();
				}
				layers++;

				break;
			case ')':
				layers--;
				if (layers < 0) { //missing (
					throw new RegExpParseException("missing (");
				}
				if (layers > 0) { //inside expression
					current.append(c);
				} else { //top level
					RegExp e = parse(current.toString(), false);
					Group g = new Group(e);
					rs.add(g);
					current = new StringBuilder();
				}

				break;
			default:
				if (layers > 0) { //inside expression
					current.append(c);
				} else { //top level
					rs.add(new Literal(c));		
				}
			
				break;
			}
		}
		if (layers != 0)
			throw new RegExpParseException("missing )");
		
		if (choice != null) {
			RegExp exp = join(rs, isTopLevel);
			choice.addChoice(exp);
			rs.add(choice);
		}
		
		RegExp root = join(rs,isTopLevel);
		
		return root;
	}
	
	/**
	 * Parses string into a regular expression
	 * @param input
	 * @return
	 */
	public RegExp parse(String input) {
		if (input.length() == 0)
			return new Empty();
		return parse(input, true);
	}

}
