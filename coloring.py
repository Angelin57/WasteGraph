# coloring.py
from graph_data import graph

def build_adjacency_list(graph):
    adj = {node: [] for node in graph}
    for node, neighbors in graph.items():
        for neigh, _ in neighbors:
            if neigh not in adj[node]:
                adj[node].append(neigh)
    return adj


def graph_coloring(graph):
    colors = {}
    available_colors = ['Rouge', 'Vert', 'Bleu', 'Jaune', 'Orange', 'Violet']

    for node in graph:
        # Couleurs des voisins
        used = set(colors.get(neigh) for neigh in graph[node] if neigh in colors)

        # Choisir la première couleur libre
        for color in available_colors:
            if color not in used:
                colors[node] = color
                break

    return colors
