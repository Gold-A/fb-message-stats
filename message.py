from datetime import datetime
import re

REACTION_MAP = {
    u'\xf0\x9f\x91\x8d' : "like",
    u'\xf0\x9f\x91\x8e' : "dislike",
    u'\xf0\x9f\x98\x86' : "haha",
    u'\xf0\x9f\x98\x8d' : "heart",
    u'\xf0\x9f\x98\xa0' : "angry",
    u'\xf0\x9f\x98\xa2' : "cry",
    u'\xf0\x9f\x98\xae' : "surprise",
}


class Emoji:

    @staticmethod
    def emojiMatch(word):
        pattern = r'\\xf0\\x9f\\x\w\w\\x\w\w'
        result = re.findall(pattern, word)
        return result

    EMOJI_MAP = {
        "\\xf0\\x9f\\xa4\\x94" : "*ChinScratch*",
        "\\xf0\\x9f\\x8d\\x89" : "*Watermelon*",
        "\\xf0\\x9f\\x98\\x82" : "*LaughingTears",
        "\\xf0\\x9f\\x98\\xad" : "*Bawling*",
        "\\xf0\\x9f\\x98\\x90" : ":|",
        "\\xf0\\x9f\\x98\\xae" : ":O",
        "\\xf0\\x9f\\x8e\\xa4" : "*Microphone*",
        "\\xf0\\x9f\\x98\\x8d" : "*HeartEyes*",
        "\\xf0\\x9f\\x98\\x83" : ":D",
        "\\xf0\\x9f\\x98\\x9e" : ":(",
        "\\xf0\\x9f\\x98\\x80" : "*GrinningFace*",
        "\\xf0\\x9f\\x98\\xb5" : "*SpiralEyes*",
        "\\xf0\\x9f\\x98\\xb1" : "*Scream*",
        "\\xf0\\x9f\\x98\\x8e" : "*Sunglasses*",
        "\\xf0\\x9f\\xa4\\xb7" : "*Shrug*",
        "\\xf0\\x9f\\xa4\\x97" : "*HuggingFace*",
        "\\xf0\\x9f\\x98\\x8f" : "*Smirk*",
        "\\xf0\\x9f\\x98\\xb4" : "*ZZZFace*",
        "\\xf0\\x9f\\x98\\x8b" : ":P",
        "\\xf0\\x9f\\x98\\xb2" : "*Astonished*",
        "\\xf0\\x9f\\x91\\x8c" : "*Okay*",
        "\\xf0\\x9f\\x91\\x8d" : "*Thumbsup*",
        "\\xf0\\x9f\\x91\\xb4" : "*Oldman*",
        "\\xf0\\x9f\\x99\\x86" : "*OHands*",
    }

    @staticmethod
    def translate(uword):
        if uword in Emoji.EMOJI_MAP:
            return Emoji.EMOJI_MAP[uword]
        else:
            return uword

class Reaction:
    def __init__(self, reactJson, speaker):
        self._reaction = REACTION_MAP[reactJson["reaction"]]
        self._actor = reactJson["actor"]
        self._speaker = speaker


    def getReactor(self):
        return self._actor


    def getReaction(self):
        return self._reaction


    def getSpeaker(self):
        return self._speaker


class MsgType():
    INVALID = "invalid"
    TEXT = "text"
    GIF = "gif"
    STICKER = "sticker"
    PHOTO = "photo"
    VIDEO = "video"
    SHARE = "share"


class Message:
    def __init__(self, messageJson):
        self._originalJsonForm = messageJson
        self._sender = str(messageJson["sender_name"])
        self._numGifs = 0
        self._isSticker = False
        self._numPhotos = 0
        self._numVideos = 0
        self._hasShare = False
        self._reactions = []
        self._bagOfWords = []
        self._type = MsgType.INVALID
        self._text = ""

        if "content" in messageJson:
            self._text = messageJson["content"]
            if self._text.find("https") >= 0:
                self._type = MsgType.SHARE
                self._hasShare = True
            else:
                self._type = MsgType.TEXT
            self.parseMessage(self._text)
        
        if "gifs" in messageJson:
            self._type = MsgType.GIF
            self._numGifs = len(messageJson["gifs"])
        elif "sticker" in messageJson:
            self._type = MsgType.STICKER
            self._isSticker = True
        elif "photos" in messageJson:
            self._type = MsgType.PHOTO
            self._numPhotos = len(messageJson["photos"])
        elif "videos" in messageJson:
            self._type = MsgType.VIDEO
            self._numVideos = len(messageJson["videos"])
        elif "share" in messageJson:
            self._type = MsgType.SHARE
            self._hasShare = True

        if self._type == None:
            return

        self._timestamp = messageJson["timestamp"]
        self._date = datetime.fromtimestamp(self._timestamp)
        self._dayOfWeek = self._date.weekday()
        self._hourOfDay = self._date.hour
        self._month = self._date.month

        if "reactions" in messageJson:
            reacts = messageJson["reactions"]
            for react in reacts:
                self._reactions.append(Reaction(react, self._sender))


    def getSender(self):
        return self._sender


    def getReactions(self):
        return self._reactions


    def parseMessage(self, text):
        bagOfWords = text.split()
        # Handle emoticons e.g. :D -___- :| D:
        # Handle repeated emojis "\u00f0\u009f\u0098\u008b\u00f0\u009f\u0098\u008b\u00f0\u009f\u0098\u008b"
        # Check mentions
        pattern = re.compile('[\W_]+')
        self._bagOfWords = map((lambda x: repr(x)), bagOfWords)
        # self._bagOfWords = map((lambda x: pattern.sub('', x.lower())), bagOfWords)
        # TODO combine lower and emoji and other parsing


    def getWords(self):
        return self._bagOfWords


    def getType(self):
        try:
            return self._type
        except Exception, e:
            print self._originalJsonForm
            raise e


    def numGifs(self):
        return self._numGifs


    def isSticker(self):
        return self._isSticker


    def numPhotos(self):
        return self._numPhotos


    def numVideos(self):
        return self._numVideos


    def hasShare(self):
        return self._hasShare


    def hour(self):
        return self._hourOfDay


    def weekday(self):
        return self._dayOfWeek


    def month(self):
        return self._month

    def getDate(self):
        return self._date

    def getContent(self):
        if self._text != "":
            return self._text
        return self._type