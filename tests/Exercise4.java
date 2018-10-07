public class Exercise4 {
    
    public static boolean isAbecedarian(String str){
        return false;
    }

    public static int indexOfMax(int[] someInts){
        return 0;
    }

    /*
    Write a method called sieve that takes an integer parameter, n, 
    and returns a boolean array that indicates, for each number 
    from 0 to n - 1, whether the number is prime.
    */
    public static boolean[] sieve(int n){
        boolean[] result = new boolean[n];
        for (int i = 0; i < n; i++){
            result[i] = i%2==0;
        }
        return result;
    }
}