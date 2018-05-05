import message as m

class Person:
    def __init__(self, name):
        self._name = name
        self._messagesSent = []
        self._wordsSent = {}
        self._totalWordCount = 0
        self._stickersSent = 0
        self._gifsSent = 0
        self._photosSent = 0
        self._videosSent = 0
        self._stickersSent = 0
        self._linksSent = 0


    def getName(self):
        return self._name


    def addMessage(self, msg):
        self._messagesSent.append(msg)
        for word in msg.getWords():
            if word in self._wordsSent:
                self._wordsSent[word] += 1
            else:
                self._wordsSent[word] = 1
            self._totalWordCount += 1

        msgType = msg.getType()
        if msgType == m.MsgType.GIF:
            self._gifsSent += msg.numGifs()
        elif msgType == m.MsgType.STICKER:
            self._stickersSent += 1
        elif msgType == m.MsgType.PHOTO:
            self._photosSent += msg.numPhotos()
        elif msgType == m.MsgType.VIDEO:
            self._videosSent += msg.numVideos()
        elif msg.hasShare():
            self._linksSent += 1


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
