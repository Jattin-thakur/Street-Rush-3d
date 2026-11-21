import java.util.Scanner;
import java.util.Stack;

public class palin{

    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {

        int t = sc.nextInt();
        sc.nextLine();

        for (int i = 0; i < t; i++) {
            solve();
        }
    }

    static void solve() {

        String s = sc.nextLine();

        Stack<Character> st = new Stack<>();

        // Push every character into the stack
        for (char c : s.toCharArray()) {
            st.push(c);
        }

        // Compare original string with reversed string
        for (char c : s.toCharArray()) {

            if (c != st.pop()) {
                System.out.println("Not palindrome");
                return;
            }
        }

        System.out.println("Palindrome");
    }
}