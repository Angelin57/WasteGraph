import heapq
from database import Database

class Dijkstra:
    def __init__(self):
        self.db = Database()
    
    def get_shortest_path(self, src, dst):
        # Récupérer tous les nœuds et arêtes
        nodes = self.db.execute_query("SELECT id FROM nodes")
        edges = self.db.execute_query("SELECT u, v, weight, constraint_value FROM edges")
        
        if not nodes:
            return {'path': [], 'distance': float('inf'), 'error': 'No nodes in graph'}
        
        # Construire le graphe avec poids total
        graph = {}
        for node in nodes:
            graph[node['id']] = []
        
        for edge in edges:
            u, v = edge['u'], edge['v']
            total_weight = edge['weight'] + edge['constraint_value']
            
            graph[u].append((v, total_weight))
            graph[v].append((u, total_weight))  # Graphe non orienté
        
        # Vérifier si les nœuds source et destination existent
        if src not in graph:
            return {'path': [], 'distance': float('inf'), 'error': f'Source node {src} not found'}
        if dst not in graph:
            return {'path': [], 'distance': float('inf'), 'error': f'Destination node {dst} not found'}
        
        # Implémentation de Dijkstra
        distances = {node: float('inf') for node in graph}
        previous = {node: None for node in graph}
        distances[src] = 0
        
        priority_queue = [(0, src)]
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            
            if current_distance > distances[current_node]:
                continue
            
            if current_node == dst:
                break
            
            for neighbor, weight in graph[current_node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        # Reconstruire le chemin
        path = []
        current = dst
        while current is not None:
            path.append(current)
            current = previous[current]
        
        path.reverse()
        
        if distances[dst] == float('inf'):
            return {'path': [], 'distance': float('inf'), 'error': 'No path found'}
        
        return {
            'path': path,
            'distance': distances[dst],
            'source': src,
            'destination': dst
        }