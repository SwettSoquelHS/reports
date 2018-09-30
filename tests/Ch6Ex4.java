public class Ch6Ex4 extends TUtils{
    public static void main(String[] args){
        testExercise4();        
        dumpReport();
    }
    
    public static void testExercise4(){
        startTest("Results for Exercise4.isAbecedarian()");
        int errorCount = 0;
        if(!tryEx4("abcdef", true)){
            errorCount++;
        }

        if(!tryEx4("aaaaaa", true)){
            errorCount++;
        }

        if(!tryEx4("gfedcba", false)){
            errorCount++;
        }

        if(!tryEx4("z", true)){
            errorCount++;
        }

        if(!tryEx4("beknow", true)){
            errorCount++;
        }

        if(!tryEx4("no", true)){
            errorCount++;
        }

        if(!tryEx4("he", false)){
            errorCount++;
        }
        

        if (errorCount > 6){
            deduct(0.2);
        }
        else if ( errorCount > 4){
            deduct(0.15);
        }
        else if (errorCount > 2){
            deduct(0.1);
        } 
        else if (errorCount > 0){
            deduct(0.05);
        }
        endTest();
    }

    public static boolean tryEx4(String testStr, boolean expectedResult){
        try {
            boolean isIt = Exercise4.isAbecedarian(testStr);
            addResult("Exercise4.isAbecedarian", testStr , String.valueOf(isIt), 
                String.valueOf(expectedResult), isIt == expectedResult);
            return isIt == expectedResult;
        } catch (Exception e) {
            deduct(0.05);
            //addResult(String methodTested, String argument, String received, String expected, boolean passed){
            addResult("Exercise4.isAbecedarian", testStr , "Exception Thrown", String.valueOf(expectedResult), false);
            return false;            
        }
    }



    public static boolean isAbecedarian(String str){
        for(int i =0; i < str.length()-1; i++){
            if( str.charAt(i) > str.charAt(i+1) ){
                return false;
            }
        }
        return true;
    }

    public static int countChar(String str, char c){
        int charCount = 0;
        for(int j = 0 ; j<str.length(); j++){
            if( str.charAt(j) == c)
                charCount++;
        }
        return charCount;
    }
}