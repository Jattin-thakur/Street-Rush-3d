public class Qstn {
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        System.out.println(x: Enter the number);
        int n = sc.nextInt();
        int factorial = 1;
        for (int i = 1; i <= n; i++) {
            factorial *= i;

        }
        System.out.println("Factorial of " + n + " is: " + factorial);
        while(factorial%10==0){
            factorial/=10;
        }System.out.println("Factorial of without trailing zeros is: " + factorial);
        System.out.println(factorial%100000000l);
    }
}
// 123456789 %10