import sys
import gzip
import snap
import time

GItems = snap.TUNGraph.New()

''' nodeIdItems = {} # Key is the nodeId (int) in the graph and value (string) is the asin of the item '''
asinItems = {} # Key (string) is the asin of the item and value is the nodeId (int) in the graph

GUsers = snap.TUNGraph.New()

nodeIdUsers = {} # Key is the nodeId (int) in the graph and value (string) is the reviewerID of the user
reviewerIdUsers = {} # Key (string) is the reviewerID of the user and value is the nodeId (int) in the graph

GCombined = snap.TUNGraph.New()

''' nodeIdCombined = {} # Key is the nodeId (int) in the graph and value (string) is the reviewerID of the user or asin of the item '''
asinReviewerIdCombined = {} # Key (string) is the reviewerID of the user or asin of the item and value is the nodeId (int) in the graph
combinedNodeId = 0

def parseIterator(path):
	g = gzip.open(path, 'r')
	for l in g:
		yield eval(l)

def parseItems(path):
	# Adding nodes to GItems and GCombined
	global combinedNodeId
	itemsNodeId = 0
	for item in parseIterator(path):
		# Adding nodes to GItems
		GItems.AddNode(itemsNodeId)
		''' nodeIdItems[itemsNodeId] = item['asin'] '''
		asinItems[item['asin']] = itemsNodeId
		itemsNodeId +=1
		# Adding nodes to GCombined
		GCombined.AddNode(combinedNodeId)
		''' nodeIdCombined[combinedNodeId] = item['asin'] '''
		asinReviewerIdCombined[item['asin']] = combinedNodeId
		combinedNodeId +=1

	# Adding edges to GItems
	for itemSrc in parseIterator(path):
		try: # Some items do not have related or bought_together
			related = itemSrc['related']
			for itemDstAsin in related['bought_together']:
				if asinItems[itemDstAsin] is not None: # Some bought_together items are not present in nodes
					GItems.AddEdge(asinItems[itemDstAsin], asinItems[itemSrc['asin']])
					GCombined.AddEdge(asinItems[itemDstAsin], asinItems[itemSrc['asin']])
		except KeyError:
			pass

def parseReviews(path):
	# Adding nodes to GUsers and GCombined
	global combinedNodeId
	usersNodeId = 0
	for review in parseIterator(path):
		# Adding nodes to GUsers
		reviewerId = reviewerIdUsers.get(review['reviewerID'])
		if reviewerId is None:
			GUsers.AddNode(usersNodeId)
			nodeIdUsers[usersNodeId] = review['reviewerID']
			reviewerIdUsers[review['reviewerID']] = usersNodeId
			usersNodeId += 1
			# Adding nodes to GCombined
			GCombined.AddNode(combinedNodeId)
			''' nodeIdCombined[combinedNodeId] = review['reviewerID'] '''
			asinReviewerIdCombined[review['reviewerID']] = combinedNodeId
			combinedNodeId += 1

	# Adding edges to GUsers
	goodRating = 5
	users = []
	reviews = parseIterator(path)
	while True: # Adding the first user with overall > goodRating
		reviewFirst = reviews.next()
		if int(reviewFirst['overall']) >= goodRating:
			break
	GCombined.AddEdge(asinReviewerIdCombined[reviewFirst['reviewerID']], asinReviewerIdCombined[reviewFirst['asin']])
	asinCompare = reviewFirst['asin']
	users.append(reviewerIdUsers[reviewFirst['reviewerID']])
	while True:
		try:
			while True:
				review = reviews.next()
				if int(review['overall']) >= goodRating:
					break
			GCombined.AddEdge(asinReviewerIdCombined[review['reviewerID']], asinReviewerIdCombined[review['asin']])
			if review['asin'] == asinCompare:
				users.append(reviewerIdUsers[review['reviewerID']])
			else:
				for userSrcIndex in range(0, len(users)):
					for userDstIndex in range(userSrcIndex+1, len(users)):
						GUsers.AddEdge(users[userSrcIndex], users[userDstIndex])
						GCombined.AddEdge(asinReviewerIdCombined[nodeIdUsers[users[userSrcIndex]]], asinReviewerIdCombined[nodeIdUsers[users[userDstIndex]]])
				del users[:]
				asinCompare = review['asin']
				users.append(reviewerIdUsers[review['reviewerID']])
		except StopIteration:
			for userSrcIndex in range(0, len(users)):
					for userDstIndex in range(userSrcIndex+1, len(users)):
						GUsers.AddEdge(users[userSrcIndex], users[userDstIndex])
						GCombined.AddEdge(asinReviewerIdCombined[nodeIdUsers[users[userSrcIndex]]], asinReviewerIdCombined[nodeIdUsers[users[userDstIndex]]])
			break
		
def main(argv):
	item = 'Automotive'

	# Parsing Items
	parseItems('meta_' + item + '.json.gz')
	
	snap.PrintInfo(GItems, 'GItems Information')
		  
	# Saving GItems
	FOut1 = snap.TFOut('Binary_GItems_' + item + '.graph')
	GItems.Save(FOut1)
	FOut1.Flush()
	snap.SaveEdgeList(GItems, 'Text_GItems_' + item + '.txt')

	# Parsing Reviews
	parseReviews('reviews_' + item + '.json.gz')
	
	snap.PrintInfo(GUsers, 'GUsers Information')

	# Saving GUsers
	FOut2 = snap.TFOut('Binary_GUsers_' + item + '.graph')
	GItems.Save(FOut2)
	FOut2.Flush()
	snap.SaveEdgeList(GUsers, 'Text_GUsers_' + item + '.txt')

	snap.PrintInfo(GCombined, 'GCombined Information')

	# Saving GCombined
	FOut3 = snap.TFOut('Binary_GCombined_' + item + '.graph')
	GCombined.Save(FOut3)
	FOut3.Flush()
	snap.SaveEdgeList(GCombined, 'Text_GCombined_' + item + '.txt')

if __name__ == '__main__':
	start_time = time.time()
	main(sys.argv)
	print 'Execution time is ' + str(time.time() - start_time) + ' seconds'