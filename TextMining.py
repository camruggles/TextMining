import sys
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import numpy as np
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine
import operator
import matplotlib.pyplot as pyplot
import seaborn as sns 
import pandas as pd
import time
import pylab

#global variables
deck = [] #Used to hold all individual cards
stoplist = [] #contains information about a stoplist

#global variable modifiers
def weedwack(s): #used to trim down strings
	n = len(s)
	if (n < 2): return s
	
	c = s[n-1]
	if (',' in c or '.' in c or '?' in c or ':' in c or '!' in c or '\n' in c):
		return s[0:len(s)-1]
	return s

def check(s): #used to see if the word described is in stoplist
	return s in stoplist

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
			#if False == check(self.words[i]):
			self.grams1 = set(self.words).difference(stoplist)
			# if False == check(self.words[i]):
			# 	self.grams1.append(self.words[i])
			# difference = set
			# self.grams1.append(self.words[i])

			# if i < length-1:
			# 	self.grams2.append("%s %s" % (self.words[i], self.words[i+1]))
			# if i < length-2:
			# 	self.grams3.append("%s %s %s" % (self.words[i], self.words[i+1], self.words[i+2]))
			# if i < length-3:
			# 	self.grams4.append("%s %s %s %s" % (self.words[i], self.words[i+1], self.words[i+2], self.words[i+3]))
			# if i < length-4:
			# 	self.grams5.append("%s %s %s %s %s" % (self.words[i], self.words[i+1], self.words[i+2], self.words[i+3], self.words[i+4]))
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
	newStopWord.strip()
	newStopWord = weedwack(newStopWord)
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


for i in range(0, len(deck)):
	deck[i].computeGrams()

for card in deck:
	card.updateUTable()


vectorArray = []
for c in range(0, len(deck)):
	vectorArray.append([])

keys = []
keys.extend(card.uTable.keys())
keys.sort()

for i in keys:
	for c in range(0, len(deck)):
		vectorArray[c].append(deck[c].table[i])


A =  np.array(vectorArray)
A_sparse = sparse.csr_matrix(A)

similarities = cosine_similarity(A_sparse)


print("\n\n\n")

class Tablet:

	def __init__(self, i, j, diff, title1, title2):
		self.i = i
		self.j = j
		self.diff = diff
		self.title1 = title1
		self.title2 = title2

	def __lt__(self, other):
         return self.diff < other.diff

def printInfo(i, j):
	sys.stdout.write("<%d, %d> : %s, %s, %s\n" % (i, j, similarities[i][j], deck[i].title, deck[j].title))
			
	for key in Card.uTable.keys():
		if deck[i].table[key] > 0 and deck[j].table[key] > 0 :
			sys.stdout.write("%s: %s, %s\n" % (key, deck[i].table[key], deck[j].table[key]))
	sys.stdout.write("\n\n")

Vault = []
print "second pass"
for i in range(1, len(similarities)):
	for j in range (0, i):
		Vault.append(Tablet(i, j, similarities[i][j], deck[i].title, deck[j].title))

		# if similarities[i][j] > 0.17:
		# 	printInfo(i, j)

Vault.sort()
Vault.reverse()


def printCard(r, s):
	print r
	print s
	for key in Card.uTable.keys():
		if deck[r].table[key] > 0 and deck[s].table[key] > 0 :
			sys.stdout.write("%s: %s, %s\n" % (key, deck[r].table[key], deck[s].table[key]))
	print '\n\n'

# printInfo(31, 12)
# printInfo(38, 32)

# for tablet in Vault:
# 	sys.stdout.write("%d %d %s %s %s\n"%(tablet.i, tablet.j, tablet.diff, len(deck[tablet.i].grams1), len(deck[tablet.j].grams1)))

lenVector = []
diffVector = []

for tablet in Vault:
	lenVector.append(abs(len(deck[tablet.i].grams1) - len(deck[tablet.j].grams1)))
	diffVector.append(tablet.diff)

for i in range(0, len(diffVector)):
	sys.stdout.write("%f %d\n" % (diffVector[i], lenVector[i]))
# diffVector = [1, 2, 3, 4, 5, 6]
# lenVector = [1, 2, 3, 4, 5, 6]
pyplot.scatter(diffVector, lenVector)
pylab.show()
# print diffVector
# print lenVector

# df = pd.DataFrame()
# df['x'] = diffVector
# df['y'] = lenVector
# print df.head()



