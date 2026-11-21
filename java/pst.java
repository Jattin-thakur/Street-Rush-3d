import java.util.Scanner;

public class SumTriangleBruteForce {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter the size of array: ");
        int n = sc.nextInt();

        int[] arr = new int[n];

        System.out.println("Enter array elements:");
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        System.out.println("Sum Triangle:"); 

        while (n > 0) {
            for (int i = 0; i < n; i++) {
                System.out.print(arr[i] + " ");
            }
            System.out.println();
            int[] next = new int[n - 1];

            for (int i = 0; i < n - 1; i++) {
                next[i] = arr[i] + arr[i + 1];
            }

            arr = next;
            n--;
        }

        sc.close();
    }
}