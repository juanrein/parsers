package json;

public class KeyValue extends Value {
    private JsonString key;
    private Value value;
    public KeyValue(JsonString key, Value value) {   
        this.key = key; 
        this.value = value;
    }
    public String toJsonString() {
        return key.toJsonString() + ":"+ value.toJsonString();
    }
    
}