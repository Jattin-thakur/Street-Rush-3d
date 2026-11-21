import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter the number of rows: ");
        int rows = sc.nextInt();

        for (int row = 0; row < rows; row++) {
            int value = 1;

            for (int space = 0; space < rows - row; space++) {
                System.out.print(" ");
            }

            for (int column = 0; column <= row; column++) {
                System.out.print(value + " ");
                value = value * (row - column) / (column + 1);
            }
            System.out.println();
        }
    }
}
/**
 * InnerMain
 */
public class InnerMain {

    
}