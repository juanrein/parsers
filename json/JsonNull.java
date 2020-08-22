package json;

public class JsonNull extends Value implements Token {
    
    public JsonNull() {

    }

    public String getValue() {
        return null;
    }

    public String toJsonString() {
        return "null";
    }


    @Override
    public String toString() {
        return toJsonString();
    }
}