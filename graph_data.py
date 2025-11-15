
# --- Définition du graphe (liste d'adjacence) ---
graph = {
    'A': [('B', 2), ('C', 5)],
    'B': [('A', 2), ('C', 1), ('D', 4)],
    'C': [('A', 5), ('B', 1), ('D', 2)],
    'D': [('B', 4), ('C', 2)]
}

# --- Contraintes sur certaines routes ---
constraints = {
    ('A', 'C'): 'stop',
    ('B', 'D'): 'obstacle',
}

# --- Coût supplémentaire selon la contrainte ---
constraint_cost = {
    'stop': 3,
    'obstacle': 10,
    'rien': 0
}
