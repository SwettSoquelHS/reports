import sys, os, time, subprocess, getpass
from datetime import date
from subprocess import Popen, PIPE, STDOUT
import loadStudents
import argparse


# Stuff we need, joy.
PARSER = argparse.ArgumentParser()
PARSER.add_argument("project", help="Github project to pull.")
PARSER.add_argument("-a", "--assignment", help="Assignment within the project.")
PARSER.add_argument("-s", "--student", help="Only on the student specified.")
args = PARSER.parse_args()


#If a specific student was specified then only that student will be run
STUDENTS = loadStudents.getStudents(args.student)


#github URL pattern
#https://github.com/SwettSoquelHS/github-proj-stuGuthubuser
#https://github.com/SwettSoquelHS/github-proj-stuGuthubuser.git
HTTPS_STR = "https://"
GITHUB_PROJ_BASE_URL= "github.com/SwettSoquelHS/"

#gitHubDempURL
GITHUB_DEMO_BASE_URL = "https://swettsoquelhs.github.io/"

OUTPUT_DIR = './stuwork'
REPORT_DIR = './stureports'
 

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
    print("[FINALIZING] Running " + projName + " summary...")
    reportFile = projName + ".html"
    if not (scores is None):
        reportFile = "admin-" + reportFile

    reportFile = REPORT_DIR + "/" + reportFile


    with open(reportFile , "w") as file:
        file.write("<html><head><title>"+projName + " class report</title></head><body>")
        file.write("<table><tr><td>Student Code Base</td><td>Live Demo</td> <td>Report</td>")
        if scores is None:
            file.write(" </tr>")
        else:
            file.write("<td> Score Value </td></tr>")

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
            if not (scores is None):
                theScore = scores[student[2]].values()


            #def     printTR(  display,            codeURL, liveDisplay, liveURL, stuReport):
            stuRow = printTR(stuName, stuCode, stuSite, stuSite, stuReport, theScore )
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
    stuCode = makeProjURL(HTTPS_STR+GITHUB_PROJ_BASE_URL, projName, studentGithubUser)
    printToReport(studentReport, "[Attempting DL:" + stuCode + ".git]")        
    gitURL = HTTPS_STR + sysUser + ":" + sysPwd + "@" + makeProjURL(GITHUB_PROJ_BASE_URL, projName, studentGithubUser)+".git"

    output = subprocess.check_output( ['git','clone', gitURL] , cwd=studentWorkingDirectory, 
                stderr=subprocess.STDOUT)        
    printToReport(studentReport, output.decode("utf-8").replace("\n", "\n\t"))
    printToReport(studentReport, "[GITWORK DONE]")

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
            printToReport(studentReport, stdout_data[1].decode("utf-8").replace("\n", "\n\t"))
            printToReport(studentReport, "<--\n\t[OUTPUT OK]\n" )
    else:
        error_code = 1

    return error_code


def handle_think_java( stuProjDir, studentReport ):
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
        "targets" : ["Exercise4", "Exercise5"], #Files to look for
        "score" : 0.4 ,              #weight for the assignment
        "checkWith": "COMPILES"      #How to verify assignment
    }

    swetterCise1 = {
        "assignment_dir": "chapter6",
        "targets" : ["Swettercise"], #Files to look for
        "score" : 0.4 ,              #weight for the assignment
        "checkWith": "COMPILES"      #How to verify assignment
    }



    #Assignments are collection of chapter assignments
    think_java_assignments = {
        "asignment_1" : {   #<-- key, value is map 
            "work": [ch2Descriptor, ch3Descriptor, ch4Descriptor],
            "enabled": True,
            "desc": "First Assignment, Ch2-Ch4" },

        "asignment_2" : {   #<-- key, value is map 
            "work": [ch6Descriptor],
            "enabled": False,
            "desc": "Second Assignment, Ch 6" },

        "asignment_3" : {   #<-- key, value is map 
            "work": [swetterCise1],
            "enabled": False,
            "desc": "Third Assignment, Swettercise" },

    }

    assign_to_score = {}
    for key in think_java_assignments.keys():
        asignment = think_java_assignments[key]
        if not asignment["enabled"]:
            continue

        printToReport(studentReport, "[Assignment]  >" + key + "<")
        printToReport(studentReport, "  [DESC] " + think_java_assignments[key]["desc"])

        printToReport(studentReport, "\n*[BEGIN " + chapter + "]")
        asg_score = 1.0 
        for chapterWork in asignment["work"]:
            #a chapterWork is a chDescriptor, e.g. ch2ch2Descriptor
            #so chapterWrok is a dictionary
            chapter = chapterWork["assignment_dir"]
            printToReport(studentReport, "\n*[BEGIN " + chapter + "]")
            
            #This directory should exist if code has been submitted to git
            chapterDir = stuProjDir + "/" + chapter

            printToReport(studentReport,    "  [EXPECTING TARGETS] " + str(chapterWork['targets']) + "]")
            if os.path.exists(chapterDir):
                target_errors = {}
                for target in chapterWork['targets']:
                    # chapter/target looks like ./stuwork/studentName/think-java-studentName/chapter2
                    javaFile = target + ".java"
                    target_errors[target] = tryCompile(studentReport, chapterDir, javaFile)

                    if chapterWork["checkWith"] == "COMPILES":
                        if 3 == tryRun(studentReport, chapterDir, target):
                            target_errors[target] = 3
                    elif chapterWork["checkWith"] == "TEST":
                        tests = chapterWork["checkWith"]

                target_summary = []
                for target in target_errors.keys():
                    if target_errors[target] == 0:
                        target_summary.append( target +  ": PASS" )
                    elif  target_errors[target] == 1:
                         target_summary.append( target + ": COMPILE ERROR" )
                         asg_score = asg_score - 0.1
                    elif  target_errors[target] == 2:
                         target_summary.append( target + ": MISSING" )
                         asg_score = asg_score - 0.2
                    elif  target_errors[target] == 3:
                         target_summary.append( target + ": RUNTIME ERROR" )
                         asg_score = asg_score - 0.05

                printToReport(studentReport, "[SUMMARY] " + str(target_summary))    
            else:
                #mark this missing, and deduct
                printToReport(studentReport, "\t[ERROR] No chapter work for:" + chapter)
                asg_score = asg_score - chapterWork['score']

            printToReport(studentReport, "[DONE "+chapter+"]")

        asg_score = max(0.0, asg_score)
        
        printToReport(studentReport, "[ASSIGNMENT DONE] " + key)
        printToReport(studentReport, "          [SCORE] {0:1.2f}".format(asg_score))
        assign_to_score[key] = "{0:1.2f}".format(asg_score)
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
        scores[studentGithubUser] = handle_think_java(stuProjDir, studentReport)
        reportFile = writeStudentResultReport(student[2], projName, REPORT_DIR , studentReport)
        stu_to_report[ studentGithubUser ] = reportFile
            #end of each student

        
#end of work, save results to the internet

Popen( ['rm','-rf', OUTPUT_DIR] )

if projName in ['think-java']:
    reportFile = createClassReport(projName, stu_to_report, None, None) 

    #so scores should look like {'stu name': {'assignment name': score}}
    createClassReport(projName, stu_to_report, None, scores) 



    saveReportToGit(stu_to_report, reportFile)
    
    
    
else:
    #todo: need to update
    reportFile = createClassReport(projName, stu_to_report, None, None)

    #so scores should look like {'stu name': {'assignment name': score}}
    createClassReport(projName, stu_to_report, None, scores) 
    saveReportToGit(stu_to_report, reportFile)

