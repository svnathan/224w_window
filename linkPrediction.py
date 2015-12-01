import snap
from sys import argv
import pickle
import networkx as nx


# TODO: Generate itemNodeIds, userNodeIds
def predictLinksJaccard(GCombined, nodesAtHop, itemNodeIds, userNodeIds, directory):
    nodesToNeighbors = {}
    for node in GCombined.Nodes():
        NodeVec = snap.TIntV()
        snap.GetNodesAtHop(GCombined, node.GetId(), 1, NodeVec, False)
        nodesToNeighbors[node.GetId()] = NodeVec
    
    scores = {} 
    for node1 in userNodeIds:
        for node2 in itemNodeIds:
            if not GCombined.IsNode(node1) or not GCombined.IsNode(node2) or GCombined.IsEdge(node1, node2):
                if not node1 in scores:
                    scores[node1] = {}
                scores[node1][node2] = 0.0
            else:
                neigborsInCommon = len(set.intersection(set(nodesToNeighbors[node1]), set(nodesToNeighbors[node2])))
                neighborUnion = len(set.union(set(nodesToNeighbors[node1]), set(nodesToNeighbors[node2])))
                if not node1 in scores:
                    scores[node1] = {}
                scores[node1][node2] = float(neigborsInCommon)/float(neighborUnion)
            
    with open(directory + 'Jaccards', 'wb') as outfile:
        pickle.dump(scores, outfile)
                

def predictLinksNegatedShortestPath(GCombined, nodesAtHop, itemNodeIds, userNodeIds, directory):
    scores = {} 
    for node1 in userNodeIds:
        for node2 in itemNodeIds:
            if not GCombined.IsNode(node1) or not GCombined.IsNode(node2) or GCombined.IsEdge(node1, node2):
                if not node1 in scores:
                    scores[node1] = {}
                scores[node1][node2] = 0.0
            else:
                if not node1 in scores:
                    scores[node1] = {}
                scores[node1][node2] = 1.0/snap.GetShortPath(GCombined, node1, node2, False)
    with open(directory + 'NegatedShortestPath', 'wb') as outfile:
        pickle.dump(scores, outfile)
    
def predictLinksAdamicAdar(nodesAtHop, itemNodeIds, userNodeIds, directory, item):
    scores = {}
    GCombined = nx.read_edgelist(directory + 'Edge_List_Combined_' + item + '.txt')
    preds = nx.adamic_adar_index(GCombined)
        
    for u, v, p in preds:
        if not u in scores:
            scores[u] = {}
        scores[u][v] = p
    
    with open(directory + 'AdamicAdar', 'wb') as outfile:
        pickle.dump(scores, outfile)
    