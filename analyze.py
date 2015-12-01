from os import listdir
from os.path import isfile, join
import networkx as nx
import matplotlib.pyplot as plt
import snap

inputDir = './UnanalyzedClusters/'
outDirPR = './PageRankedClusters/'
outDirK = './KCoredClusters/'
outDirCentrality = './CentrClusters/'

inFiles = [f for f in listdir(inputDir) 
	if isfile(join(inputDir,f)) ]
inFiles = ['cluster124']

def pageRank(G):
	pagerank = nx.pagerank(G, weight='weight', max_iter=100) # Returns dictionary
	# print pagerank	
	f = open(outDirPR + clusterFile, 'w')
	for key, value in sorted(pagerank.iteritems(),key=lambda x:(-x[1],x[0])):
		f.write(str(key) + '\t' + str(value) +'\n')

def KCored(G):
	# Set k value
	k_values = []
	# k = 0.0
	nodes = G.nodes()
	for node in nodes:
		k_values.append(G.degree(node))
	k_values = sorted(k_values)
	k = k_values[len(k_values)/2]
	# print clusterFile, k
	# print min(k_values)
	# print max(k_values)	
	subG = nx.k_core(G, k=k) # Returns subgraph
	# print len(G.nodes()), '\t', len(subG.nodes())
	nx.write_weighted_edgelist(subG, outDirK + clusterFile, 'w')

def plltr(k_values):
	fig1 = plt.figure()
	# ax1 = fig1.add_subplot(1,1,1)
	# ax1.set_yscale('log')
	# ax1.set_xscale('log')
	# ax1.set_ylim(bottom=0.8, top = 1e05)
	plt.hist(k_values)
	plt.savefig('Q3d_2.eps', format='eps', dpi=1000)
	plt.savefig('Q3d_2.png')

def centralityMeasures(G):
	# Betweenness
	# betw = nx.betweenness_centrality(G, normalized=True, weight='weight')
	# print sorted([(k,v) for k,v in betw.iteritems()], key= lambda x:(-x[1],x[0]))

	# clsn = nx.closeness_centrality(G, normalized=True)
	# print sorted([(k,v) for k,v in clsn.iteritems()], key= lambda x:(-x[1],x[0]))

	# evec = nx.eigenvector_centrality(G, weight='weight')
	# print sorted([(k,v) for k,v in evec.iteritems()], key= lambda x:(-x[1],x[0]))

	katz = nx.katz_centrality(G, normalized=True, weight='weight', alpha=0.005)
	print sorted([(k,v) for k,v in katz.iteritems()], key= lambda x:(-x[1],x[0]))

def getDistance(GSnap):
	matrix = dict()
	for node in GSnap.Nodes():
		hop = 0
		flag = True
		while flag == True:
			hop += 1
			flag = False
			NodeVec = snap.TIntV()
			# print type(node.GetId())
			# print '---------------'
			snap.GetNodesAtHop(GSnap, node.GetId(), hop, NodeVec, False)
			# print 'g'
			for item in NodeVec:
				flag = True
				if not node.GetId() in matrix:
					matrix[node.GetId()] = dict()
				matrix[node.GetId()][item] = hop					
				# print 'i'
	print matrix


for clusterFile in inFiles:
	G = nx.read_weighted_edgelist(inputDir+clusterFile, comments='#', nodetype=int)

	print "Loaded " + clusterFile
	# pageRank(G)
	centralityMeasures(G)
	# GSnap = snap.LoadEdgeList(snap.PUNGraph, inputDir + clusterFile, 0, 1, '\t')
	# getDistance(GSnap)

