import sys

import loadStudents

STUDENTS = loadStudents.getStudents()
# https://github.com/SwettSoquelHS/think-java-Fwuff547
# https://github.com/SwettSoquelHS/think-java-Fwuff547.git


def printTR(display, codeURL, liveDisplay, liveURL):
    result = '<tr><td><a href="' + codeURL + '">' + display + "</a></td>"
    if liveDisplay != 'N\A':
        result += '<td><a href="' + liveURL +'">' + liveURL + '</a></td></tr>'
    else:
        result += '<td> N\A </td></tr>'
    return result;

def makeProjURL(base, proj, user):
    return base + proj + "-" + user


# print(students)
if sys.argv[1] is None:
    sys.exit(1)

gitHubURL = "https://github.com/SwettSoquelHS/"
gitDemoURL = "https://swettsoquelhs.github.io/"
#    think-java-DrKiefer



projName = sys.argv[1]

#print(sys.argv[1])

print("<table><tr><td>Code Source</td><td>Live Demo</td></tr>")
for student in STUDENTS:
    stuCode = makeProjURL(gitHubURL, projName, student[2])
    stuSite = makeProjURL(gitDemoURL, projName, student[2]) 

    print(printTR(student[1], stuCode, stuSite, stuSite ))

print("</table>")



