from os import listdir
from os.path import isfile, join
import snap

inputDir = './input_PR'
outputDir = './output_PR'

inFiles = [f for f in listdir(inputDir) 
	if isfile(join(inputDir,f)) ]

for clusterFile in inFiles:
	binData = snap.TFIn(join(inputDir,clusterFile))
	graph = snap.TUNGraph.Load(binData)
	PRankH = snap.TIntFltH()
	snap.GetPageRank(graph, PRankH)
	with open(join(outputDir,clusterFile),'w') as f:
		for item in PRankH:
		    f.write(str(item)+'\t'+str(PRankH[item])+'\n')
		    