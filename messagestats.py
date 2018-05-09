import sys
import json
from pprint import pprint
from group import Group

def main():
    print(sys.argv[1])
    messagesData = {}
    with open(sys.argv[1]) as data_file:
        messagesData = json.load(data_file)

    group = Group(messagesData["messages"])

    print("~~People~~")
    for person in group.getMembers():
        print(person.getName())
    print("\n")

    group.printStats()

    if len(sys.argv) == 3:
        group.outputCSV(sys.argv[2])

main()


