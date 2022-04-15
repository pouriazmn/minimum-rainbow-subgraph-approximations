import copy
import math

import Graph

graph = [
    [0, 0, 0, 4, 0, 3, 0],
    [0, 0, 4, 5, 2, 4, 2],
    [0, 4, 0, 2, 0, 1, 3],
    [4, 5, 2, 0, 3, 2, 1],
    [0, 2, 0, 3, 0, 0, 0],
    [3, 4, 1, 2, 0, 0, 0],
    [0, 2, 3, 1, 0, 0, 0]
]


def print_graph(G):
    for i in range(len(G)):
        print(", ".join(map(str, G[i])))


def print_sub_graph(G, sub):
    for i in sub:
        for j in sub:
            print(G[i][j], end=", ")
        print("")


def sub_graph(G, sub):
    subgraph = []
    for i in sub:
        adjacency = []
        for j in sub:
            adjacency.append(G[i][j])
        subgraph.append(adjacency)
    return subgraph




def distinct_colors_of_sub_graph(G, sub):
    colors = set()
    for i in sub:
        for j in sub:
            if G[i][j] != 0:
                colors.add(G[i][j])
    return len(colors)


def max_color_degree(G, exclude):
    max_, max_i = 0, -1
    for vertex, neighbors_vector in enumerate(G):
        if vertex in exclude:
            continue
        colors = set(filter(lambda x: x != 0, neighbors_vector))
        if len(colors) > max_:
            max_ = len(colors)
            max_i = vertex
    return max_i


def max_color_degree_into_subgraph(G, T, exclude, from_vertices=None):
    max_, max_i = 0, -1
    for vertex, neighbors_vector in enumerate(G):
        if from_vertices and vertex not in from_vertices:
            continue

        if vertex in T or vertex in exclude:
            continue
        colors = set(filter(lambda x: x[0] in T and x[1] != 0, enumerate(neighbors_vector)))
        if len(colors) > max_:
            max_ = len(colors)
            max_i = vertex

    return max_i


def remove_edges(G, vertex):
    colors = set()
    for i in range(len(G)):
        colors.add(G[vertex][i])
        G[vertex][i] = 0
        G[i][vertex] = 0
    for c in colors:
        for i in range(len(G)):
            for j in range(len(G)):
                if G[i][j] == c:
                    G[i][j] = 0
                    G[j][i] = 0
    return G


def procedure_1(G, k):
    half = int(k/2)
    edge_cols = set()
    edges = []
    vertices = set()
    i = 0
    flag = True
    n = len(G)
    while flag and i < n:
        j = 0
        while flag and j < i:
            if G[i][j] != 0 and G[i][j] not in edge_cols:
                edge_cols.add(G[i][j])
                edges.append((i, j))
                vertices.add(i)
                vertices.add(j)
            if len(edges) >= half:
                flag = False
            j += 1
        i += 1

    i = 0
    while len(vertices) < k:
        vertices.add(i)
        i += 1
    return vertices


def procedure_2(G, k):
    G = copy.deepcopy(G)
    G_prime = copy.deepcopy(G)
    T = set()
    T_2 = set()
    for _ in range(int(math.ceil(k/2))):
        max_v = max_color_degree(G_prime, T)
        if max_v == -1:
            break
        T.add(max_v)
        G_prime = remove_edges(G_prime, max_v)

    for _ in range(int(k/2)):
        max_v = max_color_degree_into_subgraph(G, T, T_2)
        if max_v == -1:
            break

        T_2.add(max_v)
        G = remove_edges(G, max_v)

    vertices = T.union(T_2)

    i = 0
    while len(vertices) < k:
        vertices.add(i)
        i += 1
    return vertices


def N_2_v(G, v):
    N_2 = set()
    neighbors_v = list(filter(lambda x: G[v][x] != 0, range(len(G[v]))))
    for n in neighbors_v:
        for vertex in range(len(G[n])):
            if vertex != v and G[n][vertex] != 0 and vertex not in neighbors_v:
                N_2.add(vertex)
    return N_2


def procedure_3_sub(G, k, v):
    G = copy.deepcopy(G)
    G_prime = copy.deepcopy(G)
    N_1 = list(filter(lambda x: G[v][x] != 0, range(len(G[v])))) + [v]
    N_2 = N_2_v(G, v)
    P = set()
    Q = set()
    for _ in range(int(math.ceil(k/2))):
        max_v = max_color_degree_into_subgraph(G, N_1, P, N_2)
        if max_v == -1:
            break
        P.add(max_v)
        G = remove_edges(G, max_v)

    for _ in range(int(k/2)):
        max_v = max_color_degree_into_subgraph(G_prime, P, Q, N_1)
        if max_v == -1:
            break
        Q.add(max_v)
        G_prime = remove_edges(G_prime, max_v)

    vertices = P.union(Q)

    i = 0
    while len(vertices) < k:
        vertices.add(i)
        i += 1
    return vertices


def procedure_3(G, k):
    max_set = set()
    max_set_num = 0
    for v in range(len(G)):
        sub = procedure_3_sub(G, k, v)
        set_num = distinct_colors_of_sub_graph(G, sub)
        if set_num > max_set_num:
            max_set_num = set_num
            max_set = sub

    return max_set


def procedure_4(G, k):
    G = copy.deepcopy(G)
    U = set()
    V = set()
    for _ in range(int(math.ceil(k/2))):
        max_ver = max_color_degree(G, U)
        if max_ver == -1:
            break
        U.add(max_ver)
        # we consider valid colorings so there is no need for removing edges of the same color

    for _ in range(int(k/2)):
        max_v = max_color_degree_into_subgraph(G, U, V)
        if max_v == -1:
            break

        V.add(max_v)
        G = remove_edges(G, max_v)

    vertices = U.union(V)

    i = 0
    while len(vertices) < k:
        vertices.add(i)
        i += 1
    return vertices


def low_degrees_procedure_3(G, k):
    G = copy.deepcopy(G)
    U = set()
    for _ in range(int(math.ceil(k/2))):
        max_ver = max_color_degree(G, U)
        if max_ver == -1:
            break
        U.add(max_ver)

    for vertex in U:
        for i in range(len(G)):
            G[vertex][i] = 0
            G[i][vertex] = 0

    return procedure_3(G, k)


def tirodkar_procedure(G, k):
    a1_ver = procedure_1(G, k)
    a2_ver = procedure_2(G, k)
    a3_ver = low_degrees_procedure_3(G, k)
    a4_ver = procedure_4(G, k)

    vertices = max(a1_ver, a2_ver, a3_ver, a4_ver, key=lambda x: distinct_colors_of_sub_graph(G, x))
    return vertices


def remove_all_colors_present_in_subgraph(G, sub):
    colors = set()
    for i in sub:
        for j in sub:
            if G[i][j] != 0:
                colors.add(G[i][j])
    for i in range(len(G)):
        for j in range(len(G)):
            if G[i][j] in colors:
                G[i][j] = 0
    return G


def tirodkar_mrs_procedure(G):
    p = distinct_colors_of_sub_graph(G, range(len(G)))
    min_n_ver, max_n_ver = int(math.sqrt(p)), min(p * 2 + 1, len(G))

    result_ver = None
    result_n_ver = len(G)
    for k in range(min_n_ver, max_n_ver):
        G_prime = copy.deepcopy(G)
        vertices = tirodkar_procedure(G_prime, k)
        while distinct_colors_of_sub_graph(G, vertices) < p:
            G_prime = remove_all_colors_present_in_subgraph(G_prime, vertices)
            new_it = tirodkar_procedure(G_prime, k)
            vertices = vertices.union(new_it)

        if len(vertices) < result_n_ver:
            result_n_ver = len(vertices)
            result_ver = vertices

    return result_ver


def Tirodkar2017(G: Graph.Graph):
    graph = G.to_adjacency_matrix()
    result = tirodkar_mrs_procedure(graph)
    subgraph = sub_graph(graph, result)
    return Graph.Graph.from_adjacency_matrix(subgraph)


if __name__ == '__main__':
    ver = tirodkar_mrs_procedure(graph)
    print(ver)
    print_graph(sub_graph(graph, ver))
