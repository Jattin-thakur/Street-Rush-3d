import java.util.Scanner;

public class q {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter brackets: ");
        String s = sc.nextLine();

        Stk stack = new Stk(s.length());

        for (char c : s.toCharArray()) {

            // Opening brackets
            if (c == '(' || c == '{' || c == '[') {
                stack.push(c);
            }

            // Closing brackets
            else if (c == ')' || c == '}' || c == ']') {

                if (stack.isEmpty()) {
                    System.out.println(false);
                    return;
                }

                char top = (char) stack.pop();

                if ((c == ')' && top != '(') ||
                    (c == '}' && top != '{') ||
                    (c == ']' && top != '[')) {

                    System.out.println(false);
                    return;
                }
            }
        }

        // If stack is empty, all brackets matched
        System.out.println(stack.isEmpty());
    }
}