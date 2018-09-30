import sys, os, time, subprocess, getpass
from datetime import date
from subprocess import Popen, PIPE, STDOUT



#
#   Attempts to comiple java file in the directory specified by workingDir
#   relative the current directory
# 
#  Return[0]: 0 = succcess, 1 = compile time error, 2 = missing target
#  Return[1]: log output
def tryCompile( workingDir, javaFile):
    reportLog = []
    error_code = 0
    reportLog.append("[COMPILING] " + javaFile)
    
    if os.path.isfile(workingDir+'/'+ javaFile):

        p = Popen(['javac', javaFile], cwd=workingDir, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        output = p.communicate()[0]
        if p.returncode != 0: 
            reportLog.append( 
                "\t[ERROR] javac failed " + javaFile + "\n ----begin compile output------- \n" 
                + output.decode("utf-8").replace("\n", "\n\t") + "\n-----------END COMPILE-------" )
            error_code = 1
        else:
            reportLog.append( "\t[SUCCESSFUL COMPILE] " + javaFile)
    else:
        reportLog.append( "\t[ERROR] Missing Compile Target:" + javaFile)
        error_code = 2

    return (error_code, reportLog)



def extractDeduction( output ):
    lookFor = "[deductions="               
    startsAt = output.find(lookFor)    
    if startsAt > 0:
        endsAt = output.find("]",startsAt)
        deduction = output[startsAt+len(lookFor): endsAt]
        return float(deduction)
    else:
        print("Janky test.... starts at = ", startsAt)
    return 0;

def tryRun( workingDir, target):
    reportLog = []
    error_code = 0
    #try running
    javaClass = target + ".class"
    if os.path.isfile(workingDir+'/'+ javaClass):
        reportLog.append( "[RUNNING] " + target + "\n-->")
        p = Popen(['java', target], cwd=workingDir,
                    stdout=PIPE, stdin=PIPE, stderr=PIPE)
        stdout_data = p.communicate()
        if p.returncode == 0: 
            testOutput = stdout_data[0].decode("utf-8").replace("\n", "\n\t")
            deduction = extractDeduction(testOutput)
            reportLog.append( testOutput )
            reportLog.append( "<--\n\t[OUTPUT OK]\n" )
            return (error_code, reportLog, deduction)

        else:
            reportLog.append( "\t[ERROR] Runtime Error @ java " + target + "\n" +  
            stdout_data[0].decode("utf-8").replace("\n", "\n\t") )
            error_code = 3


    else:
        error_code = 2
        reportLog.append("[ERROR] Target missing: " + target + " in directory: " + workingDir)

    return (error_code, reportLog)


def expandStrs(listOfStrings):
    result = ""
    for s in listOfStrings:
        result = result + s + "\n"
    return result


if __name__ == "__main__":
    testDir = "./tests"
    target = "SwetterciseTest"

    r = tryCompile(testDir, "Swettercise1.java")
    print("Status: " + str(r[0]))
    print("output: \n" + expandStrs(r[1]) )

    r = tryCompile(testDir, "SwetterciseTest.java")
    print("Status: " + str(r[0]))
    print("output: \n" + expandStrs(r[1]) )

    r = tryRun(testDir, "SwetterciseTest")
    print("Status: " + str(r[0]))
    output = expandStrs(r[1])
    print("output: \n" +  output)
    extractDeduction(output)





