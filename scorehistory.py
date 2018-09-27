import json, os

#Right now this assumes a per project
#level run, so if something other than think-java 
# is run at the same time then this will break, otherwise
# loading/saving on per project basis
assignHistory = {}

def save( fileNmae ):
    with open(fileNmae, 'w') as outfile:
        json.dump(assignHistory, outfile)

def load( fileName ):
    #If there is no history then nothing can be laoded

    if os.path.isfile(fileName):
        with open(fileName) as f:
            assignHistory = json.load(f)
    else:
        print("INFO: No assignment history for:", fileName)

def debug( ):
    print("\n\n")
    print(assignHistory)
    print("\n\n")


def verifyAssignment(assignment):
    print(assignment)
    if assignment not in assignHistory.keys():
        # Create a map for assignments to live in
        assignHistory[assignment] = {} 


def verifyUser(assignment, githubUser):
    # get the map of assignments
    users = assignHistory[assignment]
    if githubUser not in users.keys():
        # since this user does not have an entry
        # make one for the users
        users[githubUser] = {"prev": None, "curr": None}
        assignHistory[assignment] = users

def getPrevScore(assignment, githubUser):
    # get the map of assignments
    users = assignHistory[assignment]
    if githubUser in users.keys():
        # since this user does not have an entry
        # make one for the users
        return users[githubUser]["prev"]

    #This should probably be an error
    print("WARNING: Previous Score should exist in this context: ", assignment, githubUser)
    return None

def getCurrScore(assignment, githubUser):
    # get the map of assignments
    users = assignHistory[assignment]
    if githubUser in users.keys():
        # since this user does not have an entry
        # make one for the users
        return users[githubUser]["curr"]

    #This should probably be an error
    print("WARNING: Current Score should exist in this context: ", assignment, githubUser)
    return None


def setPrevScore(assignment, githubUser, score):
    # get the map of assignments
    users = assignHistory[assignment]
    if githubUser in users.keys():
        # since this user does not have an entry
        # make one for the users
        oldPrev = users[githubUser]["prev"]
        users[githubUser]["prev"] = score
        return oldPrev

    #This should probably be an error
    print("WARNING: Set Previous Score should exist in this context: ", assignment, githubUser)
    return None


def setCurrScore(assignment, githubUser, score):
    # get the map of assignments
    users = assignHistory[assignment]
    if githubUser in users.keys():
        # since this user does not have an entry
        # make one for the users
        oldCurr = users[githubUser]["curr"]
        users[githubUser]["curr"] = score
        return oldCurr

    #This should probably be an error
    print("WARNING: Set Curr Score should exist in this context: ", assignment, githubUser)
    return None


def setScore(assignment, githubUser, score):
    verifyAssignment(assignment)
    verifyUser(assignment, githubUser)

    #Get the old current score and set it to previous
    previousScore = getCurrScore(assignment, githubUser)
    if not (score == previousScore):
        setPrevScore(assignment, githubUser, previousScore)
        setCurrScore(assignment, githubUser, score)
        return previousScore
    
    return score


    
