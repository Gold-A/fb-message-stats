import sys
import json
from pprint import pprint
import group as G

def main():
    print(sys.argv[1])
    messagesData = {}
    with open(sys.argv[1]) as data_file:
        messagesData = json.load(data_file)

    group = G.Group(messagesData["messages"])

    print("~~People~~")
    for person in group.getMembers():
        print(person.getName())
    print("\n")

    group.printStats()






main()


