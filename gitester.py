import sys, os, time, subprocess, getpass
from datetime import date
from subprocess import Popen, PIPE, STDOUT
import loadStudents
import argparse
import scorehistory
import javaRun
from shutil import copyfile


# Stuff we need, joy.
PARSER = argparse.ArgumentParser()
PARSER.add_argument("project", help="Github project to pull.")
PARSER.add_argument("-a", "--assignment", help="Assignment within the project.")
PARSER.add_argument("-s", "--student", help="Only on the student specified.")
PARSER.add_argument("-dl", "--dl", help="Skip source DL, use -dl off, defaults to on")
args = PARSER.parse_args()


SHOULD_DL = True
if not args.dl == None:
    if args.dl.lower() == "off":
        SHOULD_DL = False

if SHOULD_DL:
    print("Mode: Download source ON")
else:
    print("Mode: Download source OFF")


#If a specific student was specified then only that student will be run
STUDENTS = loadStudents.getStudents(args.student)


#github URL pattern
#https://github.com/SwettSoquelHS/github-proj-stuGuthubuser
#https://github.com/SwettSoquelHS/github-proj-stuGuthubuser.git
HTTPS_STR = "https://"
GITHUB_PROJ_BASE_URL= "github.com/SwettSoquelHS/"

#gitHubDempURL
GITHUB_DEMO_BASE_URL = "swettsoquelhs.github.io/"

OUTPUT_DIR = './stuwork'
REPORT_DIR = './stureports'
TESTS_DIR = './tests'
 

REPORTS = "github.com/SwettSoquelHS/reports.git"

#assignMent
assignment = args.assignment

#projName
projName = args.project

OK_TO_REUSE = True
stu_to_report = {}

specificUser = None
if len(sys.argv) > 2:
    specificUser = sys.argv[2]

#score history
scoreHistory = projName + ".json"
scorehistory.load(scoreHistory)


sysUser = input("Enter the git user:")
sysPwd = getpass.getpass(prompt='Enter github pwd for '+ sysUser +'? ')


if not os.path.exists(REPORT_DIR + "/" +projName):    
    os.makedirs(REPORT_DIR + "/" +projName)


def gitPull():
    if True:            
        output = subprocess.check_output( ['git','pull'] , cwd=REPORT_DIR, 
                stderr=subprocess.STDOUT)        


def saveReportToGit(stu_to_report, reportFile):
    if True:
        stuCode = makeProjURL(HTTPS_STR+GITHUB_PROJ_BASE_URL, projName, studentGithubUser)
        printToReport(studentReport, "[Attempting DL:" + stuCode + ".git]")        
        gitURL = HTTPS_STR + sysUser + ":" + sysPwd + "@" + REPORTS 

        output = subprocess.check_output( ['git','add', "."] , cwd=REPORT_DIR, 
                stderr=subprocess.STDOUT)        

        output = subprocess.check_output( ['git','commit', '-m "report check in '+ str(date.today())+'"'] , cwd=REPORT_DIR, 
                stderr=subprocess.STDOUT)        

        output = subprocess.check_output( ['git','push', gitURL] , cwd=REPORT_DIR, 
                stderr=subprocess.STDOUT)        
        printToReport(studentReport, output.decode("utf-8").replace("\n", "\n\t"))
        printToReport(studentReport, "[REPORT DONE]")

    


#<td>Student Code Base</td><td>Live Demo</td> <td>Report</td>
def printTR(displayCodeBaseStr, codeURL, liveDisplay, liveURL, stuReport, theScore):
    result = '<tr><td><a href="' + codeURL + '">' + displayCodeBaseStr + "</a></td>"
    
    if liveDisplay != 'N/A':
        result += '<td><a href="' + liveURL +'">' + liveDisplay + '</a></td>'
    else:
        result += '<td> N/A </td>'

    if stuReport is None:
        result += '<td> N/A </td>'
    else:
        result += '<td><a href="'+ stuReport +'">Report Results</a>'

    if theScore is None:
        result += "</td>"
    else:
        result += "<td>" + str(theScore) + "</td>"
    return result +'</tr>'

def makeProjURL(base, proj, user):
    return base + proj + "-" + user


def createClassReport(projName, stu_report_map, liveDemo, scores  ):
    #scores looks like:
    #{'user': { 'assign name': score}}
    print("[FINALIZING] Running " + projName + " summary...")
    reportFile = projName + ".html"
    if not (scores is None):
        reportFile = "admin-" + reportFile

    reportFile = REPORT_DIR + "/" + reportFile

    scoreHeaderStr = ''
    if scores is not None:
        #{'asianaaron2': {'asignment_1': '0.55'}
        for student in scores.keys():
            stuScores = scores[student]
            for asignmentKey in stuScores.keys(): 
                scoreHeaderStr = scoreHeaderStr + '<td>' + asignmentKey + '</td>'
            break
        scoreHeaderStr = scoreHeaderStr + "\n"    

    with open(reportFile , "w") as file:
        file.write("<html><head><title>"+projName + " class report</title></head><body>")
        file.write("<table><tr><td>Student Code Base</td><td>Live Demo</td> <td>Report</td>")
        if scores is None:
            file.write(" </tr>")
        else:
            file.write(scoreHeaderStr + "</tr>")

        for student in STUDENTS:
            studentGit = student[2]
            stuName = student[0]
            
            stuCode = makeProjURL(HTTPS_STR+GITHUB_PROJ_BASE_URL, projName, studentGit)
            stuSite ='N/A'
            if liveDemo != None:
                stuSite = makeProjURL(HTTPS_STR+GITHUB_DEMO_BASE_URL, projName, studentGit) 

            stuReport = None
            if studentGit in stu_report_map.keys():
                stuReport = stu_report_map[studentGit]

            theScore = None
            tdData = ""
            if not (scores is None):                                
                cnt = 0;
                for asg in scores[studentGit].keys():
                    theScore = scores[studentGit][asg] 
                    oldScore = scorehistory.getPrevScore(asg, studentGit)
                    if theScore != oldScore and not(oldScore is None):
                        theScore = 'WAS: ' + str(oldScore) + ' vs NOW: ' + str(theScore)
                    if cnt == 0:
                        tdData = theScore 
                    else: 
                        tdData = tdData + "</td><td>" +theScore
                    cnt = cnt + 1


            #def     printTR(  display,            codeURL, liveDisplay, liveURL, stuReport):
            stuRow = printTR(stuName, stuCode, stuSite, stuSite, stuReport, tdData )
            file.write(stuRow)
            
        file.write("</table></body><html>")
    return reportFile


def printToReport(log_list, message):
    print(message)
    log_list.append(message)
    
#writeStudentResultReport(student[2], projName, REPORT_DIR , studentReport)
def writeStudentResultReport(student, project, out_dir, log_data):
    reportFile = out_dir+"/" + projName + "/" +student + "." + project + "_results.html"
    with open(reportFile , "w") as file_obj:
        today = str(date.today())
        file_obj.write("<html><head><title>"+project+" status</title></head><body>\n")
        file_obj.write("Run date: " + today+"\n<br>")
        file_obj.write("Student User: "+ student+"\n<br>")
        file_obj.write("Project: " + project+"\n<br>\n<pre>\n")
        for logLine in log_data:
            file_obj.write(logLine +"\n")

        file_obj.write("\n</pre></body></html>")
        file_obj.close()
    return   projName + "/" +student + "." + project + "_results.html"


def checkClean(studentProjectDirectory, studentReport, studentWorkingDirectory):
    if not OK_TO_REUSE:
        if os.path.exists(studentProjectDirectory):
            printToReport(studentReport, "[CLEANUP] Removing project dir: " + studentProjectDirectory)        
            Popen( ['rm','-rf', stuProj] , cwd=studentWorkingDirectory)
        else:
            printToReport(studentReport, "[FRESH & CLEAN] @ " + studentProjectDirectory)
    else:
        if os.path.exists(studentProjectDirectory):
            printToReport(studentReport, "[REUSING WORK]: " + studentProjectDirectory)
        else:
            printToReport(studentReport, "[PRE-WARN]: Expected non-empty: " + studentProjectDirectory)   
    time.sleep(1.5)


def syncGitBase(projName, studentGithubUser, studentReport, studentWorkingDirectory):
    try:
        stuCode = makeProjURL(HTTPS_STR+GITHUB_PROJ_BASE_URL, projName, studentGithubUser)
        printToReport(studentReport, "[Attempting DL:" + stuCode + ".git]")        
        gitURL = HTTPS_STR + sysUser + ":" + sysPwd + "@" + makeProjURL(GITHUB_PROJ_BASE_URL, projName, studentGithubUser)+".git"

        output = subprocess.check_output( ['git','clone', gitURL] , cwd=studentWorkingDirectory, 
                    stderr=subprocess.STDOUT)        
        printToReport(studentReport, output.decode("utf-8").replace("\n", "\n\t"))
        printToReport(studentReport, "[GITWORK DONE]")
    except:
        print("Unable to sync for student: " + studentGithubUser + " for project: " + projName)

def tryCompile( studentReport, chapterDir, javaFile):
    error_code = 0
    printToReport(studentReport, "[COMPILING] " + javaFile)
    
    if os.path.isfile(chapterDir+'/'+ javaFile):

        p = Popen(['javac', javaFile], cwd=chapterDir, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        output = p.communicate()[0]
        if p.returncode != 0: 
            printToReport(studentReport, 
                "\t[ERROR] javac failed " + javaFile + " " + output.decode("utf-8").replace("\n", "\n\t"))
            error_code = 1
        else:
            printToReport(studentReport, "\t[SUCCESSFUL COMPILE] " + javaFile)
    else:
        printToReport(studentReport, "\t[ERROR] Missing Compile Target:" + javaFile)
        error_code = 2

    return error_code

def tryRun( studentReport, chapterDir, target):
    error_code = 0
    #try running
    javaClass = target + ".class"
    if os.path.isfile(chapterDir+'/'+ javaClass):
        printToReport(studentReport, "[RUNNING] " + target + "\n-->")
        p = Popen(['java', target], cwd=chapterDir,
                    stdout=PIPE, stdin=PIPE, stderr=PIPE)                            
        stdout_data = p.communicate(input=b'13\n')

        if p.returncode != 0: 
            printToReport(studentReport, "\t[ERROR] Runtime Error @ java " + target + "\n" +  
                stdout_data[0].decode("utf-8").replace("\n", "\n\t") )
            error_code = 3
        else:
            printToReport(studentReport, stdout_data[0].decode("utf-8").replace("\n", "\n\t"))
            printToReport(studentReport, "<--\n\t[OUTPUT OK]\n" )
    else:
        error_code = 1

    return error_code


def copyTest(TESTS_DIR, chapterDir, testTarget):
    javaFile = testTarget + ".java"
    if os.path.isfile(TESTS_DIR+'/'+ javaFile):
        copyfile(TESTS_DIR+'/'+javaFile, chapterDir + "/" + javaFile )


def handle_think_java( stuProjDir, studentReport, studentGithubUser ):
    #Chapter assignments
    ch2Descriptor = {
        "assignment_dir": "chapter2",
        "targets" : ["Date", "Time"], #Files to look for
        "score" : 0.4 ,              #weight for the assignment
        "checkWith": "COMPILES"      #How to verify assignment
        }

    ch3Descriptor = {
        "assignment_dir": "chapter3",
        "targets" : ["Exercise3", "Exercise4"], #Files to look for
        "score" : 0.4 ,              #weight for the assignment
        "checkWith": "COMPILES"      #How to verify assignment
    }

    ch4Descriptor = {
        "assignment_dir": "chapter4",
        "targets" : ["Multadd"], #Files to look for
        "score" : 0.4 ,              #weight for the assignment
        "checkWith": "COMPILES"      #How to verify assignment
    }


    ch6Descriptor = {
        "assignment_dir": "chapter6",
        "targets" : [("Exercise4","Ch6Ex4"), ("Exercise5","Ch6Ex5")], #Files to look for
        "score" : 0.4 ,              #weight for the assignment
        "checkWith": "TEST",      #How to verify assignment     
    }

    swetterCise1 = {
        "assignment_dir": "chapter6",
        "targets" : [("Swettercise1", "SwetterciseTest")], #Files to look for
        "score" : 0.4 ,              #weight for the assignment
        "checkWith": "TEST",        
    }

    ch7DescriptorA = {
        "assignment_dir": "chapter7",
        "targets" : [("Exercise3","TestCh7Ex3"), ("Exercise4","TestCh7Ex4")], #Files to look for
        "score" : 0.4 ,              #weight for the assignment
        "checkWith": "TEST",      #How to verify assignment         
    }

    ch7DescriptorB = {
        "assignment_dir": "chapter7",
        "targets" : [("Exercise5","TestCh7Ex5"), ("Exercise6","TestCh7Ex6"), ("Exercise8", "TestCh7Ex8")], #Files to look for
        "score" : 0.4 ,              #weight for the assignment
        "checkWith": "TEST",      #How to verify assignment         
    }


    #Assignments are collection of chapter assignments
    think_java_assignments = {
        "Think Java: Ch2-ch4" : {   #<-- key, value is map 
            "work": [ch2Descriptor, ch3Descriptor, ch4Descriptor],
            "enabled": True,
            "desc": "HW1, Ch2-Ch4" },

        "Think Java: Ch6" : {   #<-- key, value is map 
            "work": [ch6Descriptor],
            "enabled": True,
            "desc": "HW2, Ch 6" },

        "Swettercise1" : {   #<-- key, value is map 
            "work": [swetterCise1],
            "enabled": True,
            "desc": "HW3: Third HW Assignment, Swettercise. Assigned with Chapter6 work" },

        " Think Java: Ch7 - pt1 " : {   #<-- key, value is map 
            "work": [ch7DescriptorA],
            "enabled": True,
            "desc": "HW4: Fourth HW Assignment, Ch7 Ex3 & 4" },

        " Think Java: Ch7 - pt2 " : {   #<-- key, value is map 
            "work": [ch7DescriptorB],
            "enabled": True,
            "desc": "HW4: Fith HW Assignment, Ch7 Ex5, 6, 8" },

    }

    assign_to_score = {}
    for key in think_java_assignments.keys():
        assignment = think_java_assignments[key]
        if not assignment["enabled"]:
            continue

        printToReport(studentReport, "\n<hr>")
        printToReport(studentReport, "\n<b>[Assignment]  >" + key + "< </b>")
        printToReport(studentReport, "  [DESC] " + think_java_assignments[key]["desc"])
        
        asg_score = 1.0 
        assignmentWeight = 1.0/len(assignment["work"])
        for chapterWork in assignment["work"]:
            #a chapterWork is a chDescriptor, e.g. ch2ch2Descriptor
            #so chapterWrok is a dictionary
            chapter = chapterWork["assignment_dir"]
            printToReport(studentReport, "\n*[BEGIN " + chapter + "]")
            
            #This directory should exist if code has been submitted to git
            chapterDir = stuProjDir + "/" + chapter
            if chapterWork["checkWith"] == "COMPILES":
                printToReport(studentReport,    "  [EXPECTING TARGETS] " + str(chapterWork['targets']) + "]")
            else:                
                printToReport(studentReport,    "  [EXPECTING TARGETS] " + str([ t[0] for t in chapterWork['targets'] ]) )

            if os.path.exists(chapterDir):
                target_errors = {}
                for target in chapterWork['targets']:
                    errorCode = 0
                    deductions = 0
                    #If "checkWith" is test, use the tuple value    
                    targetName = target
                    if chapterWork["checkWith"] == "TEST":                        
                        targetName = target[0]

                    testTarget = target[1]
                    javaFile = targetName + ".java"
                    
                    #So i goofed, if this is targetName == 'Swettercise'
                    # then check if Swettercise1 (with the nubmer) exisits
                    if os.path.isfile(chapterDir+'/'+ javaFile):
                        errorCode = tryCompile(studentReport, chapterDir, javaFile)
                    elif targetName == "Swettercise1":
                        # One off fix for my own mistake in assigning the wrong classname
                        if os.path.isfile(chapterDir+'/Swettercise.java'):
                            errorCode = tryCompile(studentReport, chapterDir, 'Swettercise.java')
                        else:
                            errorCode = 2
                    else:
                        errorCode = 2

                    if chapterWork["checkWith"] == "COMPILES" and errorCode == 0:
                        errorCode = tryRun(studentReport, chapterDir, targetName) 

                    elif chapterWork["checkWith"] == "TEST" and errorCode == 0:
                        copyTest(TESTS_DIR, chapterDir, "TUtils")
                        copyTest(TESTS_DIR, chapterDir, testTarget)
                        printToReport(studentReport, "[TESTING WITH] " + testTarget)
                        results = javaRun.tryCompile(chapterDir, testTarget+".java")
                        for s in results[1]:
                            printToReport(studentReport, s)
                        
                        errorCode = results[0]
                        if results[0] == 0:                        
                            #otherwise, we compiled successfully, now try running
                            results = javaRun.tryRun(chapterDir, testTarget)
                            if results[0] == 0:
                                #It ran extract deductions
                                deductions = results[2]
                            #log the work
                            for s in results[1]:
                                printToReport(studentReport, s)
                                
                    target_errors[targetName] = (errorCode, deductions)



                target_summary = []
                for target in target_errors.keys():

                    tgErrorCode = target_errors[target][0]
                    if tgErrorCode == 0:
                        #Apply deductions to score
                        tgDeduction = target_errors[target][1]
                        asg_score = asg_score - tgDeduction
                        if tgDeduction < 0.01:
                            target_summary.append( target +  ": PASSED - EXCELLENT!" )
                        elif tgDeduction < 0.10:
                            target_summary.append( target +  ": PASSED - GOOD JOB BUT SOME EDGE CASE ERRORS WERE FOUND." )
                        elif tgDeduction < 0.3:
                            target_summary.append( target +  ": PASSED - BUT TEST CASES FOUND SOME ERRORS" )
                        else:
                            target_summary.append( target +  ": RAN - ERRORS NEED TO BE FIXED. You can to do better! :)" )
                    elif  tgErrorCode == 1:
                         target_summary.append( target + ": COMPILE ERROR (- {0:1.2f})".format(0.3 * assignmentWeight))
                         asg_score = asg_score - 0.3 * assignmentWeight
                    elif  tgErrorCode == 2:                        
                         target_summary.append( target + ": MISSING (- {0:1.2f})".format(0.5 * assignmentWeight))
                         asg_score = asg_score - 0.5 * assignmentWeight
                    elif  tgErrorCode == 3:
                         target_summary.append( target + ": RUNTIME ERROR (- {0:1.2f})".format(0.25 * assignmentWeight))
                         asg_score = asg_score - 0.25 * assignmentWeight

                printToReport(studentReport, "[SUMMARY] \n\t" + str(target_summary).replace(",", "\n\t"))    
            else:
                #mark this missing, and deduct
                printToReport(studentReport, "\t[ERROR] No chapter work for:" + chapter)
                asg_score = 0.25

            printToReport(studentReport, "[DONE "+chapter+"]")
        passing = asg_score > .8
        asg_score = max(0.0, asg_score)
        asg_score = "{0:1.2f}".format(asg_score)
        oldScore = scorehistory.setScore( key, studentGithubUser, asg_score)
        
        assign_to_score[key] = asg_score

        printToReport(studentReport, "[ASSIGNMENT DONE] " + key)
        
        
        if passing:
            asg_score = '<font color="green">'+asg_score+'</font>'

        printToReport(studentReport, "<b>          [SCORE] " + asg_score +"</b>")
    return assign_to_score


###
#
# Begin progam heavy lifting, loop over students, pull git, run work for project
#
##

gitPull()

scores = {}
for student in STUDENTS:
    studentReport = []
    studentGithubUser = student[2]

    printToReport(studentReport, "\n----------------------------------------------------------")
    printToReport(studentReport, "[STUDENT INIT] " + studentGithubUser)
    
    #Make the student directory in case it doesn't exist.
    stuProj = projName+"-"+studentGithubUser
    stuDir = OUTPUT_DIR + "/"+ studentGithubUser
    stuProjDir =  stuDir + "/"+ stuProj

    if not os.path.exists(stuDir):
        printToReport(studentReport, "[SETUP] Creating student dir:  " + stuDir)
        os.makedirs(stuDir)

    checkClean(stuProjDir, studentReport, stuDir) 

    #pull git if necissary
    if SHOULD_DL:
        if os.path.exists(stuDir):
            if not os.path.exists(stuProjDir):
                printToReport(studentReport, "[GITWORK]") 
                syncGitBase(projName, studentGithubUser, studentReport, stuDir)
                
            elif OK_TO_REUSE:
                printToReport(studentReport, "[GITWORK] Re-using code.")
            else:
                printToReport(studentReport, "[BANNANAS] Re-using code.")
            time.sleep(.5)
        else:
            printToReport(studentReport, "\t[ERROR] Unable able to proceed, no student directory: " + stuDir)
            sys.exit(0)


    if projName == 'think-java':
        scores[studentGithubUser] = handle_think_java(stuProjDir, studentReport, studentGithubUser)
        reportFile = writeStudentResultReport(student[2], projName, REPORT_DIR , studentReport)
        stu_to_report[ studentGithubUser ] = reportFile
            #end of each student

        
#end of work, save results to the internet

# Delete all the temp work (probably shoudl parameterize this)
Popen( ['rm','-rf', OUTPUT_DIR] )

if projName == 'think-java':
    print("Report created for " + 'think-java' )
    reportFile = createClassReport(projName, stu_to_report, None, None) 
    
    #so scores should look like {'stu name': {'assignment name': score}}
    createClassReport(projName, stu_to_report, None, scores) 
    scorehistory.save(scoreHistory)
    saveReportToGit(stu_to_report, reportFile)
    
elif projName in ['cs-portfolio', 'coat-of-arms', 'lightning', 'dice', 'chemotaxis']:
    print("Report created for " + 'cs-portfolio' )
    createClassReport(projName, stu_to_report, GITHUB_DEMO_BASE_URL, None) 
    
    sys.exit(0)

else:
    print("TODO: Should implement other project: " + projName)
    #todo: need to update
#    reportFile = createClassReport(projName, stu_to_report, None, None)

    #so scores should look like {'stu name': {'assignment name': score}}
    # createClassReport(projName, stu_to_report, None, scores) 
    # scorehistory.save(scoreHistory)
    # saveReportToGit(stu_to_report, reportFile)

