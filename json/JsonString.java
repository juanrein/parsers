package json;


public class JsonString extends Value implements Token {
    private String value;

    public JsonString(String s) {
        this.value = s;
    }

    public String getValue() {
        return value;
    }
    
    public String toJsonString() {
        return "\"" + value + "\"";
    }

    @Override
    public String toString() {
        return toJsonString();
    }
}