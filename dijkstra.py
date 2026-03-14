import heapq

def dijkstra(graph, start, end):

    queue = [(0, start, [])]
    visited = set()

    while queue:

        (cost, node, path) = heapq.heappop(queue)

        if node in visited:
            continue

        path = path + [node]
        visited.add(node)

        if node == end:
            return cost, path

        for neighbour, weight in graph[node].items():
            heapq.heappush(queue, (cost + weight, neighbour, path))

    return float("inf"), []