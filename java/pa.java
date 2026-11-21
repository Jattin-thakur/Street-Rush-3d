public class pa {
    public static void main(String[] args){
        // 1. Declare and initialize 'n' (number of rows)
        int n = 5;
        
        // print the pascal triangle
        for (int line = 0; line < n; line++) {
            int C = 1;
            for (int i = 0; i <= line; i++) {
                System.out.print(C + " ");
                C = C * (line - i) / (i + 1); // Calculate next element
            }
            System.out.println();
        }
    }
}


// find the element at the specific row and column in pascal triangle
// print the pascal triangle
// print the specific row
