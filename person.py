import message as m

class Person:
    def __init__(self, name):
    	self._name = name
    	self._messagesSent = []
    	self._wordsSent = {}
    	self._totalWordCount = 0

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

    def numMessagesSent(self):
    	return len(self._messagesSent)

    def numWordsSent(self):
    	return self._totalWordCount

    def topWords(self, x):
    	return sorted(self._wordsSent.iteritems(), key=lambda (k,v): (v,k), reverse=True)[:x]
    	# filterout boring words e.g. "the" "i" "a"
