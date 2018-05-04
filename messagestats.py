import sys
import json
from pprint import pprint
import message as m
import reactionGraph as rg


def messagesSent(msgs):
    hist = {}
    for msg in msgs:
        sender = msg.getSender()
        if sender in hist:
            hist[sender] += 1
        else:
            hist[sender] = 1
    return hist


def main():
    print(sys.argv[1])
    messagesData = {}
    with open(sys.argv[1]) as data_file:
        messagesData = json.load(data_file)

    people = messagesData["participants"]

    msgs = []
    for msgJson in messagesData["messages"]:
        msgs.append(m.Message(msgJson))

    messagesSentHist = messagesSent(msgs)
    print("Most Talkative")
    for sender, count in sorted(messagesSentHist.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        print("%s: %s" % (sender, count))

    reactionGraph = rg.ReactionGraph(msgs)

    for k, v in m.REACTION_MAP.iteritems():
        print("\n")
        print("Most %s" % v)
        reactionGraph.printReaction("received", v)
        print("\n")
        print("%s received by percentage" % v)
        reactionGraph.printReactionNormalized("received", messagesSentHist, v)

    for k, v in m.REACTION_MAP.iteritems():
        print("\n")
        print("Gave the most %s" % v)
        reactionGraph.printReaction("given", v)


main()


