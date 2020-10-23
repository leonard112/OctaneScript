import sys
from interpreter import run

if len(sys.argv) == 1:
    run("repl")

elif sys.argv[1][-2] == '.' and sys.argv[1][-1] == 'o' :
    run(sys.argv[1])

elif sys.argv[1] == "-version" :
    metadata = open("resources/metadata.txt", "r")
    version = metadata.readline()
    print(version)

elif sys.argv[1] == "-help":
    help_info = open("resources/help.txt", "r")
    print(help_info.read())

else :
    raise Exception("Bad file extension.\n" +
        "Is your script an Octane script with the '.o' file extension?")