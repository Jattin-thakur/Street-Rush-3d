public class pri {

    public static void main(String[] args) {
        int num = 29;

        if (isPrime(num)) {
            System.out.println(num + " is a prime number.");
        } else {
            System.out.println(num + " is not a prime number.");
        }
    }

    public static boolean isPrime(int num) {
        if (num < 2) {
            return false;
        }

        for (int i = 2; i < num; i++) {
            if (num % i == 0) {
                return false;
            }
        }

        return true;
    }
}
//1.just create an array of size n ;
// mark every element true ;
// write a loop from 2 to n  including n;