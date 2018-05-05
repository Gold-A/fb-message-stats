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