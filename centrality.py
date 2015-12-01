import snap
import json
from sys import argv

script, directory, item = argv

graphList = ['Items','Users']

for graph in graphList:

	G = snap.LoadEdgeList(snap.PUNGraph, directory + 'Edge_List_' + graph + '_' + item +'.txt', 0, 1, '\t')

	dict1 = {}
	PRankH = snap.TIntFltH()
	snap.GetPageRank(G, PRankH)
	for i in PRankH:
	    dict1[i] = PRankH[i]

	with open(directory + 'Pagerank_' + graph + '_' + item +'.txt', 'w') as outfile1:
		json.dump(dict1, outfile1)
		
	dict2 = {}
	NIdEigenH = snap.TIntFltH()
	snap.GetEigenVectorCentr(G, NIdEigenH)
	for i in NIdEigenH:
		dict2[i] = NIdEigenH[i]

	with open(directory + 'Eigen_Value_' + graph + '_' + item +'.txt', 'w') as outfile2:
		json.dump(dict2, outfile2)