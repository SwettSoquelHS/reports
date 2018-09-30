
import os, sys


def isStudent( firstName, githubUser, lookForName ):        
    if firstName.lower() == lookForName.lower():
        return True
    if githubUser.lower() == lookForName.lower():
        return True
    return False


def getStudents( loadOnlyStudent = None ):
    if os.path.isfile('students.txt'):
        result = []
        with open("students.txt" , "r") as file:
            for stuLine in file:
                if stuLine.strip() == '#':
                    break
                stuff = stuLine.split(',')
                if loadOnlyStudent is None:
                    result.append( (stuff[0].strip(), stuff[1].strip(), stuff[2].strip() ) )
                elif isStudent( stuff[0].strip(), stuff[1].strip(), loadOnlyStudent ) == True:
                    result.append( (stuff[0].strip(), stuff[1].strip(), stuff[2].strip() ) )
        
        return result

    else:
        print("No students.txt file exists.")
        print("Create students.txt file with format:")
        print("\t StuName,email,gihubname")
        #Aaron, student@email.com , gitHubUName
        sys.exit(1)
        
    
