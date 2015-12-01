import snap
from sys import argv

script, treeFile, graphFile, outputDirectory = argv

graph = snap.LoadEdgeList(snap.PUNGraph, graphFile, 0, 1, '\t')

# print graph.GetEdges()

wtData = {}
with open(graphFile,'r') as f:
	for line in f.xreadlines():
		if line[0] == '#':
			continue
		data = line.split()
		k = (int(data[0]), int(data[1]))
		try:
			v = float(data[2])
		except:
			v = 1.0
		wtData[k] = v

outFilePrefix = outputDirectory+'Cluster_'
# outFilePrefix = './input_PR/cluster'
N = 400

def writeToFile(fname, NIdV, idx):
	subG = snap.GetSubGraph(graph, NIdV)
	string = ''
	if idx==1:
		pass
		#print subG.GetEdges()
	for edge in subG.Edges():
		n1 = edge.GetSrcNId()
		n2 = edge.GetDstNId()
		string += '%d\t%d\n' %(n1, n2)
	with open(fname, 'w') as f:
		f.write(string)

with open(treeFile, 'r') as inputFile:
	idx = 1
	# toWrite = ''
	NIdV = snap.TIntV()
	minVal = 1000000
	outFile = outFilePrefix+str(idx)
	for line in inputFile.readlines():
		if line[0] == '#':
			continue
		if idx > N:
			continue
		colon = line.split(':',1)
		clusterNum = int(colon[0])
		nodeId = int(colon[1].split()[-1])
		if clusterNum > idx:
			# with open(outFile,'w') as f:
			# 	f.write(toWrite)
			outFile = outFilePrefix+str(idx)
			writeToFile(outFile, NIdV, idx)
			# if minVal > len(NIdV):
			# 	minVal = len(NIdV)
			# 	print idx, '\t', minVal
			NIdV = snap.TIntV()
			idx += 1
			# toWrite = ''
		if idx > N:
			break
		# toWrite += nodeId+'\n'
		NIdV.Add(nodeId)
