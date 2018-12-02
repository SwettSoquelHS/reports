class TestTile extends TUtils {
    public static void main(String[] args){
        WEB_RUN = true;
        /*
         Exercise 3  
        // In the board game Scrabble, each tile contains a letter, which is used to spell words in rows and columns, and a score, which is used to determine the value of words.

        // Write a definition for a class named Tile that represents Scrabble tiles. The instance variables should include a 
            character named letter and an integer named value.
        // Write a constructor that takes parameters named letter and value and initializes the instance variables.
        // Write a method named printTile that takes a Tile object as a parameter and displays the instance variables in a 
            reader-friendly format.
        // Write a method named testTile that creates a Tile object with the letter Z and the value 10, and then uses 
            printTile to display the state of the object.
        // Implement the toString and equals methods for a Tile.
        // Create getters and setters for each of the attributes.
        // The point of this exercise is to practice the mechanical part of creating a new class definition.

        */

        runTests();
        dumpReport();
    }

    public static void runTests(){
        startTest("Chapter11, Exercise3: Tile Class");
        tryCreate('C', 3);
        tryCreate('Z', 10);
        tryCheckGetterSetters('C', 3);
        tryCheckGetterSetters('Z', 10);
        trytoString('Z', 10);
        tryEquals('Z', 3);        
    }


     public static void tryCreate(char c, int value){
        try {
            Tile t = new Tile(c, value);        

            if (t == null){
                addResult("Null Tile: new Tile", c + ", " + value,"Null", "Expected new Tile to be created", false);
                deduct(0.03);
            }  else {
                addResult("new Tile()", c + ", " + value,"Null", "Expected new Tile to be created", true);
            }         
        } catch (Exception e) {
            deduct(0.1);
            //addResult(String methodTested, String argument, String received, String expected, boolean passed){
            addResult("Exception: new Tile", c + ", " + value, "Exception", "Expected new Tile to be created", false);                    
        }
    }


    public static void tryCheckGetterSetters(char c, int value){
        try {
            Tile t = new Tile(c, value);        
            if (t != null){
                if( c != t.getLetter()){
                    deduct(0.02);
                    addResult("Tile[" + t.toString() +" ].getLetter", "", ""+t.getLetter(), ""+c, false);
                } else {
                    addResult("Tile[" + t.toString() +" ].getLetter", "", ""+t.getLetter(), ""+c, true);
                }
                
                if( value != t.getValue()){
                    deduct(0.02);
                    addResult("Tile[" + t.toString() +" ].getValue", "", ""+t.getValue(), ""+value, false);
                } else {
                    addResult("Tile[" + t.toString() +" ].getValue", "", ""+t.getValue(), ""+value, true);
                }

                t.setLetter('A');
                if( t.getLetter() != 'A'){
                    deduct(0.05);
                    addResult("Tile[" + t.toString() +" ].setLetter", "'A'", ""+t.getLetter(), "'A'", false);
                } else {
                    addResult("Tile[" + t.toString() +" ].setLetter", "'A'", ""+t.getLetter(), "'A'", true);
                }

                t.setValue(8);
                if( t.getValue() != 8){
                    deduct(0.05);
                    addResult("Tile[" + t.toString() +" ].getValue", "", ""+t.getValue(), "8", false);
                } else {
                    addResult("Tile[" + t.toString() +" ].getValue", "", ""+t.getValue(), "8", true);
                }

            }            
        } catch (Exception e) {
            deduct(0.1);
            //addResult(String methodTested, String argument, String received, String expected, boolean passed){
            //addResult(String methodTested, String argument, String received, String expected, boolean passed){
            addResult("Exception during get/set test", c + ", " + value, "excception thrown",
             "Expected setter/getters to work", false);            
        }
    }

    public static void trytoString(char c, int value){
        try {
            Tile t = new Tile(c, value);        
            if(t!=null){
                String s = t.toString();
                String expected = c + " - " + value;
                if (expected.equals(s)){
                    addResult("Tile[" + t.toString() +" ].toString", "", s, expected, true);
                } else {
                    addResult("Tile[" + t.toString() +" ].toString", "", s, expected, false);
                    deduct(0.05);
                }
            }
            
        } catch (Exception e) {
            deduct(0.1);
            //addResult(String methodTested, String argument, String received, String expected, boolean passed){
            addResult("Exception: toString", c + ", " + value, "Exception", "Expected during toString()", false);                    
        }
    }


    public static void tryEquals(char c, int value){
        try {
            Tile t = new Tile(c, value);
            Tile t2 = new Tile(c, value);        
            if(t!=null){
                            
                if (t.equals(t2)){
                    addResult("Tile[" + t.toString() +" ].equals", "", "", "Same tiles are equal", true);
                } else {
                    addResult("Tile[" + t.toString() +" ].equals", "", t2.toString() , "Expected same tiles to be the same.", false);
                    deduct(0.05);
                }

                t2.setValue(value + 5);
                if (!t.equals(t2)){
                    addResult("Tile[" + t.toString() +" ].!equals", "", "", "Different tiles are not equal", true);
                } else {
                    addResult("Tile[" + t.toString() +" ].!equals", "", t2.toString() , "Different Tiles were same", false);
                    deduct(0.03);
                }

            }
            
        } catch (Exception e) {
            deduct(0.1);
            //addResult(String methodTested, String argument, String received, String expected, boolean passed){
            addResult("Exception: equals", c + ", " + value, "Exception", "Expected during equals()", false);                    
        }
    }

}