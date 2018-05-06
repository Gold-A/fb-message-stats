from message import Emoji, MsgType
import datetime

class Person:
    def __init__(self, name):
        self._name = name
        self._messagesSent = []
        self._wordsSent = {}
        self._emojiSent = {}
        self._totalWordCount = 0
        self._stickersSent = 0
        self._gifsSent = 0
        self._photosSent = 0
        self._videosSent = 0
        self._stickersSent = 0
        self._linksSent = 0
        self._dateOfFirstMessage = datetime.datetime.max
        self._firstMessage = ""


    def getName(self):
        return self._name


    def addMessage(self, msg):
        self._messagesSent.append(msg)
        for word in msg.getWords():
            if word in self._wordsSent:
                self._wordsSent[word] += 1
            else:
                self._wordsSent[word] = 1
            emojiChars = Emoji.emojiMatch(word)
            if emojiChars:
                for match in emojiChars:
                    translated = Emoji.translate(match)
                    if translated in self._emojiSent:
                        self._emojiSent[translated] += 1
                    else:
                        self._emojiSent[translated] = 1
            self._totalWordCount += 1

        msgType = msg.getType()
        if msgType == MsgType.GIF:
            self._gifsSent += msg.numGifs()
        elif msgType == MsgType.STICKER:
            self._stickersSent += 1
        elif msgType == MsgType.PHOTO:
            self._photosSent += msg.numPhotos()
        elif msgType == MsgType.VIDEO:
            self._videosSent += msg.numVideos()
        elif msg.hasShare():
            self._linksSent += 1

        msgDate = msg.getDate()
        if msgDate < self._dateOfFirstMessage:
            self._dateOfFirstMessage = msgDate
            self._firstMessage = msg.getContent()


    def numMessagesSent(self):
        return len(self._messagesSent)


    def numWordsSent(self):
        return self._totalWordCount

    
    def numGifsSent(self):
        return self._gifsSent
    

    def numStickersSent(self):
        return self._stickersSent
    

    def numPhotosSent(self):
        return self._photosSent
    

    def numVideosSent(self):
        return self._videosSent
    

    def numLinksSent(self):
        return self._linksSent


    def topWords(self, x):
        return sorted(self._wordsSent.iteritems(), key=lambda (k,v): (v,k), reverse=True)[:x]
        # filterout boring words e.g. "the" "i" "a"


    def emojiSent(self):
        return sorted(self._emojiSent.iteritems(), key=lambda (k,v): (v,k), reverse=True)


    def wordCount(self):
        return self._totalWordCount


    def messageCount(self):
        return len(self._messagesSent)


    def weekHistogram(self):
        WEEK = {
            0 : "M",
            1 : "Tu",
            2 : "W",
            3 : "Th",
            4 : "F",
            5 : "Sa",
            6 : "Su",
        }

        hist = {
            "Su" : 0,
            "M" : 0,
            "Tu" : 0,
            "W" : 0,
            "Th" : 0,
            "F" : 0,
            "Sa" : 0,
        }
        for msg in self._messagesSent:
            hist[WEEK[msg.weekday()]] += 1

        return hist


    def monthHistogram(self):
        hist = {}
        for i in range(12):
            hist[i+1] = 0

        for msg in self._messagesSent:
            hist[msg.month()] += 1

        return hist


    def hourHistogram(self):
        hist = {}
        for i in range(24):
            hist[i] = 0

        for msg in self._messagesSent:
            hist[msg.hour()] += 1

        return hist


    def getDateFirstMessage(self):
        return self._dateOfFirstMessage.isoformat()


    def getFirstMessage(self):
        return self._firstMessage