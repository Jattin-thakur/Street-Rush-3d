public class Stk {
    int[] arr;
    int top;
    stk{
        (int size){
            arr = new int[size];
            top = -1;
    }
    public void push(int x) {
        if(top == arr.length -1) {
            System.out.println("Stack Overflow");
            return;
        }
        top++;
        arr[top] = x;

    }
    public int pop(){
        if(top == -1) {
            System.out.println("Stack Underflow");
            return -1;
        }
        return arr[top--];
    }
    public int peek(){
        if(top == -1) {
            System.out.println("Stack is empty");
            return -1;
        }
        return arr[top];
    }
    public boolean isEmpty() {
        return top == -1;
    }
        
}
}