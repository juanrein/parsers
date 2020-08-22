package json;
import java.util.ArrayList;

public class JsonArray extends Value {
    private ArrayList<Value> values = new ArrayList<Value>();

    public JsonArray() {

    }

    public ArrayList<Value> getValue() {
        return values;
    }

    public void add(Value value) {
        values.add(value);
    }

    public String toJsonString() {
        if (values.size() == 0)
            return "[]";
        StringBuilder sb = new StringBuilder();
        
        sb.append("[");
        for (int i=0; i<values.size()-1; i++) {
            sb.append(values.get(i).toJsonString() + ",");
        }
        sb.append(values.get(values.size()-1).toJsonString());
        sb.append("]");
        return sb.toString();
    }

    @Override
    public String toString() {
        return toJsonString();
    }

}