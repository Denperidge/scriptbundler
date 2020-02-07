from os import path

class Translator:
    def __init__(self, bat_to_goal, ps_to_goal, sh_to_goal):
        self.templates = dict([(".bat", bat_to_goal), (".ps1", ps_to_goal), (".sh", sh_to_goal)])
    
    def convertfrom(self, oldcommand, sourceext):
        usedTemplate = self.templates[sourceext]

        replacer = usedTemplate.replacer
        if type(replacer) is str:  # If one replacer
            parsedoldcommand = oldcommand.replace('"', replacer)
        elif type(replacer) is list:  # If multiple replacers
            parsedoldcommand = oldcommand
            for replacerer in replacer:
                parsedoldcommand = parsedoldcommand.replace(replacerer[0], replacerer[1])
        else:  # If no replacer
            parsedoldcommand = oldcommand

        newcommand = usedTemplate.formatstring.format(parsedoldcommand)
        return newcommand

class Template:
    def __init__(self, formatstring, replacer=None):
        self.formatstring = formatstring
        self.replacer = replacer


# Templates to convert from x to:
# cmd.exe (.bat)
# OS: Windows only
bat = Translator(
    Template('{0}'),  # bat -> bat
    Template('powershell -Command "{0}"', '\\"'),  # ps -> bat
    Template('"%ProgramFiles%/Git/bin/sh.exe" -c "{0}"', '\\"')  # sh -> bat
    )

# Templates to convert from x to:
# PowerShell (.ps1)
# OS: Windows only
ps = Translator(
    Template('cmd.exe /c "{0}"', '$([char]34)'),  # bat -> ps
    Template('{0}'),  # ps -> ps
    Template('& "$($Env:ProgramFiles)/Git/bin/sh.exe" "-c" \'{0}\'', [('"', '\\"'), ("'", "''")])  # sh -> ps
    )

# Templates to convert from x to:
# Bash (.sh)
# OS: universal
sh = Translator(
    Template('cmd.exe /c "{0}"', '\\"'),  # bat -> sh
    Template('powershell -Command "{0}"', '\\"'),  # ps -> sh
    Template('{0}')  # sh -> sh
    )


def convert(scriptname, goal):
    # Extension of script that will be translated
    scriptext = path.splitext(scriptname)[1]

    newlines = []
    if goal == ".bat":
        template = bat 
    elif goal == ".ps1":
        template = ps
    elif goal == ".sh":
        template = sh

    with open(scriptname, "r") as script:
        oldlines = script.readlines()
        
        for oldline in oldlines:
            newline = template.convertfrom(oldline, scriptext)
            if not newline.endswith("\n"):
                newline += "\n"

            newlines.append(newline)
    return newlines