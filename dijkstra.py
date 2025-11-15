# dijkstra.py
from graph_data import graph, constraints, constraint_cost

def dijkstra_with_constraints(source):
    dist = {node: float('inf') for node in graph}
    dist[source] = 0

    unvisited = set(graph.keys())

    while unvisited:
        # choisir le nœud non visité le plus proche
        current = min(unvisited, key=lambda n: dist[n])

        if dist[current] == float('inf'):
            break

        unvisited.remove(current)

        for neighbor, weight in graph[current]:
            constraint = constraints.get((current, neighbor), 'rien')
            extra_cost = constraint_cost[constraint]

            new_dist = dist[current] + weight + extra_cost

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist

    return dist
