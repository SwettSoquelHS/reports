public class CheckPokerHands {

    // which accepts an array of cards as its only parameter and determines whether or 
    //   not the array of Cards represents a Royal Flush
    public static boolean isRoyalFlush(Card[] hand){

        int suit = hand[0].getSuit();

        for(Card c: hand){
            if(c.getSuit() != suit)
                return false;
        }
        return hasRank(hand, Card.ACE) && hasRank(hand, Card.KING) &&
            hasRank(hand, Card.QUEEN) && hasRank(hand, Card.JACK) && hasRank(hand, 10);
    } 

    private static boolean hasRank(Card[] hand, int rank ){
        for(Card c: hand){
            if(c.getRank() == rank)
                return true;
        }
        return false;
    }

    private static int getLowestRank(Card[] hand){
        int result = hand[0].getRank();
        for(Card c: hand){
            if((c.getRank() < result && c.getRank() != Card.ACE) || result == Card.ACE){  
                result = c.getRank();
            }
        }
        return result;
    }

    public static boolean isStraightFlush(Card[] hand){
        int suit = hand[0].getSuit();

        for(Card c: hand){
            if(c.getSuit() != suit){
                return false;
            }
        }

        int[] ranksWeHave = new int[14];
        for(Card c: hand){
            ranksWeHave[c.getRank()]++;
        }

        int lowRank = getLowestRank(hand);    
        int expetecdSum = 5*lowRank + 10;

        //crap, we have a 10 the ace is only worth 1
        if(lowRank == 10){
            expetecdSum = 47;
        }

        int checkSum = 0;
        for(Card c: hand){
            if(ranksWeHave[c.getRank()] == 1){
                checkSum += c.getRank();
            }
        }
        return expetecdSum == checkSum;
    }

    public static boolean isFlush(Card[] hand){
        int s = hand[0].getSuit();
        for(int i =0; i<hand.length; i++){
            if (hand[i].getSuit() != s)
                return false;
        }
        return true;
    }

    public static boolean isFullHouse(Card[] hand){
        int[] cardCounts = new int[14];
        for(Card c: hand){
            cardCounts[c.getRank()]++;
        }

        boolean hasPair = false;
        boolean hasThreeOf = false;

        for(int cnt: cardCounts){
            if (cnt == 2)
                hasPair = true;
            if (cnt == 3)
                hasThreeOf = true;
        }

        return hasPair && hasThreeOf;
    }
    
    public static Card highCard(Card[] hand){
        int highValue = -1;
        Card result = null;
        for(int i = 0; i < hand.length; i++){
            if(hand[i].getRank() == Card.ACE){
                return hand[i];
            }

            if (hand[i].getRank() > highValue){
                highValue = hand[i].getRank();
                result = hand[i];
            }
        }
        return result;
    }
}