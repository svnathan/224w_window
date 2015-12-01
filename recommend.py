import json
import snap
from os import listdir
from os.path import isfile, join
from sys import argv
import pickle
import math
from linkPrediction import *


script, directory, item, inputDirectoryUsers, inputDirectoryItems = argv

graph = 'Users'

# Read in page rank scores 
pagerank = {}
with open(directory + 'Pagerank_' + graph + '_' + item +'.txt', 'r') as infile1:
    pagerank = json.load(infile1)


# Read in eigen centrality scores 
eigen_centrality = {}
with open(directory + 'Eigen_Value_' + graph + '_' + item +'.txt', 'r') as infile2:
    eigen_centrality = json.load(infile2)

# Read in nodesAtHop
inFiles = [f for f in listdir(inputDirectoryUsers) 
    if isfile(join(inputDirectoryUsers,f)) ]
# inFiles = ['cluster_100']

nodesAtHop = []
for filename in inFiles:
    with open(inputDirectoryUsers + filename, 'r') as infile3:
        curCluster = json.load(infile3)
    nodesAtHop.append(curCluster)

# Read in nodesAtHop
inFiles = [f for f in listdir(inputDirectoryItems) 
    if isfile(join(inputDirectoryItems,f)) ]
# inFiles = ['cluster_100']


# Read in userNodeIds
userNodeIds = [] 
with open(directory + 'UserNodeIds', 'rb') as infile1:
    userNodeIds = pickle.load(infile1)

# Read in itemNodeIds 
itemNodeIds = [] 
with open(directory + 'ItemNodeIds', 'rb') as infile1:
    itemNodeIds = pickle.load(infile1)

# Read in nodeToAmazonIds
f1 = open(directory + 'NodeIdToAmazonId','r')
nodeToAmazonIds = json.load(f1)
f1.close()

# Read in amazonIdsToNodeIds
f2 = open(directory + 'AmazonIdToCombinedId', 'r')
nodeToAmazonIds = json.load(f2)
f2.close()

nodesAtHopItems = []
for filename in inFiles:
    with open(inputDirectoryItems + filename, 'r') as infile4:
        curCluster = json.load(infile4)
    nodesAtHopItems.append(curCluster)

userToItems = {}
with open(directory + '_User_Item_' + item + '.txt', 'r') as infile4:
    userToItems = json.load(infile4)


usersGraph = snap.LoadEdgeList(snap.PUNGraph, directory + 'Edge_List_Users_' + item +'.txt', 0, 1, '\t')
itemsGraph = snap.LoadEdgeList(snap.PUNGraph, directory + 'Edge_List_Items_' + item +'.txt', 0, 1, '\t')
GCombined = snap.LoadEdgeList(snap.PUNGraph, directory + 'Edge_List_Combined_' + item +'.txt', 0, 1, '\t')

#predictLinksJaccard(GCombined, nodesAtHop, itemNodeIds, userNodeIds, directory)
#predictLinksNegatedShortestPath(GCombined, nodesAtHop, itemNodeIds, userNodeIds, directory)
predictLinksAdamicAdar(nodesAtHop, itemNodeIds, userNodeIds, directory, item)

with open(directory + 'Jaccards', 'rb') as infile1:
    scoresJaccard = pickle.load(infile1)
    
with open(directory + 'NegatedShortestPath', 'rb') as infile2:
    scoresNegatedShortedPath = pickle.load(infile2)
    
scoresAdamicAdar = {}
with open(directory + 'AdamicAdar', 'rb') as infile3:
    scoresAdamicAdar = pickle.load(infile3)

# PR, EIG
wtVec = [2.0, 1.5]

def dotProduct(vec):
    score = 0
    for idx in range(len(wtVec)):
        score += wtVec[idx]*vec[idx]
    return score

def updateDict(scores, hopDistance, queryUser, targetUser, items, alreadyBought):
    scale = 1.0/hopDistance
    pr = pagerank[targetUser]
    eig = eigen_centrality[targetUser]
    numThrownAway = 0
    for item in items:
        if item in alreadyBought:
            numThrownAway += 1
            continue
        if not item in scores:
            scores[item] = 0.0
        scores[item] += scale*dotProduct([pr,eig])
    # print 100.0*numThrownAway/len(items)
    return
    
N = 10 # How many predictions per user

itemToCommunityDict = {} 
for community in nodesAtHopItems:
    for item in community:
        if not item in itemToCommunityDict:
            itemToCommunityDict[item] = set()
        itemToCommunityDict[item].update(community.keys())
# print itemToCommunityDict.keys()
itemWeight = 5.0

def updateByItemCommunity(scores, distance, referenceItems, alreadyBought):
    scale = 1/(1.0+distance)
    for item in referenceItems:
        # print item
        if item not in itemToCommunityDict:
            continue
        simItems = itemToCommunityDict[item]
        # print simItems
        for simItem in simItems:
            # print simItem
            if simItem in alreadyBought:
                continue
            if not simItem in scores:
                scores[simItem] = 0.0
            scores[simItem] += scale*itemWeight
            # print simItem
        
# Recommend
userRecommendations = []
for community in nodesAtHop:
    userRecommendations.append({})
    for queryUser in community:
        scores = {} # Item -> Score
        allNbrs = community[queryUser]
        alreadyBought = userToItems[queryUser]
        for targetUser in allNbrs:
            boughtItems = userToItems[targetUser]
            hopDistance = allNbrs[targetUser]
            updateDict(scores, hopDistance, queryUser, targetUser, boughtItems, alreadyBought)
            updateByItemCommunity(scores, hopDistance, boughtItems, alreadyBought)
        updateByItemCommunity(scores, 0, alreadyBought, alreadyBought)
        srted = sorted(scores.iteritems(), key=lambda x:(-x[1],x[0]))
        topN = [x[0] for x in srted[:min(N,len(srted))]]
        userRecommendations[-1][queryUser] = topN
with open(directory + 'recommendations', 'wb') as outfile:
    pickle.dump(userRecommendations, outfile)
# Compare against ground truth 
