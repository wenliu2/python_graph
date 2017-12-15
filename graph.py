#!/usr/bin/env python
import json

class Graph():
    def __init__(self):
        '''initialize Graph'''
        pass

    def fromFile(self, fileName):
        """
        load graph from json file and convert it to data structure
        needed by Dijkstra function (self.G)
        """
        self.fileName = fileName
        self.G = {}
        with open(fileName) as jsonFile:
            self.fileJsonData = json.load(jsonFile)
            self.fileJsonData["comments"] = "" #remove comments
            innerData = self.convertToInnerData(self.fileJsonData) 
            self.G = self.convertToDijkstraData(innerData)
        return self.G

    def convertToInnerData(self, fileJsonData):
        innerData = {}
        for node in fileJsonData["nodes"]:
            (name, data) = (node["id"], node["data"])
            if name in innerData:
                print("Warning: duplicate node: %s, it will be skippted." % name)
                continue
            innerData[name] = {"data":data, "edges":{}}
        for edge in fileJsonData["edges"]:
            (start, end, distance) = (edge["start"], edge["end"], edge["distance"])
            if start not in innerData:
                print("Warning: start node of edge (%s, %s) is not defined, it will be skipped" % (start, end))
                continue
            innerData[start]["edges"][end] = {"distance": distance}
        return innerData;
        #self.innerData = innerData

    def convertToDijkstraData(self, innerData):
        G = {}
        for node in innerData.keys():
            G[node] = {}
            edges = innerData[node]["edges"]
            for edge in edges.keys():
                G[node][edge] = edges[edge]["distance"]
        return G

    def shortestPath(self, start, end):
        return shortestPath(self.G, start, end)


# Dijkstra's algorithm for shortest paths
# David Eppstein, UC Irvine, 4 April 2002

# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117228
from priodict import priorityDictionary

def Dijkstra(G,start,end=None):
	"""
	Find shortest paths from the start vertex to all
	vertices nearer than or equal to the end.

	The input graph G is assumed to have the following
	representation: A vertex can be any object that can
	be used as an index into a dictionary.  G is a
	dictionary, indexed by vertices.  For any vertex v,
	G[v] is itself a dictionary, indexed by the neighbors
	of v.  For any edge v->w, G[v][w] is the length of
	the edge.  This is related to the representation in
	<http://www.python.org/doc/essays/graphs.html>
	where Guido van Rossum suggests representing graphs
	as dictionaries mapping vertices to lists of neighbors,
	however dictionaries of edges have many advantages
	over lists: they can store extra information (here,
	the lengths), they support fast existence tests,
	and they allow easy modification of the graph by edge
	insertion and removal.  Such modifications are not
	needed here but are important in other graph algorithms.
	Since dictionaries obey iterator protocol, a graph
	represented as described here could be handed without
	modification to an algorithm using Guido's representation.

	Of course, G and G[v] need not be Python dict objects;
	they can be any other object that obeys dict protocol,
	for instance a wrapper in which vertices are URLs
	and a call to G[v] loads the web page and finds its links.
	
	The output is a pair (D,P) where D[v] is the distance
	from start to v and P[v] is the predecessor of v along
	the shortest path from s to v.
	
	Dijkstra's algorithm is only guaranteed to work correctly
	when all edge lengths are positive. This code does not
	verify this property for all edges (only the edges seen
 	before the end vertex is reached), but will correctly
	compute shortest paths even for some graphs with negative
	edges, and will raise an exception if it discovers that
	a negative edge has caused it to make a mistake.
	"""

	D = {}	# dictionary of final distances
	P = {}	# dictionary of predecessors
	Q = priorityDictionary()   # est.dist. of non-final vert.
	Q[start] = 0
	
	for v in Q:
		D[v] = Q[v]
		if v == end: break
		
		for w in G[v]:
			vwLength = D[v] + G[v][w]
			if w in D:
				if vwLength < D[w]:
					raise ValueError, \
  "Dijkstra: found better path to already-final vertex"
			elif w not in Q or vwLength < Q[w]:
				Q[w] = vwLength
				P[w] = v
	
	return (D,P)
			
def shortestPath(G,start,end):
	"""
	Find a single shortest path from the given start vertex
	to the given end vertex.
	The input has the same conventions as Dijkstra().
	The output is a list of the vertices in order along
	the shortest path.
	"""

	D,P = Dijkstra(G,start,end)
	Path = []
	while 1:
		Path.append(end)
		if end == start: break
		end = P[end]
	Path.reverse()
	return Path

if __name__ == "__main__":
    #print("graph start")
    graph = Graph()
    graph.fromFile("./sample/graph1.json")
    #print("file name: %s" % graph.fileName)
    #print("json object: %s" % graph.fileJsonData )
    #print("inner object: %s" % graph.innerData )
    #print("G object: %s" % graph.G)
    path = graph.shortestPath("a","h")
    print("shortestPath: %s" % path)
