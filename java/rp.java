import java.util.Scanner;

public class rp{
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter distance: ");
        double distance = sc.nextDouble();

        System.out.print("Enter time : ");
        double time = sc.nextDouble();

        double speed = distance / time;

        System.out.println("Speed = " + speed + " km/h");

        sc.close();
    }
}