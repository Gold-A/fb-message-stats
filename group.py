from message import Message
from person import Person
from reactionGraph import ReactionGraph
import datetime

class Group:
    def __init__(self, allMessages):
        self._members = []
        self._membersByName = {}
        self._allMessages = []
        self._messageHist = {}
        self._emojiHist = {}
        for msgJson in allMessages:
            if msgJson["type"] != "Generic" and msgJson["type"] != "Share":
                continue
            message = Message(msgJson)
            self._allMessages.append(message)
            senderName = message.getSender()
            if senderName not in self._membersByName:
                newPerson = Person(senderName)
                self._membersByName[senderName] = newPerson
                self.addMember(newPerson)

            self._membersByName[senderName].addMessage(message)

        for name, person in self._membersByName.iteritems():
            self._messageHist[name] = person.messageCount()


    def addMember(self, person):
        self._members.append(person)
        self._membersByName[person.getName()] = person


    def getMembers(self):
        return self._members


    def emojiHist(self):
        if len(self._emojiHist) > 0:
            return self._emojiHist

        for person in self._members:
            for emoji, count in person.emojiSent():
                if emoji in self._emojiHist:
                    self._emojiHist[emoji] += count
                else:
                    self._emojiHist[emoji] = count
        return self._emojiHist


    def printStats(self):
        intStats = [
            {
                "title" : "Most Spammy (messages)",
                "func" : lambda x: x.messageCount()
            },
            {
                "title" : "Most Talkative (words)",
                "func" : lambda x: x.wordCount()
            },
            {
                "title" : "GIFs Sent",
                "func" : lambda x: x.numGifsSent()
            },
            {
                "title" : "Photos Sent",
                "func" : lambda x: x.numPhotosSent()
            },
            {
                "title" : "Videos Sent",
                "func" : lambda x: x.numVideosSent()
            },
            {
                "title" : "Links Sent",
                "func" : lambda x: x.numLinksSent()
            },
        ]

        stats = [
            {
                "title" : "Average words / message",
                "func" : self.printAverageWordsPerMessage
            },
            {
                "title" : "Top Words",
                "func" : self.printTopWords
            },
            {
                "title" : "Emoji",
                "func" : self.printEmoji
            },
            {
                "title" : "Hour",
                "func" : self.printHour
            },
            {
                "title" : "Week",
                "func" : self.printWeek
            },
            {
                "title" : "Month",
                "func" : self.printMonth
            },
            {
                "title" : "FIRST MESSAGE",
                "func" : self.printFirstMessage
            },
            {
                "title" : "Total Emojis",
                "func" : self.printTotalEmoji
            },

        ]

        for stat in stats:
            self.printStat(stat["title"], stat["func"])

        for stat in intStats:
            self.printIntegerStatSorted(stat["title"], stat["func"])

        reactionGraph = ReactionGraph(self._allMessages)
        reactionGraph.printStats(self._messageHist)


    def printStat(self, title, fnc):
        print("~~%s~~" % title)
        fnc()
        print("\n")


    def printIntegerStatSorted(self, title, fnc):
        print("~~%s~~" % title)
        for person in sorted(self._members, key=fnc, reverse=True):
            name = person.getName()
            print("%s: %s" % (name, fnc(person)))
        print("\n")



    def printAverageWordsPerMessage(self):
        for person in sorted(self._members, key=lambda x: (x.numWordsSent() / x.numMessagesSent())):
            name = person.getName()
            print("%s: %.2f" % (name, float(person.numWordsSent()) / person.numMessagesSent()))


    def printTotalEmoji(self):
        for emoji, count in sorted(self.emojiHist().iteritems(), key=lambda (k, v): (v, k), reverse=True)[:20]:
            print("%s, %d" % (emoji, count))


    def printTopWords(self):
        for person in self._members:
            name = person.getName()
            print("%s: %s" % (name, person.topWords(5)))


    def printEmoji(self):
        for person in self._members:
            name = person.getName()
            print("%s: %s" % (name, person.emojiSent()))


    def printWeek(self):
        print("SENDER\tSUN\tMON\tTUE\tWED\tTHU\tFRI\tSAT")
        for person in self._members:
            name = person.getName()
            week = person.weekHistogram()
            print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (name.split()[0], week["Su"], week["M"], week["Tu"], week["W"], week["Th"], week["F"], week["Sa"]))


    def printMonth(self):
        print("SENDER\tJ\tF\tM\tA\tM\tJ\tJ\tA\tS\tO\tN\tD")
        for person in self._members:
            name = person.getName()
            month = person.monthHistogram()
            monthStr = name.split()[0]
            for k, v in month.iteritems():
                monthStr += ("\t" + str(v))
            print monthStr

        
    def printHour(self):
        hourheader = "SENDER"
        for i in range(24):
            hourheader += "\t" + str(i)
        print hourheader
        for person in self._members:
            name = person.getName()
            hour = person.hourHistogram()
            hourStr = name.split()[0]
            for k, v in hour.iteritems():
                hourStr += ("\t" + str(v))
            print hourStr


    def printFirstMessage(self):
        for person in self._members:
            name = person.getName()
            print("%s: %s %s" % (name, person.getDateFirstMessage(), person.getFirstMessage()))
