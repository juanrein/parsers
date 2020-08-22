package json;
import java.util.ArrayList;
import java.util.Stack;
import java.util.ListIterator;

/*
JavaScript Object Notation
data interchange format 
*/
public class Parser {

    public Parser() {

    }   

    //TODO: validate correct parentheses
    public Value parse(ArrayList<Token> tokens) {
        if (tokens.size() == 0)
            return new JsonNull();
        Token token = tokens.get(0);

        if (token instanceof JsonNumber) {
            JsonNumber num = (JsonNumber) token;
            return num;
        }
        else if (token instanceof JsonString) {
            JsonString s = (JsonString) token;
            return s;
        }
        else if (token instanceof JsonNull) {
            JsonNull n = (JsonNull) token;
            return n;
        }
        else if (token instanceof JsonBool) {
            JsonBool bool = (JsonBool) token;
            return bool;
        }
        else if (token instanceof OpenCurlyBracket) {
            JsonObject object = new JsonObject();
            int index = 1;
            ArrayList<Token> key = new ArrayList<Token>();
            ArrayList<Token> value = new ArrayList<Token>();
            boolean parseKey = true;
            Stack<Token> stack = new Stack<Token>();
            while (index < tokens.size()) {
                if (tokens.get(index) instanceof CloseCurlyBracket && stack.empty()) {
                    object.add((JsonString)parse(key), parse(value) );
                    return object;
                }
                if (tokens.get(index) instanceof Comma && stack.empty()) {
                    object.add((JsonString)parse(key), parse(value));
                    key.clear();
                    value.clear();
                    index++;
                    parseKey = true;
                }
                if (tokens.get(index) instanceof Colon && stack.empty()) {
                    parseKey = false;
                    index++;
                }
                else {
                    if (parseKey)
                        key.add(tokens.get(index));
                    else { 
                        if (tokens.get(index) instanceof OpenCurlyBracket) {
                            stack.push(tokens.get(index));
                        }
                        else if (tokens.get(index) instanceof CloseCurlyBracket) {
                            stack.pop();
                        }
                        else if (tokens.get(index) instanceof OpenSquareBracket) {
                            stack.push(tokens.get(index));
                        }
                        else if (tokens.get(index) instanceof CloseSquareBracket) {
                            stack.pop();
                        }
                        value.add(tokens.get(index));
                    }
                    index++;
                }
            }
            return object;
        }
        else if (token instanceof OpenSquareBracket) {
            JsonArray array = new JsonArray();
            int index = 1;
            Stack<Token> stack = new Stack<Token>();
            ArrayList<Token> value = new ArrayList<Token>();
            while (index < tokens.size()) {
                if (tokens.get(index) instanceof CloseSquareBracket && stack.empty()) {
                    array.add(parse(value));
                    return array;
                }
                if (tokens.get(index) instanceof Comma && stack.empty()) {
                    array.add(parse(value));
                    value.clear();
                    index++;
                }
                else {
                    if (tokens.get(index) instanceof OpenCurlyBracket) {
                        stack.push(tokens.get(index));
                    }
                    else if (tokens.get(index) instanceof CloseCurlyBracket) {
                        stack.pop();
                    }
                    else if (tokens.get(index) instanceof OpenSquareBracket) {
                        stack.push(tokens.get(index));
                    }
                    else if (tokens.get(index) instanceof CloseSquareBracket) {
                        stack.pop();
                    }
                    value.add(tokens.get(index));
                    index++;
                }
            }
            return array;
        }
        throw new IllegalArgumentException("problem parsing "+ token);
    }

}