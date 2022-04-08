import Graph as G

def computeValues(inputGraph, coloursNeeded):
    n = inputGraph.n()
    value = [0] * n
    newEdges = []
    for i in range(n):
        newEdges.append([])

    for i in range(n):
        vertex = inputGraph.vertices[i]
        incidentColours = []
        for edge in vertex.incidentEdges:
            if edge.colour in coloursNeeded and not edge.colour in incidentColours:
                value[i]+=1
                newEdges[i].append(edge)
                incidentColours.append(edge.colour)
    return value, newEdges

def greedy(inputGraph):
    n = inputGraph.n()
    H = G.Graph()
    coloursNeeded = []

    for edge in inputGraph.edges:
        if not edge.colour in coloursNeeded:
            coloursNeeded.append(edge.colour)

    while len(coloursNeeded) > 0:
        #find the value of each vertex
        value, incidentEdges = computeValues(inputGraph, coloursNeeded)

        #find the vertex of the maximum value
        maxValue = -1
        maxI = -1
        for i in range(n):
            if value[i] > maxValue:
                maxValue = value[i]
                maxI = i

        #add the vertex and all the new edges to the output graph
        newVertex = inputGraph.vertices[maxI]
        newEdges = incidentEdges[maxI]

        for edge in newEdges:
            assert(newVertex == edge.v1 or newVertex == edge.v2)
            if not edge.v1 in H.vertices:
                H.addVertex(edge.v1)
            if not edge.v2 in H.vertices:
                H.addVertex(edge.v2)
            H.addEdge(edge.v1, edge.v2, edge.colour)
            
            if edge.colour in coloursNeeded:
                coloursNeeded.remove(edge.colour) #we no longer need this colour

    return H