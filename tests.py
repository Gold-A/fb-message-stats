import unittest
import message
import person
import json

def buildMessageJson(insert):
    sampleJson = """
    {
      "sender_name": "John Smith",
      "timestamp": 1523824963,
    """ + \
    insert + \
    """
      "reactions": [
        {
          "reaction": "\u00f0\u009f\u0098\u0086",
          "actor": "Jane Jones"
        }
      ],
      "type": "Generic"
    }
    """
    return json.loads(sampleJson)


class TestMessage(unittest.TestCase):

    def test_getWords(self):
        testMessage = message.Message(buildMessageJson("\"content\": \"Hello there friend\","))
        result = testMessage.getWords()
        self.assertItemsEqual(result, ["hello", "there", "friend"])


    def test_Name(self):
        testMessage = message.Message(buildMessageJson(""))
        result = testMessage.getSender()
        self.assertEqual(result, "John Smith")


    def test_Gifs(self):
        gifs = """
          "gifs": [
            {
              "uri": "messages/groupID/gifs/1111.gif",
              "media_path": "messages/groupID/gifs"
            }
          ],
        """
        testMessage = message.Message(buildMessageJson(gifs))
        self.assertEquals(testMessage.numGifs(), 1)
        self.assertEquals(testMessage.getType(), message.MsgType.GIF)


    def test_Stickers(self):
        sticker = """
          "sticker": {
            "uri": "messages/stickers_used/1111.png",
            "media_path": "messages/stickers_used"
          },
        """
        testMessage = message.Message(buildMessageJson(sticker))
        self.assertTrue(testMessage.isSticker())
        self.assertEquals(testMessage.getType(), message.MsgType.STICKER)



    def test_Photos(self):
        photos = """
          "photos": [
            {
              "uri": "messages/groupID/gifs/1111.gif",
              "media_path": "messages/groupID/gifs"
            },
            {
              "uri": "messages/groupID/gifs/2222.gif",
              "media_path": "messages/groupID/gifs"
            }
          ],
        """
        testMessage = message.Message(buildMessageJson(photos))
        self.assertEquals(testMessage.numPhotos(), 2)
        self.assertEquals(testMessage.getType(), message.MsgType.PHOTO)



    def test_Videos(self):
        videos = """
          "videos": [
            {
              "uri": "messages/groupID/videos/1111.mp4",
              "media_path": "messages/groupID/videos",
              "thumbnail": {
                "uri": "messages/groupID/videos/thumbnails/1111.jpg",
                "media_path": "messages/groupID/videos/thumbnails"
              }
            },
            {
              "uri": "messages/groupID/videos/2222.mp4",
              "media_path": "messages/groupID/videos",
              "thumbnail": {
                "uri": "messages/groupID/videos/thumbnails/2222.jpg",
                "media_path": "messages/groupID/videos/thumbnails"
              }
            }
          ],
        """
        testMessage = message.Message(buildMessageJson(videos))
        self.assertEquals(testMessage.numVideos(), 2)
        self.assertEquals(testMessage.getType(), message.MsgType.VIDEO)



    def test_Share(self):
        typeshare = json.loads("""
        {
            "sender_name": "Jane Jones",
            "timestamp": 1518666201,
            "content": "https://www.google.com",
            "share": {
                "link": "https://www.google.com"
            },
            "type": "Share"
        }
        """)
        testMessage = message.Message(typeshare)
        self.assertTrue(testMessage.hasShare())
        self.assertEquals(testMessage.getType(), message.MsgType.SHARE)
        impliedShare = json.loads("""
        {
            "sender_name": "Jane Jones",
            "timestamp": 1518666201,
            "content": "https://www.google.com",
            "type": "Generic"
        }
        """)
        testMessage2 = message.Message(impliedShare)
        self.assertTrue(testMessage2.hasShare())
        self.assertEquals(testMessage2.getType(), message.MsgType.SHARE)


    def test_Unicode(self):
        matches = message.Message.unicodeMatch(repr(u'\xf0\x9f\x98\xae\xf0\x9f\x98\xae'))

        self.assertItemsEqual(matches, ["\\xf0\\x9f\\x98\\xae", "\\xf0\\x9f\\x98\\xae"])


class TestPerson(unittest.TestCase):
    def setUp(self):
        msgs = []
        photos = """
            "content": "Hello there friend",
            "photos": [
                {
                  "uri": "messages/groupID/photos/1111.png",
                  "media_path": "messages/groupID/photos"
                },
                {
                  "uri": "messages/groupID/photos/2222.png",
                  "media_path": "messages/groupID/photos"
                }
            ],
        """
        sticker = """
          "sticker": {
            "uri": "messages/stickers_used/1111.png",
            "media_path": "messages/stickers_used"
          },
        """
        msgs.append(message.Message(buildMessageJson(photos)))
        msgs.append(message.Message(buildMessageJson(sticker)))
        msgs.append(message.Message(buildMessageJson("\"content\": \"My friend says hello\",")))
        self._testPerson = person.Person("John Smith")
        for msg in msgs:
            self._testPerson.addMessage(msg)


    def test_Name(self):
        name = self._testPerson.getName()
        self.assertEquals(name, "John Smith")


    def test_Counts(self):
        self.assertEquals(self._testPerson.numMessagesSent(), 3)
        self.assertEquals(self._testPerson.numStickersSent(), 1)
        self.assertEquals(self._testPerson.numPhotosSent(), 2)


    def test_TopWords(self):
        topwords = [x[0] for x in self._testPerson.topWords(2)]
        self.assertItemsEqual(topwords, ["friend", "hello"])


if __name__ == '__main__':
    unittest.main()