import copy
import math

import Graph


def procedure_1(graph: Graph.Graph, k):
    half = int(k/2)
    edges = []
    for colour in graph.colours.keys():
        if len(graph.colours[colour]) == 0:
            print(f"graph `{graph.name}` does not have any edge with colour `{colour}`, although it should")
            continue
        edge = graph.colours[colour].pop()
        graph.colours[colour].add(edge)
        edges.append(edge)

    edges = edges[:min(half, len(edges))]

    vertices = set()
    for edge in edges:
        vertices.add(edge.v1.index)
        vertices.add(edge.v2.index)

    for v_ind in graph.vertices.keys():
        if len(vertices) < k:
            vertices.add(v_ind)

    return vertices


def procedure_2(graph: Graph.Graph, k):

    graph = graph.copy()
    g_prime = graph.copy()
    T = set()
    T_2 = set()

    for _ in range(int(math.ceil(k/2))):
        max_v = g_prime.max_colour_degree()
        T.add(max_v.index)
        g_prime.remove_all_colours_incident_to_vertex(max_v)

    t_sub_graph_vertices = graph.vertices_by_index(T)

    for _ in range(int(k/2)):

        max_v = graph.max_colour_degree_into_subgraph(t_sub_graph_vertices)
        T_2.add(max_v.index)
        graph.remove_all_colours_incident_to_vertex(max_v)

    vertices = T.union(T_2)

    for v_ind in graph.vertices.keys():
        if len(vertices) < k:
            vertices.add(v_ind)

    return vertices


def procedure_3_sub(graph: Graph.Graph, k, vertex_ind):
    graph = graph.copy()
    g_prime = graph.copy()
    N_1 = graph.vertices[vertex_ind].neighbours
    N_2 = set()
    for vertex in N_1:
        N2 = N_2.union(vertex.neighbours)

    N_2.difference_update(N_1)

    P = set()
    Q = set()
    for _ in range(int(math.ceil(k/2))):
        max_v = graph.max_colour_degree_into_subgraph(sub_vertices=N_1, from_vertices=N_2)
        P.add(max_v.index)
        graph.remove_all_colours_incident_to_vertex(max_v)

    p_sub_graph_vertices = g_prime.vertices_by_index(P)
    N_1_g_prime = g_prime.vertices_by_index([v.index for v in N_1])

    for _ in range(int(k/2)):
        max_v = g_prime.max_colour_degree_into_subgraph(sub_vertices=p_sub_graph_vertices, from_vertices=N_1_g_prime)
        Q.add(max_v.index)
        g_prime.remove_all_colours_incident_to_vertex(max_v)

    vertices = P.union(Q)

    for v_ind in graph.vertices.keys():
        if len(vertices) < k:
            vertices.add(v_ind)

    return vertices


def procedure_3(graph, k, U=None):
    if U is None:
        U = graph.vertices.keys()
    max_sub_graph = set()
    max_colour_num = 0
    for v_ind in U:
        sub = procedure_3_sub(graph, k, v_ind)
        sub_graph_vertices = graph.vertices_by_index(sub)

        colours_set = graph.distinct_colours_of_subgraph(sub_graph_vertices)
        if len(colours_set) > max_colour_num:
            max_sub_graph = sub
            max_colour_num = len(colours_set)

    return max_sub_graph


def procedure_4(graph, k):
    original = graph
    graph = graph.copy()
    g_prime = graph.copy()
    U = set()
    U_vertices = set()
    V_prime = set()
    V = set()
    for _ in range(int(math.ceil(k/2))):
        max_v = graph.max_colour_degree()
        graph.keep_only_one_edge_of_each_colour(max_v)
        U.add(max_v.index)
        U_vertices.add(max_v)

    for _ in range(int(k / 2)):
        max_v = graph.max_colour_degree_into_subgraph(U_vertices)
        V.add(max_v.index)
        graph.remove_all_colours_incident_to_vertex(max_v)

    u_sub_graph_vertices = g_prime.vertices_by_index(U)

    for _ in range(int(k/2)):
        max_v = g_prime.max_colour_degree_into_subgraph(u_sub_graph_vertices)
        V_prime.add(max_v.index)
        g_prime.remove_all_colours_incident_to_vertex(max_v)

    vertices = U.union(V)
    for v_ind in original.vertices.keys():
        if len(vertices) < k:
            vertices.add(v_ind)

    vertices_prime = U.union(V_prime)
    for v_ind in original.vertices.keys():
        if len(vertices_prime) < k:
            vertices_prime.add(v_ind)

    sub_graph_vertices = original.vertices_by_index(vertices)
    sub_graph_vertices_prime = original.vertices_by_index(vertices_prime)

    colours_set = original.distinct_colours_of_subgraph(sub_graph_vertices)
    colours_set_prime = original.distinct_colours_of_subgraph(sub_graph_vertices_prime)
    if len(colours_set) > len(colours_set_prime):
        return vertices, U
    else:
        return vertices_prime, U


def tirodkar_procedure(graph, k):
    a1_ver = procedure_1(graph, k)
    a2_ver = procedure_2(graph, k)
    a4_ver, U = procedure_4(graph, k)
    a3_ver = procedure_3(graph, k, U)

    vertices = max(a1_ver, a2_ver, a3_ver, a4_ver,
                   key=lambda x: graph.distinct_colours_of_subgraph(graph.vertices_by_index(x)))
    return vertices


def Tirodkar2017(graph: Graph.Graph):
    print("----------------------------------")
    p = graph.num_colours
    min_n_ver, max_n_ver = int(math.sqrt(p)), min(p * 2 + 1, graph.n())
    print(f"{p} colors, min_k = {min_n_ver}, max_k = {max_n_ver}, size: {graph.n()}")
    result_ver = None
    result_size = graph.n()
    for k in range(min_n_ver, max_n_ver):
        if k > result_size:
            break
        g_prime = graph.copy()
        sub_graph = tirodkar_procedure(g_prime, k)
        c = 1
        while len(graph.distinct_colours_of_subgraph(graph.vertices_by_index(sub_graph))) < p:
            # print(f"iteration -> {c}")
            # print(f"g_prime colours: {g_prime.colours.keys()}")
            # print(f"graph colours: {graph.colours.keys()}")
            # print(f"distict colors of sub graph in g_prime: {g_prime.distinct_colours_of_subgraph(g_prime.vertices_by_index(sub_graph))}")
            # print(f"distict colors of sub graph in graph: {graph.distinct_colours_of_subgraph(graph.vertices_by_index(sub_graph))}")
            # print(f"the subgraph: {sub_graph}")
            c += 1
            sub_graph_vertices = g_prime.vertices_by_index(sub_graph)
            g_prime.remove_all_colours_in_sub_graph(sub_graph_vertices)
            new_it = tirodkar_procedure(g_prime, k)
            sub_graph = sub_graph.union(new_it)

        if len(sub_graph) < result_size:
            result_size = len(sub_graph)
            result_ver = sub_graph

    print(f"result k = {result_size}, {result_ver}")
    sub_graph = graph.induced_sub_graph(graph.vertices_by_index(result_ver))
    print(list(sub_graph.vertices.values()), sub_graph.edges, sep="\n")

    return sub_graph

