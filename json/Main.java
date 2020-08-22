package json;

import java.util.ArrayList;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Main {
    public static String readFile(String filename) {
        StringBuilder fileSb = new StringBuilder();   
        try (Scanner scanner = new Scanner(new FileInputStream(filename), "UTF-8")) {
            while (scanner.hasNext()) {
                String s = scanner.nextLine();
                fileSb.append(s);
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        return fileSb.toString();
    } 

    public static void main(String[] args) {
        String file = readFile("test.json");
        Tokenizer tokenizer = new Tokenizer(file);
        ArrayList<Token> tokens =  tokenizer.tokenize();
        //tokens.forEach(t -> System.out.print(t + " "));
        
        Parser parser = new Parser();
        Value value = parser.parse(tokens);
        System.out.println(value);
    }

}