import snap
from sys import argv

script, inputfile, outputfile= argv

G = snap.LoadEdgeList(snap.PUNGraph, inputfile, 0, 1, '\t')
CmtyV = snap.TCnComV()
modularity = snap.CommunityCNM(G, CmtyV)
communityCount = 0
f = open(outputfile, 'w')
nodes = 0
for Cmty in CmtyV:
	communityCount += 1
	for NI in Cmty:
		f.write(str(communityCount) + ":" + str(NI)+'\n')
		nodes += 1
print 'nodes=', nodes