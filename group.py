from message import Message, REACTION_MAP
from person import Person
from reactionGraph import ReactionGraph
import datetime
import csv


class Group:
    def __init__(self, allMessages):
        self._members = []
        self._membersByName = {}
        self._allMessages = []
        self._messageHist = {}
        self._emojiHist = {}
        self._messageTimeline = []
        self._earliestMessage = datetime.datetime.max
        self._messageTimelineByPerson = {}
        lastSender = ""
        numConsecutive = 1
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

            if message.getDate() < self._earliestMessage:
                self._earliestMessage = message.getDate()

            self._membersByName[senderName].addMessage(message)
            if senderName == lastSender:
                numConsecutive += 1
            elif lastSender in self._membersByName:
                self._membersByName[lastSender].addConsecutiveCount(numConsecutive)
                numConsecutive = 1
            lastSender = senderName
        self._membersByName[senderName].addConsecutiveCount(numConsecutive)

        self.setMessageTimeLine()

        for name, person in self._membersByName.iteritems():
            self._messageHist[name] = person.numMessagesSent()

    def setMessageTimeLine(self):
        if len(self._messageTimeline) == 0:
            for message in self._allMessages:
                day = (message.getDate() - self._earliestMessage).days
                name = message.getSender()
                self._messageTimeline.append((day, name))
                if day not in self._messageTimelineByPerson:
                    self._messageTimelineByPerson[day] = {}
                if name in self._messageTimelineByPerson[day]:
                    self._messageTimelineByPerson[day][name] += 1
                else:
                    self._messageTimelineByPerson[day][name] = 1

    def addMember(self, person):
        self._members.append(person)
        self._membersByName[person.getName()] = person

    def getMembers(self):
        return self._members

    def getMembersWithNames(self):
        return self._membersByName

    def emojiHist(self):
        if len(self._emojiHist) > 0:
            return self._emojiHist

        for person in self._members:
            for emoji, count in person.emojisSent():
                if emoji in self._emojiHist:
                    self._emojiHist[emoji] += count
                else:
                    self._emojiHist[emoji] = count
        return self._emojiHist

    def printStats(self):
        intStats = [
            {
                "title": "Most Spammy (messages)",
                "func": lambda x: x.numMessagesSent()
            },
            {
                "title": "Most Talkative (words)",
                "func": lambda x: x.wordCount()
            },
            {
                "title": "GIFs Sent",
                "func": lambda x: x.numGifsSent()
            },
            {
                "title": "Photos Sent",
                "func": lambda x: x.numPhotosSent()
            },
            {
                "title": "Videos Sent",
                "func": lambda x: x.numVideosSent()
            },
            {
                "title": "Links Sent",
                "func": lambda x: x.numLinksSent()
            },
        ]

        stats = [
            {
                "title": "Average words / message",
                "func": self.printAverageWordsPerMessage
            },
            {
                "title": "Top Words",
                "func": self.printTopWords
            },
            {
                "title": "Emoji",
                "func": self.printEmoji
            },
            {
                "title": "Hour",
                "func": self.printHour
            },
            {
                "title": "Week",
                "func": self.printWeek
            },
            {
                "title": "Month",
                "func": self.printMonth
            },
            {
                "title": "FIRST MESSAGE",
                "func": self.printFirstMessage
            },
            {
                "title": "Total Emojis",
                "func": self.printTotalEmoji
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
        for emoji, count in sorted(self.emojiHist().iteritems(), key=lambda (k, v): (v, k), reverse=True)[:10]:
            print("%s, %d" % (emoji, count))

    def printTopWords(self):
        for person in self._members:
            name = person.getName()
            print("%s: %s" % (name, person.topWords(5)))

    def printEmoji(self):
        for person in self._members:
            name = person.getName()
            print("%s: %s" % (name, person.emojisSent()))

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

    def outputCSV(self, outputFolder):
        with open(outputFolder + '/statsMonth.csv', 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(["SENDER","J","F","M","A","M","J","J","A","S","O","N","D"])
            for person in self._members:
                name = person.getName()
                month = person.monthHistogram()
                row = [name]
                for k, v in month.iteritems():
                    row.append(v)
                csvwriter.writerow(row)
            # Normalized as a percentage of total messages
            for person in self._members:
                name = person.getName()
                month = person.monthHistogram()
                row = [name]
                for k, v in month.iteritems():
                    row.append("%.2f" % (float(v * 100) / person.numMessagesSent()))
                csvwriter.writerow(row)
        with open(outputFolder + '/statsHour.csv', 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            header = ["SENDER"] + range(24)
            csvwriter.writerow(header)
            for person in self._members:
                name = person.getName()
                hour = person.hourHistogram()
                row = [name]
                for k, v in hour.iteritems():
                    row.append(v)
                csvwriter.writerow(row)
            for person in self._members:
                name = person.getName()
                hour = person.hourHistogram()
                row = [name]
                for k, v in hour.iteritems():
                    row.append("%.2f" % (float(v * 100) / person.numMessagesSent()))
                csvwriter.writerow(row)
        with open(outputFolder + '/statsWeek.csv', 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            header = ["SENDER", "SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
            csvwriter.writerow(header)
            for person in self._members:
                name = person.getName()
                week = person.weekHistogramAsList()
                row = [name] + week
                csvwriter.writerow(row)
            for person in self._members:
                name = person.getName()
                week = person.weekHistogramAsList()
                normalizedWeek = map((lambda x: "%.2f" % (float(x * 100) / person.numMessagesSent())), week)
                row = [name] + normalizedWeek
                csvwriter.writerow(row)
        with open(outputFolder + "/basicStats.csv", 'wb') as csvfile:
            header = ["SENDER", "MESSAGE_COUNT", "WORD_COUNT", "AVERAGE_MESSAGE_LENGTH", "AVERAGE_CONSECUTIVE"]
            header += ["GIFS_SENT", "PHOTOS_SENT", "VIDEOS_SENT", "STICKERS_SENT", "LINKS_SENT"]
            csvwriter = csv.DictWriter(csvfile, fieldnames=header, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writeheader()
            for person in self._members:
                row = {
                    "SENDER": person.getName(),
                    "MESSAGE_COUNT": person.numMessagesSent(),
                    "WORD_COUNT": person.wordCount(),
                    "AVERAGE_MESSAGE_LENGTH": "%.2f" % (float(person.numWordsSent()) / person.numMessagesSent()),
                    "AVERAGE_CONSECUTIVE": person.getAverageConsecutiveCount(),
                    "GIFS_SENT": person.numGifsSent(),
                    "PHOTOS_SENT": person.numPhotosSent(),
                    "VIDEOS_SENT": person.numVideosSent(),
                    "STICKERS_SENT": person.numStickersSent(),
                    "LINKS_SENT": person.numLinksSent(),
                }
                csvwriter.writerow(row)
        with open(outputFolder + "/reactionStats.csv", 'wb') as csvfile:
            header = ["SENDER"]
            for _, reaction in REACTION_MAP.iteritems():
                header += ["%s_RECIEVED" % reaction, "%s_GIVEN" % reaction]
            csvwriter = csv.DictWriter(csvfile, fieldnames=header, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writeheader()
            reactionGraph = ReactionGraph(self._allMessages)
            for person in self._members:
                row = reactionGraph.reactionsSentRecievedAndNormalizedByPerson(self._messageHist, person.getName())
                row["SENDER"] = person.getName()
                csvwriter.writerow(row)
        with open(outputFolder + '/lifeStats.csv', 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            personIndex = {}
            index = 0
            for (msgTime, sender) in self._messageTimeline:
                if sender not in personIndex:
                    personIndex[sender] = index
                    index += 1
                csvwriter.writerow([msgTime, personIndex[sender]])
            for p, i in personIndex.iteritems():
                csvwriter.writerow([p, i])
        with open(outputFolder + '/timelineStats.csv', 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            timeline = self._messageTimelineByPerson
            csvwriter.writerow(["SENDER"] + timeline.keys())
            for person in self._members:
                name = person.getName()
                row = [name]
                cumulative = 0
                for day, details in timeline.iteritems():
                    if name in details:
                        cumulative += details[name]
                    else:
                        cumulative += 0
                    row += [cumulative]
                csvwriter.writerow(row)
        with open(outputFolder + "/topStats.csv", 'wb') as csvfile:
            header = ["SENDER", "#1", "Count", "#2", "Count"]
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(header)
            for person in self._members:
                name = person.getName()
                row = [name]
                emojis = person.emojisSent()
                if len(emojis) == 1:
                    row += [emojis[0][0], emojis[0][1], "", 0]
                elif len(emojis) > 1:
                    row += [emojis[0][0], emojis[0][1], emojis[1][0], emojis[1][1]]
                else:
                    row += ["", 0, "", 0]
                csvwriter.writerow(row)
