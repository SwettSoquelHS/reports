public class Tile {
    //     Exercise 3  
// In the board game Scrabble, each tile contains a letter, which is used to spell words in rows and columns, and a score, which is used to determine the value of words.

// Write a definition for a class named Tile that represents Scrabble tiles. 
    //The instance variables should include a character named letter and an integer named value.
// Write a constructor that takes parameters named letter and value and initializes the instance variables.
// Write a method named printTile that takes a Tile object as a parameter and displays the instance variables in a 
    //reader-friendly format.
// Write a method named testTile that creates a Tile object with the letter Z and the value 10, and then uses printTile to display the state of the object.
// Implement the toString and equals methods for a Tile.
// Create getters and setters for each of the attributes.
// The point of this exercise is to practice the mechanical part of creating a new class definition.

    int value;
    char letter;

    public Tile(char letter, int value){
        this.letter = letter;
        this.value = value;
    }

    public void printTile(Tile t){
        System.out.println(t);
    }

    public void setLetter(char c){
        letter = c;
    }

    public char getLetter(){
        return letter;
    }

    public void setValue(int value){
        this.value = value;
    }

    public int getValue(){
        return value;
    }

    public String toString(){
        return letter + " - " + value;
    }

    public boolean equals(Tile that){
        return this.letter == that.letter && this.value == that.value;
    }

    public static void testTile(){
        Tile z =  new Tile('Z', 10);
        z.printTile(z);
    }

}