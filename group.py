import message as M
import person as P

import datetime

class Group:
    def __init__(self, allMessages):
        self._members = []
        self._membersByName = {}
        self._allMessages = []
        self._messageHist = {}
        for msgJson in allMessages:
            if msgJson["type"] != "Generic" and msgJson["type"] != "Share":
                continue
            message = M.Message(msgJson)
            self._allMessages.append(message)
            senderName = message.getSender()
            if senderName not in self._membersByName:
                newPerson = P.Person(senderName)
                self._membersByName[senderName] = newPerson
                self.addMember(newPerson)

            self._membersByName[senderName].addMessage(message)

        for name, person in self._membersByName.iteritems():
            self._messageHist[name] = person.messageCount()


    def allMessages(self):
        return self._allMessages


    def messagesSentHist(self):
        return self._messageHist


    def addMember(self, person):
        self._members.append(person)
        self._membersByName[person.getName()] = person


    def getMembers(self):
        return self._members


    def printStats(self):
        self.printStat("Most Spammy (messages)", self.printMostMessages)
        self.printStat("Most Talkative (words)", self.printMostWords)
        self.printStat("Average words / message", self.printAverageWordsPerMessage)
        self.printStat("Top Words", self.printTopWords)
        self.printStat("Hour", self.printHour)
        self.printStat("Week", self.printWeek)
        self.printStat("Month", self.printMonth)
        self.printStat("FIRST MESSAGE", self.printFirstMessage)


    def printStat(self, title, fnc):
        print("~~%s~~" % title)
        fnc()
        print("\n")

    def printMostMessages(self):
        for person in sorted(self._members, key=lambda x: x.messageCount(), reverse=True):
            name = person.getName()
            print("%s: %s" % (name, person.messageCount()))


    def printMostWords(self):
        for person in sorted(self._members, key=lambda x: x.wordCount(), reverse=True):
            name = person.getName()
            print("%s: %s" % (name, person.wordCount()))


    def printAverageWordsPerMessage(self):
        for person in sorted(self._members, key=lambda x: (x.numWordsSent() / x.numMessagesSent())):
            name = person.getName()
            print("%s: %.2f" % (name, float(person.numWordsSent()) / person.numMessagesSent()))


    def printTopWords(self):
        for person in self._members:
            name = person.getName()
            print("%s: %s" % (name, person.topWords(5)))


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
