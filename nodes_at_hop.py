from os import listdir
from os.path import isfile, join
import snap
import json
from sys import argv

script, inputDirectory, outputDirectory = argv

inFiles = [f for f in listdir(inputDirectory) 
	if isfile(join(inputDirectory,f)) ]

for clusterFile in inFiles:
	GSnap = snap.LoadEdgeList(snap.PUNGraph, inputDirectory+clusterFile, 0, 1, '\t')
	matrix = dict()
	for node in GSnap.Nodes():
		hop = 0
		flag = True
		while flag == True:
			hop += 1
			flag = False
			NodeVec = snap.TIntV()
			snap.GetNodesAtHop(GSnap, node.GetId(), hop, NodeVec, False)
			for item in NodeVec:
				flag = True
				if not node.GetId() in matrix:
					matrix[node.GetId()] = dict()
				matrix[node.GetId()][item] = hop					
	with open(outputDirectory + clusterFile, 'w') as outfile:
		json.dump(matrix, outfile)