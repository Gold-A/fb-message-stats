import sys
import json
from pprint import pprint
import message as M
import reactionGraph as RG
import person as P
import string
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

    messagesSentHist = group.messagesSentHist()

    reactionGraph = RG.ReactionGraph(group.allMessages())

    for k, v in M.REACTION_MAP.iteritems():
        print("\n")
        print("Most %s" % v)
        reactionGraph.printReaction("received", v)
        print("\n")
        print("%s received by percentage" % v)
        reactionGraph.printReactionNormalized("received", messagesSentHist, v)

    for k, v in M.REACTION_MAP.iteritems():
        print("\n")
        print("Gave the most %s" % v)
        reactionGraph.printReaction("given", v)
    print("\n")



main()


