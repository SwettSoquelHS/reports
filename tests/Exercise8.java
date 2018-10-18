public class Exercise8 {
    
    // Exercise 8  
    // Two words are anagrams if they contain the same letters and 
    // the same number of each letter. For example, “stop” is an anagram 
    // of “pots” and “allen downey” is an anagram of “well annoyed”. 
    // Write a method that takes two strings and checks whether they are anagrams of each other.

    public static boolean isAnagram(String str1, String str2){

        for(int i = 0; i < str1.length(); i++){
            int currCount = countChr(str1, str1.charAt(i));
            int str2Count = countChr(str2, str1.charAt(i));
            if(currCount != str2Count)
                return false;
        }
        
        return true;
    }

    public static int countChr(String str1, char c){
        int count = 0;
        for(int i=0; i < str1.length(); i++)
            if(str1.charAt(i) == c)
                count++;
        return count;
    }

}