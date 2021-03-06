from message import REACTION_MAP

class ReactionGraph:
    def __init__(self, msgs):
        self._reactsByReactor = {}
        self._reactsByReactee = {}
        for msg in msgs:
            for reaction in msg.getReactions():
                self.addToReactionGraph(reaction)

    def getReactsByReactee(self):
        return self._reactsByReactee


    def getReactsByReactor(self):
        return self._reactsByReactor


    def totalReacts(self, graph, usr, reaction):
        count = 0
        if usr not in graph:
            return count
        for s, reactions in graph[usr].iteritems():
            if reaction in reactions:
                count += reactions[reaction]
        return count


    def totalReactsReceived(self, speaker, reaction):
        return self.totalReacts(self._reactsByReactee, speaker, reaction)


    def totalReactsSent(self, reactor, reaction):
        return self.totalReacts(self._reactsByReactor, reactor, reaction)


    def addToReactionGraph(self, reactionObj):
        self.addToReceiverGraph(reactionObj)
        self.addToReactorGraph(reactionObj)


    def addToReactorGraph(self, reactionObj):
        reactor = reactionObj.getReactor()
        speaker = reactionObj.getSpeaker()
        reaction = reactionObj.getReaction()
        if reactor not in self._reactsByReactor:
            self._reactsByReactor[reactor] = {}
        if speaker not in self._reactsByReactor[reactor]:
            self._reactsByReactor[reactor][speaker] = {}
        if reaction not in self._reactsByReactor[reactor][speaker]:
            self._reactsByReactor[reactor][speaker][reaction] = 1
        else:
            self._reactsByReactor[reactor][speaker][reaction] += 1


    def addToReceiverGraph(self, reactionObj):
        reactor = reactionObj.getReactor()
        speaker = reactionObj.getSpeaker()
        reaction = reactionObj.getReaction()
        if speaker not in self._reactsByReactee:
            self._reactsByReactee[speaker] = {}
        if reactor not in self._reactsByReactee[speaker]:
            self._reactsByReactee[speaker][reactor] = {}
        if reaction not in self._reactsByReactee[speaker][reactor]:
            self._reactsByReactee[speaker][reactor][reaction] = 1
        else:
            self._reactsByReactee[speaker][reactor][reaction] += 1


    def printStats(self, messagesSentHist):
        for k, v in REACTION_MAP.iteritems():
            print("Most %s" % v)
            self.printReaction("received", v)
            print("\n")
            print("%s received by percentage" % v)
            self.printReactionNormalized("received", messagesSentHist, v)

        for k, v in REACTION_MAP.iteritems():
            print("\n")
            print("Gave the most %s" % v)
            self.printReaction("given", v)
        print("\n")


    def printReaction(self, rg, reaction):
        for person, count in self.reactionNormalized(rg, None, reaction).iteritems():
            print("%s: %s" % (person, count))

    def printReactionNormalized(self, rg, hist, reaction):
        for person, count in self.reactionNormalized(rg, hist, reaction).iteritems():
            print("%s: %s" % (person, count))
    
    def reactionNormalized(self, rg, hist, reaction):
        graph = {}
        if rg == "received":
            graph = self._reactsByReactee
        elif rg == "given":
            graph = self._reactsByReactor
        reactionHist = {}
        for r, s in graph.iteritems():
            reactionHist[r] = self.totalReacts(graph, r, reaction)
        ret = {}
        if hist == None:
            for r, count in sorted(reactionHist.iteritems(), key=lambda (k,v): (v,k), reverse=True):
                if count > 0:
                    ret[r] = count
        else:
            for r, count in sorted(reactionHist.iteritems(), key=lambda (k,v): (float(v)/hist[k],k), reverse=True):
                if count > 0:
                    ret[r] = "%.2f%%" % (float(count*100)/hist[r])
        return ret


    def reactionsSentRecievedAndNormalizedByPerson(self, hist, person):
        stats = {}
        for _, reaction in REACTION_MAP.iteritems():
            stat = 0
            if person in self._reactsByReactee:
                stat = self.totalReacts(self._reactsByReactee, person, reaction)
            stats["%s_RECIEVED" % reaction] = stat

            stat = 0
            normalized = self.reactionNormalized("received", hist, reaction)
            if person in normalized:
                stat = normalized[person]
            stats["%s_RECIEVED_NORMALIZED" % reaction] = stat

            stat = 0
            if person in self._reactsByReactor:
                stat = self.totalReacts(self._reactsByReactor, person, reaction)
            stats["%s_GIVEN" % reaction] = stat
        return stats
