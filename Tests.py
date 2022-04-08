import Graph as G
from Greedy import greedy

def generateTestData(startGraph, numGraphs):
    #start with the initial graph
    graphs = []
    graphs.append(startGraph)

    #generate a sequence of random graphs
    for i in range(numGraphs):
        graphs.append(G.randomGraph(graphs[i]))
    return graphs

def writeTestData(testData, fileName):
    testDataString = ""

    #create a string for each test graph
    for graph in testData:
        testDataString += str(graph.n()) + "\n" #num verices first

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

    #parse the string for each test into a graph object
    for testString in testDataStrings:
        if len(testString) > 0:
            graphData = testString.split("\n")

            #create the vertices
            n = int(graphData[0])
            newGraph = G.Graph()
            for i in range(n):
                newGraph.newVertex()

            #create the edges
            for i in range(1, len(graphData)):
                edgeStr = graphData[i]
                if len(edgeStr) > 0:
                    indices = edgeStr.split(",")
                    newGraph.addEdge(newGraph.vertices[int(indices[0])], newGraph.vertices[int(indices[1])], int(indices[2]))

            graphs.append(newGraph)

    return graphs

def runTests(testData, mrsFunction):
    results = []

    for graph in testData:
        print("drawing original graph")
        graph.draw()
        resultGraph = mrsFunction(graph)
        print("drawing rainbow subgraph")
        resultGraph.draw()
        results.append(resultGraph.n())

    return results

def runTestsFromFile(testFile, mrsFunction):
    return runTests(readTestData(testFile), mrsFunction)

#------------------------------------
#test with a cycle as the start graph, can't make n too big or drawing doesn't work
n = 9
startGraph = G.Graph()

for i in range(n):
    startGraph.newVertex()

for i in range(n):
    startGraph.addEdge(startGraph.vertices[i], startGraph.vertices[(i+1) % n], i%3)

print(runTests(generateTestData(startGraph, 4), greedy))