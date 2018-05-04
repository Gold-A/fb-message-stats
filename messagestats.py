import sys
import json
from pprint import pprint
import message as m

ReactsByReactor = {}
ReactsByReactee = {}

def totalReacts(graph, usr, reaction):
    count = 0
    for s, reactions in graph[usr].iteritems():
        if reaction in reactions:
            count += reactions[reaction]
    return count


def totalReactsReceived(speaker, reaction):
    return totalReacts(ReactsByReactee, speaker, reaction)


def totalReactsSent(reactor, reaction):
    return totalReacts(ReactsByReactor, reactor, reaction)


def addToReactionGraph(reactionObj):
    addToReceiverGraph(reactionObj)
    addToReactorGraph(reactionObj)


def addToReactorGraph(reactionObj):
    reactor = reactionObj.getReactor()
    speaker = reactionObj.getSpeaker()
    reaction = reactionObj.getReaction()
    if reactor not in ReactsByReactor:
        ReactsByReactor[reactor] = {}
    if speaker not in ReactsByReactor[reactor]:
        ReactsByReactor[reactor][speaker] = {}
    if reaction not in ReactsByReactor[reactor][speaker]:
        ReactsByReactor[reactor][speaker][reaction] = 1
    else:
        ReactsByReactor[reactor][speaker][reaction] += 1


def addToReceiverGraph(reactionObj):
    reactor = reactionObj.getReactor()
    speaker = reactionObj.getSpeaker()
    reaction = reactionObj.getReaction()
    if speaker not in ReactsByReactee:
        ReactsByReactee[speaker] = {}
    if reactor not in ReactsByReactee[speaker]:
        ReactsByReactee[speaker][reactor] = {}
    if reaction not in ReactsByReactee[speaker][reactor]:
        ReactsByReactee[speaker][reactor][reaction] = 1
    else:
        ReactsByReactee[speaker][reactor][reaction] += 1


def reactionsSentAndReceived(msgs):
    for msg in msgs:
        for reaction in msg.getReactions():
            addToReactionGraph(reaction)


def messagesSent(msgs):
    hist = {}
    for msg in msgs:
        sender = msg.getSender()
        if sender in hist:
            hist[sender] += 1
        else:
            hist[sender] = 1
    return hist


def printReaction(rs, reaction):
    printReactionNormalized(rs, None, reaction)


def printReactionNormalized(rs, hist, reaction):
    graph = {}
    if rs == "r":
        graph = ReactsByReactee
    elif rs == "s":
        graph = ReactsByReactor
    reactionHist = {}
    for r, s in graph.iteritems():
        reactionHist[r] = totalReacts(graph, r, reaction)
    if hist == None:
        for r, count in sorted(reactionHist.iteritems(), key=lambda (k,v): (v,k), reverse=True):
            if count > 0:
                print("%s: %s" % (r, count))
    else:
        for r, count in sorted(reactionHist.iteritems(), key=lambda (k,v): (float(v)/hist[k],k), reverse=True):
            if count > 0:
                print("%s: %.2f%%" % (r, float(count*100)/hist[r]))


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

    reactionsSentAndReceived(msgs)

    for k, v in m.REACTION_MAP.iteritems():
        print("\n")
        print("Most %s" % v)
        printReaction("r", v)
        print("\n")
        print("%s received by percentage" % v)
        printReactionNormalized("r", messagesSentHist, v)

    for k, v in m.REACTION_MAP.iteritems():
        print("\n")
        print("Gave the most %s" % v)
        printReaction("s", v)


main()


