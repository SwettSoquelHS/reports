import java.util.List;
import java.util.ArrayList;


public class SwetterciseTest extends TUtils {

    public static void main(String[] args){
        doTestReverse();
        doTestColatz();
        doTestPrime();

        dumpReport();
    }


    public static void doTestPrime(){
        startTest("Results for isPrime()");
        int errorCount = 0;
        int sourceNum = 12;
        boolean passed = true;

        if (!testIsPrime(sourceNum, false)) {
            errorCount++;
            passed = false;
        }

        sourceNum = 4;                       
        if (!testIsPrime(sourceNum, false)) {
            errorCount++;
            deduct(0.01);
            passed = false;
        }

        sourceNum = 7;               
        if( !testIsPrime(sourceNum, true) ){
            errorCount++;
            passed = false;
        }

        sourceNum = 13;               
        if( !testIsPrime(sourceNum, true) ){
            errorCount++;
            passed = false;
        }

        sourceNum = 15;               
        if( !testIsPrime(sourceNum, false) ){
            errorCount++;
            passed = false;
        }

        sourceNum = 2048;               
        if( !testIsPrime(sourceNum, false) ){
            errorCount++;
            passed = false;
        }

        sourceNum = 1031;
        if( !testIsPrime(sourceNum, isPrime(sourceNum)) ){
            errorCount++;
            passed = false;
        }

        if (errorCount > 5)
            deduct(0.15);
        else if (errorCount > 3)
            deduct(0.08);
        else if (errorCount > 0)
            deduct(0.04);

        endTest();
    }

    public static boolean testIsPrime(int num, boolean expected){
        boolean gotBack;
        try {
            gotBack = Swettercise1.isPrime(num);
            boolean result = expected == gotBack;
            addResult("isPrime", String.valueOf(num), String.valueOf(gotBack), String.valueOf(expected), result );
            return result;
        } catch (Exception e) {
            deduct(0.05);
            addResult("isPrime", String.valueOf(num), String.valueOf(null), String.valueOf(expected), false);
            return false;
        }           
    }

    public static void doTestColatz(){
        startTest("Results for collatzThis()");
        int sourceNum = 12;
        String expected = collatzThis(sourceNum);
        boolean passed = false;
        passed = testColatz(sourceNum, expected);

        sourceNum = 4;
        expected = collatzThis(sourceNum);        
        passed = testColatz(sourceNum, expected) && passed;

        sourceNum = 11;
        expected = collatzThis(sourceNum);        
        passed = testColatz(sourceNum, expected) && passed;

        endTest();
    }

    public static boolean testColatz(int num, String expected){
        String gotBack = "";
        try {
            gotBack = Swettercise1.collatzThis(num);
            String[] botBackSplit = gotBack.split(",");
            String[] expectedSplit = expected.split(",");
            boolean matched = true;
            for(int i = 0; i < expectedSplit.length - 1 && matched; i++ ){
                matched = expectedSplit[i].trim().equals( botBackSplit[i].trim() ) && matched;                                    
            }

            if(!matched){
                deduct(0.03);
            }

            addResult("collatzThis", String.valueOf(num), gotBack, expected, matched );
            return matched;
        } catch (Exception e) {
            deduct(0.05);
            addResult("collatzThis", String.valueOf(num), gotBack, expected, false);
            return false;
        }        
    }

    public static void doTestReverse(){
        startTest("Results for reverseStr()");
        String strCase = "I haz win?";
        String expected = reverseStr(strCase);
        boolean passed = false;
        passed = testReverse(strCase, expected);

        strCase = "007 bond james";
        expected = reverseStr(strCase);
        passed = testReverse(strCase, expected) && passed;
        
        strCase = "banannas";
        expected = reverseStr(strCase);
        passed = testReverse(strCase, expected) && passed;

        strCase = "tacocat";
        expected = reverseStr(strCase);
        passed = testReverse(strCase, expected) && passed;
        endTest();
        if (!passed){
            deduct(0.12);
        }        
    }

    public static boolean testReverse(String input, String expected){
        String gotBack = "";
        try {
            gotBack = Swettercise1.reverseStr(input);
            boolean result = expected.equals(gotBack);
            addResult("reverseStr", input, gotBack, expected, result );
            return result;
        } catch (Exception e) {
            addResult("reverseStr", input, gotBack, expected, false);
            return false;
        }
    }



    public static String reverseStr(String str){
        String result = "";
        for(int i = str.length()-1; i >= 0; i--){
            result = result + str.charAt(i);
        }
        return result;
    }   

    public static boolean isPrime(int number){
        for(int i = 2; i < Math.sqrt(number); i++){
            if (number % i == 0)
                return false;
        }
        return true;
    }

    public static String collatzThis(int number){
        String result = String.valueOf(number);
        while(number > 2){
            if (number % 2 == 0)
                number = number / 2;
            else
                number = 3 * number + 1;
            result = result + ", " + number;
        }

        result = result + ", 1";

        // If the number is even, divide it by two.
        // If the number is odd, triple it and add one.
        return result;
    }

}
