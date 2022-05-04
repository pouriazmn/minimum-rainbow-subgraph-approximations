import Graph

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

def Koch2011(inputGraph):
    n = inputGraph.n()
    H = Graph.Graph(inputGraph.maxColour)
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
            i1 = edge.v1.index
            i2 = edge.v2.index
            if not i1 in H.vertices.keys():
                H.newVertex(i1)
            if not i2 in H.vertices.keys():
                H.newVertex(i2)
            H.addEdge(H.vertices[i1], H.vertices[i2], edge.colour)
            
            if edge.colour in coloursNeeded:
                coloursNeeded.remove(edge.colour) #we no longer need this colour

    return H