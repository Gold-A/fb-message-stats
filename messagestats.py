import sys
import json
from pprint import pprint
import message as M
import reactionGraph as RG
import person as P
import string

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

    people = {}
    for personName in messagesData["participants"]:
        people[str(personName)] = P.Person(personName)

    print("~~People~~")
    for _, person in people.iteritems():
        print(person.getName())
    print("\n")

    allMessages = []
    for msgJson in messagesData["messages"]:
        if msgJson["type"] != "Generic" and msgJson["type"] != "Share":
            continue
        message = M.Message(msgJson)
        allMessages.append(message)
        senderName = message.getSender()
        if senderName not in people:
            people[senderName] = P.Person(senderName)
        people[senderName].addMessage(message)


    messagesSentHist = messagesSent(allMessages)
    print("~~Most Talkative~~")
    for sender, count in sorted(messagesSentHist.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        print("%s: %s" % (sender, count))
    print("\n")

    print("~~Average words / message~~")
    for name, person in sorted(people.iteritems(), key=lambda (k, v): (v.numWordsSent() / v.numMessagesSent(), k)):
        print("%s: %.2f" % (name, float(person.numWordsSent()) / person.numMessagesSent()))
    print("\n")

    print ("~~Top Words~~")
    for name, person in people.iteritems():
        print("%s: %s" % (name, person.topWords(5)))
    print("\n")

    reactionGraph = RG.ReactionGraph(allMessages)

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

    print("~~Week~~")
    print("SENDER\tSUN\tMON\tTUE\tWED\tTHU\tFRI\tSAT")
    for name, person in people.iteritems():
        week = person.weekHistogram()
        print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (name.split()[0], week["Su"], week["M"], week["Tu"], week["W"], week["Th"], week["F"], week["Sa"]))
    print("\n")

    print("~~Month~~")
    print("SENDER\tJ\tF\tM\tA\tM\tJ\tJ\tA\tS\tO\tN\tD")
    for name, person in people.iteritems():
        month = person.monthHistogram()
        monthStr = name.split()[0]
        for k, v in month.iteritems():
            monthStr += ("\t" + str(v))
        print monthStr
    print("\n")

    print("~~Hour~~")
    hourheader = "SENDER"
    for i in range(24):
        hourheader += "\t" + str(i)
    print hourheader
    for name, person in people.iteritems():
        hour = person.hourHistogram()
        hourStr = name.split()[0]
        for k, v in hour.iteritems():
            hourStr += ("\t" + str(v))
        print hourStr
    print("\n")

main()


