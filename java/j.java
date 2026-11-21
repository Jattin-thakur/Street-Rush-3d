import java.util.Arrays;
import java.util.Scanner;

public class j{
    public static void main(String[] args){
        // Scanner sc = new Scanner(System.in);
        // int n = sc.nextInt();
        // int arr[] = {10,3033, 34,2,4,5,63,53,5,54,4};
        // int max= arr[0];
        // for(int i=0;i<arr.length;i++)
        // {
        //     if(max<arr[i]);{
        //         max=arr[i];
        //     }
        // }
        // int[] n = {10,3033, 34,2,4,5,63,53,5,54,4};
        // double sum=0;
        // for(int i =0; i<n.length;i++)
        // {
        //     sum+=n[i];
        // }
        // double avg = sum/n.length;
        // System.out.println(avg);
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter a number: ");
        int number = scanner.nextInt();

        if (isPrime(number)) {
            System.out.println(number + " is a prime number.");
        } else {
            System.out.println(number + " is not a prime number.");
        }

        scanner.close();
    }

    public static boolean isPrime(int num) {
        // Numbers less than or equal to 1 are not prime
        if (num <= 1) {
            return false;
        }

        // Check divisors from 2 up to the square root of the number
        for (int i = 2; i <= Math.sqrt(num); i++) {
            if (num % i == 0) {
                return false; // Found a factor, so it's not prime
            }
        }

        return true; // No factors found, so it is prime
    }
}
    
