package json;
import java.util.ArrayList;
import java.util.ListIterator;

public class Tokenizer {

    private String fileString;
    private int index = 0;
    
    public Tokenizer(String fileString) {
        this.fileString = fileString;
    }


    public boolean hasNext() {
        return index < this.fileString.length();
            
    }


    public ArrayList<Token> tokenize() {
        ArrayList<Token> tokens = new ArrayList<Token>();
        
        while (hasNext()) {
            if (Character.isDigit(fileString.charAt(index))) {
                JsonNumber num = new JsonNumber();
                this.index = num.parse(fileString, index);
                tokens.add(num);
            }

            else if (fileString.startsWith("null", index)) {
                tokens.add(new JsonNull());
                index += 3;
            }

            else if (fileString.startsWith("true", index)) {
                tokens.add(new JsonBool(true));
                index += 3;
            }

            else if (fileString.startsWith("false", index)) {
                tokens.add(new JsonBool(false));
                index += 4;
            }
            else {
                switch (fileString.charAt(index)) {
                    case '\"':
                        index++;
                        StringBuilder sb = new StringBuilder();
                        while (hasNext() && fileString.charAt(index) != '\"') {
                            sb.append(fileString.charAt(index));
                            index++;
                        }
                        tokens.add(new JsonString(sb.toString()));
                        break;
                    case ':':
                        tokens.add(new Colon());
                        break;
                    case ',':
                        tokens.add(new Comma());
                        break;
                    case '{':
                        tokens.add(new OpenCurlyBracket());
                        break;
                    case '}':
                        tokens.add(new CloseCurlyBracket());
                        break;
                    case '[':
                        tokens.add(new OpenSquareBracket());
                        break;
                    case ']':
                        tokens.add(new CloseSquareBracket());
                        break;        
                }
            }
            index++;
        }
        return tokens;
    }

}