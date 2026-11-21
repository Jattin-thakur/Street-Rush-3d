import java.util.Queue;

public class s {
    public static void main(String[] args) {}

        static boolean canSort(Queue<Integer> q) {
            Stack<Integer> stack = new Stack<>();
            int expected = 1;

            while (!q.isEmpty()) {
                int current = q.poll();

                // If the current number is the expected one, move to the next expected number
                if (current == expected) {
                    expected++;
                } else {
                    // If the stack is not empty and the top of the stack is the expected number
                    while (!stack.isEmpty() && stack.peek() == expected) {
                        stack.pop();
                        expected++;
                    }

                    // If the current number is greater than the expected number, push it onto the stack
                    if (current > expected) {
                        stack.push(current);
                    } else {
                        // If the current number is less than the expected number, sorting is not possible
                        return false;
                    }
                }
            }

            // After processing all elements, check if we can pop remaining elements from the stack in order
            while (!stack.isEmpty()) {
                if (stack.pop() != expected) {
                    return false;
                }
                expected++;
            }

            return true;
        }
}
