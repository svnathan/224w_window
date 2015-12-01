communitiesDict = {}

with open("communityData/Text_GItems_Books.tree") as itemFile:
	next(itemFile)
	next(itemFile)
	for line in itemFile:
		data = line.split()
		#print data
		communities = data[0].split(':')
		#print communities
		community = int(communities[0])
		node = int(data[2][1:-1])
		if(community in communitiesDict):
			communitiesDict[community].append(node)
		else:
			communitiesDict[community] = []
			communitiesDict[community].append(node)

for key in communitiesDict.keys():
	fileName = "itemCommunities/itemCommunity%d" % key
	file = open(fileName, 'w')
	for item in communitiesDict[key]:
		file.write("%s\n" % item)

communitiesDict1 = {}
communitiesDict2 = {}

with open("communityData/Text_GUsers_Books.tree") as itemFile:
        next(itemFile)
        next(itemFile)
        for line in itemFile:
                data = line.split()
                #print data
                communities = data[0].split(':')
                #print communities
                community1 = int(communities[0])
		community2 = int(communities[1])
                node = int(data[2][1:-1])
                if(community1 in communitiesDict1):
                        communitiesDict1[community1].append(node)
                else:
                        communitiesDict1[community1] = []
                        communitiesDict1[community1].append(node)
		if(community2 in communitiesDict2):
                        communitiesDict2[community2].append(node)
                else:
                        communitiesDict2[community2] = []
                        communitiesDict2[community2].append(node)


for key in communitiesDict1.keys():
        fileName = "userCommunitiesSmall/userCommunity%d" % key
        file = open(fileName, 'w')
        for item in communitiesDict1[key]:
                file.write("%s\n" % item)

for key in communitiesDict2.keys():
        fileName = "userCommunitiesBig/userCommunity%d" % key
        file = open(fileName, 'w')
        for item in communitiesDict2[key]:
                file.write("%s\n" % item)

