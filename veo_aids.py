def vertex_intersection_len(n1, n2):
    d1, d2 = {}, {}
    result = 0
    for x in n1:
        if x not in d1:
            d1[x] = 0
        d1[x] += 1
    for x in n2:
        if x not in d2:
            d2[x] = 0
        d2[x] += 1
    for x in d1:
        if x in d2:
            result += min(d1[x], d2[x])
    return result


def edge_intersection_len(g1, g2):
    n1, n2, e1, e2 = g1["n"], g2["n"], g1["e"], g2["e"]
    d1, d2 = {}, {}
    result = 0
    num_nodes_1 = len(n1)
    num_nodes_2 = len(n2)
    for i in range(num_nodes_1):
        for j in range(num_nodes_1):
            if e1[i][j] == 1:
                u, v = n1[i], n1[j]
                if u not in d1:
                    d1[u] = {}
                if v not in d1[u]:
                    d1[u][v] = 0
                d1[u][v] += 1
    for i in range(num_nodes_2):
        for j in range(num_nodes_2):
            if e2[i][j] == 1:
                u, v = n2[i], n2[j]
                if u not in d1:
                    d2[u] = {}
                if v not in d2[u]:
                    d2[u][v] = 0
                d2[u][v] += 1
    for x in d1:
        if x in d2:
            result += min(d1[x], d2[x])
    return result


if __name__ == '__main__':
    main()
