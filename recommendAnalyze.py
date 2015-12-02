from sys import argv
import gzip
import shutil
import json
import pickle
import json
from matplotlib import pyplot

script, directory, directoryReviews, item, week, year = argv

print year
weeks = range(int(week)+1,int(week)+53)

newEdges = {} # Ground truth next year

def parseIterator(path):
	with open(path,'r') as f:
	    for line in f:
	    	yield eval(line)
	# g = gzip.open(path, 'r')
	# for l in g:
	# 	yield eval(l)

def findNewEdges():
	with open(directory + 'Dictionary_Items_' + item + '.txt', 'r') as f1:
		asinItems = json.load(f1)
	with open(directory + 'Dictionary_Users_' + item + '.txt', 'r') as f2:
		reviewerIdUsers = json.load(f2)
	with open(directoryReviews + 'reviews_' + item + '_' + year + '.json', 'rb') as f_in, gzip.open(directoryReviews + 'reviews_' + item + '_' + year + '.json.gz', 'wb') as f_out:
		shutil.copyfileobj(f_in, f_out)
	for curWeek in weeks:
		filename = directoryReviews + 'reviews_' + item + '_' + year + '_' + str(curWeek) + '.json'
		for review in parseIterator(filename):
			# print review['reviewerID']
			if review['reviewerID'] in reviewerIdUsers: # Check if user in the years we predicted from
				nodeNumber = reviewerIdUsers[review['reviewerID']]
				if not nodeNumber in newEdges:
					newEdges[nodeNumber] = []
				itemNodeId = int(asinItems[review['asin']])
				newEdges[nodeNumber].append(itemNodeId)
	# filename = directoryReviews + 'reviews_' + item + '_' + year + '.json'
	# for review in parseIterator(filename):
	# 	# print review['reviewerID']
	# 	if review['reviewerID'] in reviewerIdUsers: # Check if user in the years we predicted from
	# 		nodeNumber = reviewerIdUsers[review['reviewerID']]
	# 		if not nodeNumber in newEdges:
	# 			newEdges[nodeNumber] = []
	# 		# print nodeNumber, '\t', review['asin']
	# 		itemNodeId = int(asinItems[review['asin']])
	# 		newEdges[nodeNumber].append(itemNodeId)

def checkEdges():
	with open(directory + 'recommendations','rb') as f:
		predictions = pickle.load(f)

	allScores = []
	allPreds = []
	allUsers = []
	for cluster in range(0, len(predictions)):
		commScores = []
		commPreds = []
		commUsers = 0.0
		for userStr, items in predictions[cluster].iteritems():
			user = int(userStr)
			if not user in newEdges:
				groundTruth = set()
			else:
				groundTruth = set(newEdges[user])
			itemSet = set(items)
			matched = set.intersection(*[itemSet, groundTruth])
			if len(itemSet) == 0:
				score = 0.5
				continue
			else:
				score = len(matched)*1.0/len(itemSet)
			commScores.append(score)
			commPreds.append(len(itemSet))
			commUsers += 1
		allScores.append(commScores)
		allUsers.append(commUsers)
		allPreds.append(commPreds)
	
	commScores = [sum(x)*100.0/(0.000001+len(x)) for x in allScores]
	commPreds = [sum(x)/(0.000001+len(x)) for x in allPreds]
	X = [commScores[i]*allUsers[i] for i in range(len(allUsers))]
	# print zip(commScores, commPreds)
	# print allUsers
	print sum(X)/sum(allUsers)
	pyplot.plot(range(len(predictions)), commScores, 'b-', label = 'Correct')
	#pyplot.plot(range(len(predictions)), commPreds, 'r--', label = 'Correct')
	pyplot.title('Cluster vs. Percentage of Predictions')
	pyplot.xlabel('Cluster')
	pyplot.ylabel('Percentage of Correct Predictions')
	pyplot.legend(loc = 'upper right')
	# pyplot.show()
	pyplot.savefig('Rec.png')

def main(argv):
	findNewEdges()
	checkEdges()

if __name__ == '__main__':
	main(argv)