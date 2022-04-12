import Graph as G
import math as m
import random

def generateTestData(startGraph, numGraphs):
    #start with the initial graph
    graphs = []
    graphs.append(startGraph)

    #generate a sequence of random graphs
    for i in range(numGraphs):
        graphs.append(G.randomGraph(graphs[i]))
    return graphs

def writeTestData(testData, fileName):
    graphs = testData[0]
    size = testData[1]
    density = testData[2]
    maxColour = testData[3]

    testDataString = str(size) + "," + str(density) + "," + str(maxColour) + "#\n"
    #create a string for each test graph
    for graph in graphs:

        #write each edge
        for edge in graph.edges:
            testDataString += str(graph.vertices.index(edge.v1)) + "," + str(graph.vertices.index(edge.v2)) + "," + str(edge.colour) + "\n"
        testDataString += "#" #between the graphs
    
    #write to the file
    file = open(fileName, "w")
    file.write(testDataString)
    file.close()

def readTestData(fileName):
    #open the file containing the test data
    file = open(fileName, "r")
    testDataString = file.read()
    file.close()

    graphs = []

    #split the string into the strings for each test
    testDataStrings = testDataString.split("#")
    params = testDataStrings[0].split(",")
    size = int(params[0])
    density = int(params[1])
    maxColour = int(params[2])

    #parse the string for each test into a graph object
    for i in range(1, len(testDataStrings)):
        testString = testDataStrings[i]

        if len(testString) > 0:
            graphData = testString.split("\n")

            newGraph = G.Graph()
            #create the vertices
            for i in range(size):
                newGraph.newVertex()

            #create the edges
            for i in range(1, len(graphData)):
                edgeStr = graphData[i]
                if len(edgeStr) > 0:
                    indices = edgeStr.split(",")
                    newGraph.addEdge(newGraph.vertices[int(indices[0])], newGraph.vertices[int(indices[1])], int(indices[2]))

            graphs.append(newGraph)

    return [graphs, size, density, maxColour]

def runTests(testData, mrsFunction, draw=False):
    results = []

    graphs = testData[0]
    size = testData[1]
    density = testData[2]
    maxColour = testData[3]
    for graph in graphs:
        if(draw):
            print("drawing original graph")
            graph.draw()
        resultGraph = mrsFunction(graph)

        if(draw):
            print("drawing rainbow subgraph")
            resultGraph.draw()
        
        results.append(resultGraph.n())

    return [results, size, density, maxColour]

def runTestsFromFile(testFile, mrsFunction, draw=False):
    return runTests(readTestData(testFile), mrsFunction, draw=draw)

sizes = [10, 50, 100, 200, 500, 1000]
def generateStartingGraphs():
    graphs = []

    #walk through all sizes
    for size in sizes:
        #walk through all edge densities
        for edgeDensity in range(10, 90, 10):
            edgeDensityFraction = edgeDensity / 100
        
            #figure out what the colour parameters will be
            maxColours = int(m.sqrt(size))
            if(maxColours < 5):
                maxColours = 6
            colourStep = m.ceil((maxColours - 5) / 5)
            if colourStep < 1:
                colourStep = 1

            #walk through the numbers of colours
            for numColours in range(5, maxColours, colourStep):
                #generate the vertices of the graph
                newGraph = G.Graph()
                for i in range(size):
                    newGraph.newVertex()

                #generate the edges
                for u in newGraph.vertices:
                    for v in newGraph.vertices:
                        edgeProbability = random.random()
                        if edgeProbability < edgeDensityFraction:
                            newGraph.addEdge(u, v, 0)

                #generate the colours
                toBeColoured = newGraph.edges.copy()
                colourNum = 0
                while len(toBeColoured) > 0:
                    edgeIndex = random.randint(0, len(toBeColoured)-1)
                    toBeColoured[edgeIndex].colour = colourNum
                    colourNum = (colourNum + 1) % (numColours+1)
                    toBeColoured.remove(toBeColoured[edgeIndex])

                graphs.append([newGraph, size, edgeDensity, numColours])
    return graphs

startGraphs = generateStartingGraphs()
print("starting graphs done")

for startGraph in startGraphs:
    graphs = generateTestData(startGraph[0], 100)
    testData = [graphs, startGraph[1], startGraph[2], startGraph[3]]
    writeTestData(testData, "TEST_" + str(startGraph[1]) + "_" + str(startGraph[2]) + "_" + str(startGraph[3]) + ".txt")