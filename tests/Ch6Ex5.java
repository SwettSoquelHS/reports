public class Ch6Ex5 extends TUtils{
    public static void main(String[] args){        
        testExercise5();
        dumpReport();
    }


    public static void testExercise5(){
        startTest("Results for Exercise5().isDoubloon()");
        int errorCount = 0;
        if(!tryEx5("abcdef", false)){
            errorCount++;
        }
        if(!tryEx5("aa", true)){
            errorCount++;
        }
        if(!tryEx5("anna", true)){
            errorCount++;
        }
        if(!tryEx5("abcdabcd", true)){
            errorCount++;
        }
        if(!tryEx5("aaa", false)){
            errorCount++;
        }
        if(!tryEx5("intestines", true)){
            errorCount++;
        }
        if(!tryEx5("i cook crepes on sundays!", false)){
            errorCount++;
        }

        if(!tryEx5("Bannab", true)){
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


    public static boolean tryEx5(String testStr, boolean expectedResult){
        try {
            boolean isIt = Exercise5.isDoubloon(testStr);
            addResult("Exercise5.isDoubloon", testStr , String.valueOf(isIt), 
                String.valueOf(expectedResult), isIt == expectedResult);
            return isIt == expectedResult;
        } catch (Exception e) {
            deduct(0.05);
            //addResult(String methodTested, String argument, String received, String expected, boolean passed){
            addResult("Exercise5.isDoubloon", testStr , "Exception Thrown", String.valueOf(expectedResult), false);
            return false;            
        }
    }


    public static int countChar(String str, char c){
        int charCount = 0;
        for(int j = 0 ; j<str.length(); j++){
            if( str.charAt(j) == c)
                charCount++;
        }
        return charCount;
    }

    public static boolean isDoubloon(String str){
        str = str.toLowerCase();

        for(int i = 0; i < str.length(); i++){
            char currentChar = str.charAt(i);
            int charCount = countChar(str, currentChar);
            if (charCount != 2) {
                return false;
            }
        }
        return true;
    }

    public static boolean canSpell(String letters, String canSpell){
        letters = letters.toLowerCase();
        canSpell = canSpell.toLowerCase();
        for(int i = 0; i < canSpell.length(); i++){
            int needCount = countChar(canSpell, canSpell.charAt(i));
            int haveCount = countChar(letters, canSpell.charAt(i));
            if(haveCount < needCount)
                return false;
        }
        return true;
    }

}