import copy
from max_matching import Match
from tirodkar import *


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


def match_colors_greedy(graph, colours):
    print("----------------------------------")
    # construct colours matching graph
    p = len(colours)
    colours_edges = []
    colours_graph_paths = [[0 for _ in range(p)] for _ in range(p)]
    print(f"{p} colors, size: {len(graph)}")
    print_graph(graph)
    for i in range(p):
        for j in range(i):
            path = find_adjacent_edges(graph, colours[i], colours[j])
            if path:
                colours_edges.append((i, j))
                colours_edges.append((j, i))
                colours_graph_paths[i][j] = path
                colours_graph_paths[j][i] = path

    print(colours_edges)
    # do the matching
    match = Match.from_edges(p, colours_edges)
    match.maximum_matching()
    # construct MRS
    n = len(graph)
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
        v1, v2 = find_first_appearance_of_colour(graph, colours[c])
        graph_h_nodes.add(v1)
        graph_h_nodes.add(v2)

    print(f"result k = {len(graph_h_nodes)}, {graph_h_nodes}")
    print_sub_graph(graph, graph_h_nodes)
    return graph_h_nodes


def Schiermeyer2013(G: Graph.Graph):
    graph = G.to_adjacency_matrix()
    colors = set()
    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph[i][j] != 0:
                colors.add(graph[i][j])
    result = match_colors_greedy(graph, list(colors))
    subgraph = sub_graph(graph, result)
    color_size = distinct_colors_of_sub_graph(graph, result)
    return Graph.Graph.from_adjacency_matrix(subgraph, color_size)

if __name__ == "__main__":
    mrs_sub = match_colors_greedy(graph, [1, 2, 3, 4, 5])
    print(mrs_sub)
    print_sub_graph(graph, mrs_sub)
