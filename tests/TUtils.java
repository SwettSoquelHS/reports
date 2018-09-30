import java.util.List;
import java.util.ArrayList;

public class TUtils {
    static List<String> results = new ArrayList<String>();
    static double deduction = 0.0;


    public static void startTest(String testPhase){
        results.add("\n<br>" + testPhase +"\n");
        results.add("<table width=\"600\" border=\"1\"><tr>"+
            "<th align=\"right\" width=\"200\"> Function Call</th><th align= \"left\"> -->Your output<--</th><th width=\"50\"> Expected Output </th>"+
            "</tr>");
    }

    public static void endTest(){
        results.add("</table><br>\n");
    }

    public static void addResult(String methodTested, String argument, String received, String expected, boolean passed){
        
        results.add("<tr><td align=\"right\" width=\"200\">"+methodTested + "(\"" + argument + "\")  </td><td align=\"left\">" + received + "</td>");
        if (passed){
            results.add("<td width=\"50\" bgcolor=\"green\"> :) </td></tr>\n");
        } else {
            results.add("<td bgcolor=\"red\"><b>" + expected + " </b></td></tr>\n");
        }        
    }

    public static void deduct(double deduct){
        deduction += deduct;        
    }

    public static void dumpReport(){
        String dump = "";
        for(String s: results){
            System.out.print(s);
        }
            //dump = dump + s;
        //System.out.print(dump);
        System.out.println("[deductions="+deduction+"]\n");
    }
}