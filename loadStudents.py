
def getStudents():
    result = []
    with open("students.txt" , "r") as file:
        for stuLine in file:
            stuff = stuLine.split(',');
            result.append( (stuff[0].strip(), stuff[1].strip(), stuff[2].strip() ) )
        
    return result;
