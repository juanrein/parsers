package json;
import java.util.ArrayList;

public class JsonObject extends Value {

    private ArrayList<KeyValue> items = new ArrayList<KeyValue>();

    public JsonObject() {

    }

    public void add(JsonString key, Value value) {
        items.add(new KeyValue(key, value));
    }

    public void add(String key, Value value) {
        items.add(new KeyValue(new JsonString(key), value));
    }

    public String toJsonString() {
        if (items.size() == 0) {
            return "{}";
        }
        StringBuilder sb = new StringBuilder();
        sb.append("{\n");
        for (int i=0; i<items.size()-1; i++) {
            sb.append("    " + items.get(i).toJsonString() +  ",\n");
        }
        sb.append("    " + items.get(items.size()-1).toJsonString());
        sb.append("\n}");
        return sb.toString();
    }

    @Override
    public String toString() {
        return toJsonString();
    }
}

