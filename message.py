from datetime import datetime

REACTION_MAP = {
    u'\xf0\x9f\x91\x8d' : "like",
    u'\xf0\x9f\x91\x8e' : "dislike",
    u'\xf0\x9f\x98\x86' : "haha",
    u'\xf0\x9f\x98\x8d' : "heart",
    u'\xf0\x9f\x98\xa0' : "angry",
    u'\xf0\x9f\x98\xa2' : "cry",
    u'\xf0\x9f\x98\xae' : "surprise",
}


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
    TEXT = 1
    GIF = 2
    STICKER = 3
    PHOTO = 4
    VIDEO =5

class Message:
    def __init__(self, messageJson):
        self._sender = messageJson["sender_name"]
        self._numGifs = 0
        self._numStickers = 0
        self._numPhotos = 0
        self._numVideos = 0
        self._reactions = []

        if "content" in messageJson:
            self._type = MsgType.TEXT
            self._text = messageJson["content"]
        elif "gifs" in messageJson:
            self._type = MsgType.GIF
            self._numGifs = len(messageJson["gifs"])
        elif "sticker" in messageJson:
            self._type = MsgType.STICKER
            self._numStickers = len(messageJson["sticker"])
        elif "photos" in messageJson:
            self._type = MsgType.PHOTO
            self._numPhotos = len(messageJson["photos"])
        elif "videos" in messageJson:
            self._type = MsgType.VIDEO
            self._numVideos = len(messageJson["videos"])

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