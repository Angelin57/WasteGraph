from database import Database

class Coloring:
    def __init__(self):
        self.db = Database()
    
    def color_graph(self):
        # Récupérer tous les nœuds et arêtes
        nodes = self.db.execute_query("SELECT id FROM nodes")
        edges = self.db.execute_query("SELECT u, v FROM edges")
        
        if not nodes:
            return {}
        
        # Construire la liste d'adjacence
        graph = {}
        for node in nodes:
            graph[node['id']] = []
        
        for edge in edges:
            u, v = edge['u'], edge['v']
            graph[u].append(v)
            graph[v].append(u)
        
        # Algorithme de coloriage glouton
        colors = {}  # node -> color
        available_colors = set(range(len(nodes)))  # Couleurs disponibles
        
        # Trier les nœuds par degré décroissant
        sorted_nodes = sorted(graph.keys(), key=lambda x: len(graph[x]), reverse=True)
        
        for node in sorted_nodes:
            # Couleurs utilisées par les voisins
            used_colors = set(colors.get(neighbor, -1) for neighbor in graph[node])
            used_colors.discard(-1)  # Enlever la valeur par défaut
            
            # Trouver la première couleur disponible
            for color in available_colors:
                if color not in used_colors:
                    colors[node] = color
                    break
        
        # Mapper les couleurs aux jours de la semaine
        days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        colored_days = {}
        
        for node, color_idx in colors.items():
            day = days[color_idx % len(days)]
            colored_days[node] = {
                'color': color_idx,
                'day': day
            }
        
        return colored_days