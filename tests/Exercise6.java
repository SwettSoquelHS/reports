public class Exercise6 {
    
    public static boolean isDoubloon(String str){
        return false;
    }
        // that takes an integer 
        // n and an array of integers, and that returns true if 
        // the numbers in the array are all factors of n 
    public static boolean areFactors(int n, int[] nums){
        for(int i=0; i<nums.length; i++){
            if ( n % nums[i] != 0)
                return false;
        }
        return true;
    }

//     Exercise 6  
// Write a method named arePrimeFactors that takes an integer n and an array of integers, 
    //and that returns true if the numbers in the array are all prime and their product is n.
    public static boolean arePrimeFactors(int n, int[] nums){
        int product = 1;
        for(int i = 0; i < nums.length; i++){
            if( !isPrime(nums[i])){                
                return false;
            }
            product *= nums[i];
        }
        return product == n;
    }

    public static boolean isPrime(int n){
        if(n <= 1)
            return false;
        for(int i = 2; i < n/2; i++){
            if (n%i==0)
                return false;
        }
        return true;
    }

}