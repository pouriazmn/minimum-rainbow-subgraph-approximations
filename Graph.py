import random
from collections import defaultdict
from typing import List, Dict, Iterable

import networkx as nx
from matplotlib import pyplot as plt


class Vertex:
    # create a vertex
    def __init__(self, index):
        self.index = index
        self.incidentEdges = set()
        self._neighbours = defaultdict(set)
        self._colours = defaultdict(set)

    @property
    def neighbours(self):
        return set(self._neighbours.keys())
    # check how many edges this vertex is incident to
    def degree(self):
        return len(self.incidentEdges)

    @property
    def colours(self):
        return self._colours

    @property
    def colour_degree(self):
        return len(self._colours)

    def colour_degree_into_sub_graph(self, vertices):
        return len(self.colours_into_sub_graph(vertices))

    def colours_into_sub_graph(self, vertices):
        colours = set()
        for vertex in vertices:
            for edge in self._neighbours.get(vertex, []):
                colours.add(edge.colour)
        return colours

    def edges_into_sub_graph(self, vertices):
        edges = list()
        for vertex in vertices:
            for edge in self._neighbours.get(vertex, []):
                edges.append(edge)
        return edges


    # add a new edge we are incident to
    def addEdge(self, newEdge):
        assert (newEdge.v1 is self or newEdge.v2 is self)
        self.incidentEdges.add(newEdge)
        self._colours[newEdge.colour].add(newEdge)
        if newEdge.v1 is self:
            self._neighbours[newEdge.v2].add(newEdge)
        else:
            self._neighbours[newEdge.v1].add(newEdge)

    def removeEdge(self, edge):
        assert (edge.v1 is self or edge.v2 is self)
        self.incidentEdges.remove(edge)
        self._colours[edge.colour].remove(edge)
        if len(self._colours[edge.colour]) == 0:
            del self._colours[edge.colour]
        if edge.v1 is self:
            self._neighbours[edge.v2].remove(edge)
            if len(self._neighbours[edge.v2]) == 0:
                del self._neighbours[edge.v2]
        else:
            self._neighbours[edge.v1].remove(edge)
            if len(self._neighbours[edge.v1]) == 0:
                del self._neighbours[edge.v1]

    def __str__(self):
        return f"<{self.index}>"

    def __repr__(self):
        return f"<{self.index}>"


class Edge:

    # create an edge between v1 and v2 with a specific colour
    def __init__(self, v1: Vertex, v2: Vertex, colour):
        self.v1: Vertex = v1
        self.v2: Vertex = v2
        self.colour = colour

    def equal(self, other):
        return self.colour == other.colour and \
               (self.v1 == other.v1 and self.v2 == other.v2) or (self.v1 == other.v2 and self.v2 == other.v1)

    def __hash__(self):
        return hash(id(self))

    def __bool__(self):
        return True

    def __str__(self):
        return f"({self.v1}, {self.v2}, {self.colour})"

    def __repr__(self):
        return f"({self.v1}, {self.v2}, {self.colour})"


class Graph:

    # create an empty graph
    def __init__(self, maxColour=None, name=None):
        self.name = name
        self._vertex_index = 0
        self.vertices: Dict[int][Vertex] = dict()
        self.edges: List[Edge] = []
        self.colours = defaultdict(set)
        self.degrees = defaultdict(list)
        self.maxColour = maxColour

    @property
    def num_colours(self):
        return len(self.colours.keys())

    def max_colour_degree(self):
        vertex = max(self.vertices.values(), key=lambda v: v.colour_degree)
        return vertex

    def max_colour_degree_into_subgraph(self, sub_vertices: List[Vertex], from_vertices: List[Vertex] = None):
        if from_vertices:
            vertex = max(from_vertices, key=lambda v: v.colour_degree_into_sub_graph(sub_vertices))
        else:
            vertex = max(self.vertices.values(), key=lambda v: v.colour_degree_into_sub_graph(sub_vertices))
        return vertex

    def keep_only_one_edge_of_each_colour(self, vertex: Vertex):
        remove_edges = set()
        keep_edges = set()
        for colour in vertex.colours.keys():
            keep = vertex.colours[colour].pop()
            keep_edges.add(keep)
            remove_edges = remove_edges.union(vertex.colours[colour])
            vertex.colours[colour].add(keep)

        for edge in keep_edges:
            if edge.v1 == vertex:
                neigh = edge.v2
            else:
                neigh = edge.v1
            for rem_edge in neigh.colours[edge.colour]:
                if rem_edge != edge:
                    remove_edges.add(rem_edge)

        for edge in remove_edges:
            self.removeEdge(edge)

    def remove_all_colours_incident_to_vertex(self, vertex: Vertex):
        edges = set(vertex.incidentEdges)
        for colour in vertex.colours.keys():
            edges = edges.union(self.colours[colour])

        for edge in edges:
            self.removeEdge(edge)

    def distinct_colours_of_subgraph(self, sub_vertices: Iterable[Vertex]):
        colours = set()
        for vertex in sub_vertices:
            colours = colours.union(vertex.colours_into_sub_graph(sub_vertices))
        return colours

    def vertices_by_index(self, indices: Iterable[int]):
        vertices = []
        for index in indices:
            vertices.append(self.vertices[index])
        return vertices

    def remove_all_colours_in_sub_graph(self, sub_vertices: Iterable[Vertex]):
        colours = self.distinct_colours_of_subgraph(sub_vertices)
        remove_edges = []
        for c in colours:
            remove_edges.extend(self.colours[c])

        for edge in remove_edges:
            self.removeEdge(edge)

    def induced_sub_graph(self, sub_vertices):
        sub_graph = self.__class__(name=f"{self.name}-sub")
        edges = set()
        for vertex in sub_vertices:
            sub_graph.newVertex(vertex.index)
            for edge in vertex.edges_into_sub_graph(sub_vertices):
                edges.add((edge.v1.index, edge.v2.index, edge.colour))

        for e in edges:
            v1 = sub_graph.vertices[e[0]]
            v2 = sub_graph.vertices[e[1]]
            c = e[2]
            sub_graph.addEdge(v1, v2, c)

        return sub_graph

    # get the number of vertices in the graph
    def n(self):
        return len(self.vertices)

    # get the number of edges in the graph
    def m(self):
        return len(self.edges)

    @property
    def vertex_index(self):
        while self._vertex_index in self.vertices.keys():
            self._vertex_index += 1
        return self._vertex_index

    # add a new vertex to the graph
    def newVertex(self, index=None):
        if index is None:
            index = self.vertex_index
        if index in self.vertices.keys():
            raise ValueError(f"Index {index} already exists in the graph")
        v = Vertex(index)
        self.vertices[v.index] = v
        self.degrees[0].append(v)
        return v

    # connect vertices u and v with an edge of a specified colour
    def addEdge(self, u: Vertex, v: Vertex, colour):
        assert self.vertices[v.index] is v and self.vertices[u.index] is u
        if(u is not v):
            self.degrees[v.degree()].remove(v)
            self.degrees[u.degree()].remove(u)
            newEdge = Edge(u, v, colour)
            self.edges.append(newEdge)
            u.addEdge(newEdge)
            v.addEdge(newEdge)
            self.colours[colour].add(newEdge)
            self.degrees[v.degree()].append(v)
            self.degrees[u.degree()].append(u)

    def removeEdge(self, edge: Edge):
        assert edge is not None
        self.degrees[edge.v1.degree()].remove(edge.v1)
        self.degrees[edge.v2.degree()].remove(edge.v2)
        self.edges.remove(edge)
        edge.v1.removeEdge(edge)
        edge.v2.removeEdge(edge)
        self.colours[edge.colour].remove(edge)
        if len(self.colours[edge.colour]) == 0:
            del self.colours[edge.colour]
        self.degrees[edge.v1.degree()].append(edge.v1)
        self.degrees[edge.v2.degree()].append(edge.v2)

    # check if vertices u and v are connected by at least one edge
    def adjacent(self, u: Vertex, v: Vertex):
        assert self.vertices[v.index] is v and self.vertices[u.index] is u
        return u in v.neighbours

    def toNX(self):
        nx_graph = nx.MultiGraph()

        for e in self.edges:
            nx_graph.add_edge(e.v1, e.v2, color=e.colour)

        return nx_graph

    def draw(self):
        selfNX = self.toNX()
        selfcolors = list(nx.get_edge_attributes(selfNX, name='color').values())
        nx.draw(selfNX, edge_color=selfcolors)
        plt.show()

    @classmethod
    def from_adjacency_matrix(cls, adjacency_matrix):
        graph = cls()

        n = len(adjacency_matrix)
        for i in range(n):
            graph.newVertex(i)
        for i in range(n):
            for j in range(n):
                if adjacency_matrix[i][j] != 0:
                    color = adjacency_matrix[i][j]
                    graph.addEdge(graph.vertices[i], graph.vertices[j], color)
        return graph

    def copy(self):
        newGraph = Graph()
        for index in self.vertices.keys():
            newGraph.newVertex(index)

        for edge in self.edges:
            v1 = newGraph.vertices[edge.v1.index]
            v2 = newGraph.vertices[edge.v2.index]
            newGraph.addEdge(v1, v2, edge.colour)

        return newGraph


def rewire(G):
    m = G.m()

    # find the first edge
    edgeNum = random.randint(0, m - 1)
    edge = G.edges[edgeNum]

    # find the first two vertices
    vertexNum = random.randint(0, 1)
    if vertexNum == 0:
        u1 = edge.v1
        v = edge.v2
    else:
        u1 = edge.v2
        v = edge.v1

    vertexDegree = u1.degree()
    u2 = None
    w = None
    otherEdge = None

    #find all the eligible edges
    eligibleEdges = []
    for vertex in G.degrees[vertexDegree]:
        for potentialEdge in vertex.incidentEdges:
            if not potentialEdge in eligibleEdges and potentialEdge is not edge:
                eligibleEdges.append(potentialEdge)

    #if there is an eligible edge, pick one
    if len(eligibleEdges) > 0:
        otherEdge = eligibleEdges[random.randint(0, len(eligibleEdges)-1)]
    
        if otherEdge.v1.degree() == vertexDegree:
            u2 = otherEdge.v1
            w = otherEdge.v2
        else:
            u2 = otherEdge.v2
            w = otherEdge.v1
    
    #otherwise, choose an edge uniformly at random
    else:
        otherEdge = edge
        while otherEdge is edge:
            otherEdge = G.edges[random.randint(0, len(G.edges)-1)]

        if otherEdge.v1 is u1:
            u2 = otherEdge.v2
            w = otherEdge.v1
        else:
            u2 = otherEdge.v1
            w = otherEdge.v2

    G.removeEdge(edge)
    G.removeEdge(otherEdge)

    G.addEdge(u1, w, edge.colour)
    G.addEdge(u2, v, otherEdge.colour)


def randomGraph(G):
    k = G.m()
    newGraph = G.copy()

    for _ in range(k):
        rewire(newGraph)
    return newGraph