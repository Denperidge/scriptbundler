from os import path
from glob import glob
from convert import convert

workingdir = path.dirname(path.realpath(__file__))
inputdir = path.join(workingdir, "input")
inputscripts = []
selectedscripts = []
exts = [".sh", ".ps1", ".bat"]
output = ""
outputext = ""
outputpath = ""

for ext in exts:
    inputscripts += glob(path.join(inputdir, "*" + ext))
inputscripts.sort()

print("Valid extensions: {0}".format(exts))
while outputext not in exts:
    output = input("Write desired name for bundled script: ")
    outputext = path.splitext(output)[1]

outputpath = path.join(workingdir, "output", output)

def strSelectedScripts():
    string = ""
    for selectedscript in selectedscripts:
        string += path.basename(selectedscript) + ", "
    string = string.strip(", ")
    return string

addinginput = True
errormsg = ""
while addinginput:
    print()
    print(errormsg)
    print("Scripts: ")
    i = 0
    for script in inputscripts:
        print("\t[{0}] {1}".format(i, path.basename(script)))
        i += 1
    
    print()
    print("Script order: {0}".format(strSelectedScripts()))

    nextscriptindex = input("Insert index of next script (or press ENTER if you're finished): ")
    try:
        nextscriptindex = int(nextscriptindex)
        if inputscripts[nextscriptindex] and nextscriptindex != "":
            nextscript = inputscripts[nextscriptindex]
            selectedscripts.append(nextscript)
            inputscripts.remove(nextscript)
            errormsg = "{0} added!".format(path.basename(nextscript))
    except ValueError:
        if nextscriptindex == "":
            addinginput = False
        else:
            errormsg = "Insert a valid index ({0}-{1})".format(0, len(inputscripts) -1)
    except IndexError:
        errormsg = "Index out of range!"
    
print()
print()

translatedlines = []
# If goal is .bat, add echo off
if outputext == ".bat":
    translatedlines.append("@echo off\n\n")

for scriptname in selectedscripts:
    print("Converting script {0}".format(scriptname))
    convertedlines = convert(scriptname, outputext)
    translatedlines += convertedlines

with open(outputpath, "w") as outputfile:
    outputfile.writelines(translatedlines)

