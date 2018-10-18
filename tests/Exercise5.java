public class Exercise5 {
    
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
}