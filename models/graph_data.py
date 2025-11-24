from database import Database

class GraphData:
    def __init__(self):
        self.db = Database()
    
    def get_all_nodes(self):
        return self.db.execute_query("SELECT * FROM nodes")
    
    def get_all_edges(self):
        return self.db.execute_query("SELECT * FROM edges")
    
    def get_node(self, node_id):
        result = self.db.execute_query("SELECT * FROM nodes WHERE id = %s", (node_id,))
        return result[0] if result else None
    
    def add_node(self, node_id, x, y, capacity):
        return self.db.execute_query(
            "INSERT INTO nodes (id, x, y, capacity) VALUES (%s, %s, %s, %s)",
            (node_id, x, y, capacity)
        )
    
    def update_node(self, node_id, x=None, y=None, capacity=None):
        updates = []
        params = []
        
        if x is not None:
            updates.append("x = %s")
            params.append(x)
        if y is not None:
            updates.append("y = %s")
            params.append(y)
        if capacity is not None:
            updates.append("capacity = %s")
            params.append(capacity)
        
        if updates:
            params.append(node_id)
            query = f"UPDATE nodes SET {', '.join(updates)} WHERE id = %s"
            return self.db.execute_query(query, params)
        return 0
    
    def delete_node(self, node_id):
        return self.db.execute_query("DELETE FROM nodes WHERE id = %s", (node_id,))
    
    def add_edge(self, u, v, weight, constraint_value=0):
        return self.db.execute_query(
            "INSERT INTO edges (u, v, weight, constraint_value) VALUES (%s, %s, %s, %s)",
            (u, v, weight, constraint_value)
        )
    
    def update_edge(self, u, v, weight=None, constraint_value=None):
        updates = []
        params = []
        
        if weight is not None:
            updates.append("weight = %s")
            params.append(weight)
        if constraint_value is not None:
            updates.append("constraint_value = %s")
            params.append(constraint_value)
        
        if updates:
            params.extend([u, v])
            query = f"UPDATE edges SET {', '.join(updates)} WHERE u = %s AND v = %s"
            return self.db.execute_query(query, params)
        return 0
    
    def delete_edge(self, u, v):
        return self.db.execute_query("DELETE FROM edges WHERE u = %s AND v = %s", (u, v))
    
    def get_graph(self):
        nodes = self.get_all_nodes()
        edges = self.get_all_edges()
        
        # Calculer le poids total avec contrainte
        for edge in edges:
            edge['total_weight'] = edge['weight'] + edge['constraint_value']
        
        return {
            'nodes': nodes,
            'edges': edges
        }
    
    def get_stats(self):
        nodes_count = self.db.execute_query("SELECT COUNT(*) as count FROM nodes")[0]['count']
        edges_count = self.db.execute_query("SELECT COUNT(*) as count FROM edges")[0]['count']
        
        # Calcul du degré moyen
        degree_avg = self.db.execute_query("""
            SELECT AVG(degree) as avg_degree FROM (
                SELECT n.id, COUNT(e.id) as degree 
                FROM nodes n 
                LEFT JOIN edges e ON n.id = e.u OR n.id = e.v 
                GROUP BY n.id
            ) as degrees
        """)[0]['avg_degree'] or 0
        
        return {
            'nodes_count': nodes_count,
            'edges_count': edges_count,
            'average_degree': float(degree_avg)
        }