import java.util.LinkedList;
import java.util.Queue;

public class qeue {
    Queue<Integer> q1 =new LinkedList<>();
    Queue<Integer> q2 =new LinkedList<>();

    public void push(int x ){
        q2.offer(x);
        while(!q1.isEmpty()){
            q2.offer(q1.poll());

        }
    }
    public int pop(){
        return q.poll();
    }
    public int peek(){
        return q.peek();
    }
    public boolean isEmpty(){
        return q.isEmpty();
    }
    public int size(){
        return q.size();
    }
}
