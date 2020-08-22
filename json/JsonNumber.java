package json;


public class JsonNumber extends Value implements Token {
    private double value;

    public JsonNumber() {
        this(0.0);
    }

    public JsonNumber(double value) {
        this.value = value;
    }

    public double getValue() {
        return value;
    }

    public void setValue(double value) {
        this.value = value;
    }

    public String toJsonString() {
        return value + "";
    }


    @Override
    public String toString() {
        return toJsonString();
    }

    private boolean isNumberChar(char c) {
        return Character.isDigit(c) || c == '.' || c == '+' || c == '-' || c == 'e' || c == 'E';
    }

    public int parse(String s, int index) {
        StringBuilder number = new StringBuilder();
        //TODO: move and make better .2.23.32.2....1 shouldn't be valid
        int i = index;
        while (i < s.length() && isNumberChar(s.charAt(i)))
        {
            number.append(s.charAt(i));
            i++;
        }
        double val = Double.parseDouble(number.toString());
        this.setValue(val);
        return i-1;
    }
}