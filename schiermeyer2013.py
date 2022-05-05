import copy
from max_matching import Match
import Graph


def find_first_appearance_of_colour(graph, c):
    n = len(graph)
    for i in range(n):
        for j in range(n):
            if graph[i][j] == c:
                return i, j
    raise ValueError(f"colour {c} is not presented in graph")



def find_adjacent_edges(graph, c1, c2):
    n = len(graph)
    for i in range(n):
        for j in range(n):
            if graph[i][j] == c1:
                for k in range(n):
                    if graph[j][k] == c2:
                        return i, j, k
    return False


def match_colors_greedy(graph: Graph.Graph, colours):
    print("----------------------------------")
    # construct colours matching graph
    p = graph.num_colours
    colours_edges = []
    colours_graph_paths = [[0 for _ in range(p)] for _ in range(p)]
    print(f"{p} colors, size: {graph.n()}")
    for i in range(p):
        for j in range(i):
            joined_vertices = graph.find_adjacent_vertices_with_colours(colours[i], colours[j])
            if joined_vertices:
                colours_edges.append((i, j))
                colours_edges.append((j, i))
                colours_graph_paths[i][j] = joined_vertices
                colours_graph_paths[j][i] = joined_vertices

    print(colours_edges)
    # do the matching
    match = Match.from_edges(p, colours_edges)
    match.maximum_matching()
    # construct MRS
    n = graph.n()
    graph_h_nodes = set()

    matched_colours = []
    not_matched_colours = []
    for node in match.nodes:
        if node.mate is not None:
            if node.index < node.mate.index:
                c1, c2 = node.index, node.mate.index
                matched_colours.append((c1, c2))
        else:
            not_matched_colours.append(node.index)

    print(matched_colours)
    for c1, c2 in matched_colours:
        print(c1, c2)
        v1, v2, v3 = colours_graph_paths[c1][c2]
        graph_h_nodes.add(v1)
        graph_h_nodes.add(v2)
        graph_h_nodes.add(v3)

    for c in not_matched_colours:
        edge = graph.colours[c].pop()
        graph.colours[c].add(edge)
        graph_h_nodes.add(edge.v1)
        graph_h_nodes.add(edge.v2)

    print(f"result k = {len(graph_h_nodes)}, {graph_h_nodes}")
    return graph_h_nodes


def Schiermeyer2013(graph: Graph.Graph):
    colors = graph.colours.keys()
    result = match_colors_greedy(graph, list(colors))
    subgraph = graph.induced_sub_graph(result)
    return subgraph
