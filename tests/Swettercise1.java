public class Swettercise1{
    public static void main(String[] args){
        System.out.println("Swettercise 1");
        System.out.println(reverseStr("This is not reversed!"));

        System.out.println( isPrime(14) );
        System.out.println( isPrime(13) );
        System.out.println( isPrime(19) );

        System.out.println( collatzThis(12) );        

    }

    public static String reverseStr(String str){
        String result = "";
        for(int i = str.length()-1; i >= 0; i--){
            result = result + str.charAt(i);
        }
        return result;
    }   

    public static boolean isPrime(int number){
        for(int i = 2; i <= Math.sqrt(number); i++){
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