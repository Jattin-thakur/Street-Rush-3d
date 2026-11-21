public class main {
    public static void main(String[] args) {

        Stk st = new Stk(5);

        st.push(5);
        st.push(10);
        st.push(8);
        st.push(9);

        while (!st.isEmpty()) {
            System.out.println(st.pop());
        }
    }
}
