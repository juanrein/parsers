package json;


public class JsonBool extends Value implements Token {
    private boolean value;

    public JsonBool(boolean bool) {
        this.value = bool;
    }

    public boolean getValue() {
        return value;
    }
    public String toJsonString() {
        return value+"";
    }
    

    @Override
    public String toString() {
        return toJsonString();
    }
}