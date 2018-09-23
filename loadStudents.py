
import os, sys


    


def getStudents():
    if os.path.isfile('students.txt'):
        result = []
        with open("students.txt" , "r") as file:
            for stuLine in file:
                stuff = stuLine.split(',');
                result.append( (stuff[0].strip(), stuff[1].strip(), stuff[2].strip() ) )
    else:
        print("No students.txt file exists.")
        print("Create students.txt file with format:")
        print("\t StuName,email,gihubname")
        #Aaron, student@email.com , gitHubUName
        sys.exit(1)
        
    return result;
