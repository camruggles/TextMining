import sys
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

#global variables
deck = [] #Used to hold all individual cards
stoplist = [] #contains information about a stoplist

#global variable modifiers
def weedwack(s): #used to trim down strings
	n = len(s)
	if (n < 2): return s
	
	c = s[n-1]
	if (',' in c or '.' in c or '?' in c or ':' in c or '!' in c):
		return j[0:len(j)-1]
	return j

def check(s): #used to see if the word described is in stoplist
	return stoplist.contains(s)

def stopAdd(s): #adds a word to the stoplist
	stoplist.append(s)

#Class Cardcounter, used to record card id's and their cosine similarity value
class Cardcounter:

	def __init__(self, i, j, diff):
		self.i = i
		self.j = j
		self.diff = diff

	def compareTo(self, c):
		if self.diff < c.diff:
			return 1
		if self.diff == c.diff:
			return 0
		return -1

#holds all the grams about a particular card
class Card:

	uTable = {}

	def __init__(self):
		self.words = []
		self.table = {}
		self.grams1 = []
		self.grams2 = []
		self.grams3 = []
		self.grams4 = []
		self.grams5 = []
		self.title = ""


	def add(self, s): #adds a unigram to words
		self.words.append(s)

	def printall(self): #prints out all words in the list "words"
		for s in self.words:
			sys.stdout.write("%s, " % (s))
		sys.stdout.write("\n")

	def setTitle(self, title): #changes variable "title" to the value given by the parameter
		self.title = title

	def computeGrams(self): #populates the grams# lists
		length = len(self.words)
		for i in range(0, length):
			self.grams1.append(self.words[i])
			if i < length-1:
				self.grams2.append("%s %s" % (self.words[i], self.words[i+1]))
			if i < length-2:
				self.grams3.append("%s %s %s" % (self.words[i], self.words[i+1], self.words[i+2]))
			if i < length-3:
				self.grams4.append("%s %s %s %s" % (self.words[i], self.words[i+1], self.words[i+2], self.words[i+3]))
			if i < length-4:
				self.grams5.append("%s %s %s %s %s" % (self.words[i], self.words[i+1], self.words[i+2], self.words[i+3], self.words[i+4]))
		for word in self.grams1:
			self.uTable[word] = 0
			if self.table.has_key(word):
				self.table[word] += 1
			else:
				self.table[word] = 1

	def updateUTable(self):
		for keys in self.uTable.keys():
			if self.table.has_key(keys) == False:
				self.table[keys] = 0



######## MAIN ########

#create a card, add all the words to the card, then
#add the card to the deck
#compute grams later on


#open the file, add the stoplist words to list "stopword"
stopRead = open("stopwords.txt", "r")
newStopWord = stopRead.readline()
while (newStopWord != None and newStopWord != ""):
#	print newStopWord
	stopAdd(newStopWord)
	newStopWord = stopRead.readline()

del stopRead
newStopWord = None


#gets the file from command line
if (len(sys.argv) != 2):
	print "Need a file name"
	quit()
fileName1 = sys.argv[1]

#declares all necessary variables for intaking words
line = ""
word = ""
file1 = open(fileName1, "r")
title = True

#loop that reads in words, breaks between cards,
#--------------------QUARANTINE ZONE-----------------------------
card  = Card()
s = "Help me."
s = s[0:len(s)-1]
#print s

fileContents = file1.read()
lines = fileContents.split("\n")
for i in lines:
	if i.strip() == '':
		continue
	if 'BLUEBOTTLECOFFEE.COM' in i:
		#append card
		#create a new card
		#set title to be true
		#continue
		deck.append(card)
		#print "Printing"
		#card.printall()
		#quit()
		card = Card()
		title = True
		continue
	#sys.stdout.write("Line: %s\n" % (i))
	if title:
		line = i.strip()
		#sys.stdout.write("TITLE TITLE TITLE : %s\n" % (line))
		card.setTitle(line)
		title = False
	#tempWords = line.split(" ")
	# for s in tempWords:
	# 	sys.stdout.write("%s : %s\n" % (s, weedwack(s)))

	# 	card.add(weedwack(s))
	#print i
	#print "SPLITTING"
	tempWords  = i.split(" ")
	#targetWords = []
	#print tempWords
	for j in tempWords:
		j.strip()
		j = weedwack(j)
		j.lower()
		card.add(j)
		#targetWords.append(j)

	#print 'REFINED:'
	#print targetWords
	#sys.stdout.write("\n\n\n")

#-------------------------------------------------
# print "fuckme"
# for cards in deck:
# 	cards.printall()
# 	print 'fuck'

for i in range(0, len(deck)):
	deck[i].computeGrams()

for card in deck:
	card.updateUTable()


#create hash tables for all words

#create a universal hash table based on all the keys from all hash tables
#re calculate every hash table based on the new universal hash table

# for card in deck:
# 	card.createUTable(universe)

#print len(deck)
#create a list and traverse the list of cards in order
card1 = deck[0]
card2 = deck[1]

print set(card1.table.keys()).symmetric_difference(card2.table.keys())

# print "Card 1:"
key1 = []
key2 = []
key1.extend(card1.table.keys())
key2.extend(card2.table.keys())
key1.sort()
key2.sort()
print key1 == key2
vector1 = []
vector2 = []

for i in key2:
	vector1.append(card1.table[i])
	vector2.append(card2.table[i])

print vector1
print vector2

A = np.array(vector1, vector2)
similarities = cosine_similarity(A_sparse)
print('pairwise dense output:\n {}\n'.format(similarities))

#print card1.table.keys()

#print "Card 2:"


# for i in card2.table.keys():
# 	print i


#print card2.table.keys()
# for i in card1.table:
# 	sys.stdout.write("%s %d\n" % (i, card1.table[i]))
# quit()
# print card1.table
# print card2.table







