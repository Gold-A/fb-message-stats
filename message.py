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
        "\\xf0\\x9f\\xa7\\x90" : "*Monicle*",
        "\\xf0\\x9f\\x8e\\x82" : "*Cake*",
        "\\xf0\\x9f\\x98\\x95" : ":S",
        "\\xf0\\x9f\\x99\\x83" : "*UpsideDownSmile*",
        "\\xf0\\x9f\\x94\\xa5" : "*Fire*",
        "\\xf0\\x9f\\x98\\xb7" : "*MedicalMask*",
        "\\xf0\\x9f\\x98\\x91" : "-_-",
        "\\xf0\\x9f\\x91\\x8b" : "*Wave*",
        "\\xf0\\x9f\\x98\\xa9" : "*WearyFace*",
    }


    @staticmethod
    def translate(uword):
        if uword in Emoji.EMOJI_MAP:
            return Emoji.EMOJI_MAP[uword]
        else:
            return uword

    @staticmethod
    def matchAllAndTranslate(word):
        allTranslatedMatches = []
        matches = Emoji.emojiMatch(uword)
        if matches:
            for match in matches:
                allTranslatedMatches.append(Emoji.translate(match))
        return allTranslatedMatches


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
        # Handle emoticons e.g. :D :| D:
        self._bagOfWords = [word for  sublist in map((lambda x: Message.formatWord(x)), bagOfWords) for word in sublist]

    @staticmethod
    def removeU(text):
        if text[0] == 'u':
            return text[1:]
        return text

    @staticmethod
    def formatWord(text):
        # This is all super hacky, playing around with raw strings and unicodes
        text = repr(text)
        if text.startswith("u"):
            text = text[2:-1]
            text = text.replace("\\xe2\\x80\\x99", "'")

        emojis = Emoji.emojiMatch(text)
        for emoji in emojis:
            text = text.replace(emoji, " ", 1)
        remainingWords = text.split()
        nonAlphaNumericWords = []

        for word in remainingWords:
            if re.match('^[^a-zA-Z0-9]+$', word):
                nonAlphaNumericWords.append(word)

        pattern = re.compile('[\W_]+')
        formattedWords = map((lambda x: pattern.sub('', x.lower())), remainingWords)
        ret = filter(lambda x: len(x) > 0, formattedWords) + emojis + nonAlphaNumericWords
        return ret


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


    def getUnixTime(self):
        return self._date.strftime("%s")


    def getContent(self):
        if self._text != "":
            return self._text
        return self._type


    @staticmethod
    def isBoringWord(word):
        top100EnglishWords = [
            "the",
            "be",
            "to",
            "of",
            "and",
            "a",
            "in",
            "that",
            "have",
            "i",
            "it",
            "for",
            "not",
            "on",
            "with",
            "he",
            "as",
            "you",
            "do",
            "at",
            "this",
            "but",
            "his",
            "by",
            "from",
            "they",
            "we",
            "say",
            "her",
            "she",
            "or",
            "an",
            "will",
            "my",
            "one",
            "all",
            "would",
            "there",
            "their",
            "what",
            "so",
            "up",
            "out",
            "if",
            "about",
            "who",
            "get",
            "which",
            "go",
            "me",
            "when",
            "make",
            "can",
            "like",
            "time",
            "no",
            "just",
            "him",
            "know",
            "take",
            "people",
            "into",
            "year",
            "your",
            "good",
            "some",
            "could",
            "them",
            "see",
            "other",
            "than",
            "then",
            "now",
            "look",
            "only",
            "come",
            "its",
            "over",
            "think",
            "also",
            "back",
            "after",
            "use",
            "two",
            "how",
            "our",
            "work",
            "first",
            "well",
            "way",
            "even",
            "new",
            "want",
            "because",
            "any",
            "these",
            "give",
            "day",
            "most",
            "us",
        ]
        return word in top100EnglishWords


