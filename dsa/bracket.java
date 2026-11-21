public class bracket {
    public static void main(String[] args) {
        String s = sc.nextline();
        Stack<Character> st = new Stack<> ();
        for(cahr ch: s.toCharArray()){
            if(ch !=')'){
                st.push(ch);
            }
            else{
                if(st.peek() !='(')return true;
                while(st.peek() !='('){
                    st.pop();

                }
                st.pop();
            }
        }
        return false;


    }
    
}
