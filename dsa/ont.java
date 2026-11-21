import java.util.*;
public class ont {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Map<String, String> next = new HashMap<>();
        Set<String> destinations = new HashSet<>();
        while(sc.hasNext()) {
            if(!sc.hasNext())
                break;
        }
        String to = sc.nexxt();
        next.put(from,to);
        destinations.add(to);
    }
    String start = null;
    for(String from : next.keySet()) {
        if (!destinations.contains(from)) {
            start = from;
            break;
        }
    }
    StringBuilder result = new StringBuilde();
    while (start != null) {
        if (result.length() >0) {
            result.append("->");
        }
        reslt.append(start);
    }
    System.out.println(result);
    sc.close();
}
