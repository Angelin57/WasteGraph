import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from models.graph_data import GraphData
from models.dijkstra import Dijkstra
from models.coloring import Coloring
from views.json_view import JSONView

class Router(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers(200)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        
        try:
            # Servir les fichiers statiques et la page d'accueil
            if path.startswith('/static/'):
                self._serve_static_file(path)
            elif path == '/' or path == '/index.html':
                self._serve_index()
            elif path == '/graph':
                self._handle_get_graph()
            elif path == '/algo/dijkstra':
                self._handle_dijkstra(query_params)
            elif path == '/algo/coloring':
                self._handle_coloring()
            elif path == '/stats':
                self._handle_stats()
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps(JSONView.error("Endpoint not found", 404)).encode())
        
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps(JSONView.error(str(e), 500)).encode())
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode()) if content_length > 0 else {}
            
            if path == '/graph/node':
                self._handle_add_node(data)
            elif path == '/graph/edge':
                self._handle_add_edge(data)
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps(JSONView.error("Endpoint not found", 404)).encode())
        
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps(JSONView.error(str(e), 500)).encode())
    
    def do_PUT(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            data = json.loads(put_data.decode()) if content_length > 0 else {}
            
            if path == '/graph/node':
                self._handle_update_node(data)
            elif path == '/graph/edge':
                self._handle_update_edge(data)
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps(JSONView.error("Endpoint not found", 404)).encode())
        
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps(JSONView.error(str(e), 500)).encode())
    
    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        
        try:
            if path == '/graph/node':
                self._handle_delete_node(query_params)
            elif path == '/graph/edge':
                self._handle_delete_edge(query_params)
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps(JSONView.error("Endpoint not found", 404)).encode())
        
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps(JSONView.error(str(e), 500)).encode())
    
    # Handlers pour les fichiers statiques
    def _serve_index(self):
        """Servir la page index.html"""
        try:
            with open('static/index.html', 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self._set_headers(404)
            self.wfile.write(b'Index file not found')
    
    def _serve_static_file(self, path):
        """Servir les fichiers statiques (CSS, JS)"""
        try:
            # Enlever le préfixe /static/
            file_path = path[8:]
            
            # Déterminer le type MIME
            if path.endswith('.css'):
                mime_type = 'text/css'
            elif path.endswith('.js'):
                mime_type = 'application/javascript'
            elif path.endswith('.png'):
                mime_type = 'image/png'
            elif path.endswith('.jpg') or path.endswith('.jpeg'):
                mime_type = 'image/jpeg'
            elif path.endswith('.svg'):
                mime_type = 'image/svg+xml'
            else:
                mime_type = 'text/plain'
            
            with open(f'static/{file_path}', 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', mime_type)
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            
        except FileNotFoundError:
            self._set_headers(404)
            self.wfile.write(b'Static file not found')
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(f'Error serving static file: {str(e)}'.encode())
    
    # Handlers pour les API
    def _handle_get_graph(self):
        graph_data = GraphData()
        result = graph_data.get_graph()
        self._set_headers(200)
        self.wfile.write(json.dumps(JSONView.success(result)).encode())
    
    def _handle_dijkstra(self, query_params):
        src = query_params.get('src', [None])[0]
        dst = query_params.get('dst', [None])[0]
        
        if not src or not dst:
            self._set_headers(400)
            self.wfile.write(json.dumps(JSONView.error("Missing src or dst parameters", 400)).encode())
            return
        
        dijkstra = Dijkstra()
        result = dijkstra.get_shortest_path(src, dst)
        self._set_headers(200)
        self.wfile.write(json.dumps(JSONView.success(result)).encode())
    
    def _handle_coloring(self):
        coloring = Coloring()
        result = coloring.color_graph()
        self._set_headers(200)
        self.wfile.write(json.dumps(JSONView.success(result)).encode())
    
    def _handle_stats(self):
        graph_data = GraphData()
        result = graph_data.get_stats()
        self._set_headers(200)
        self.wfile.write(json.dumps(JSONView.success(result)).encode())
    
    def _handle_add_node(self, data):
        required_fields = ['id', 'x', 'y']
        if not all(field in data for field in required_fields):
            self._set_headers(400)
            self.wfile.write(json.dumps(JSONView.error("Missing required fields: id, x, y", 400)).encode())
            return
        
        graph_data = GraphData()
        result = graph_data.add_node(data['id'], data['x'], data['y'], data.get('capacity'))
        self._set_headers(201)
        self.wfile.write(json.dumps(JSONView.success(None, "Node added successfully")).encode())
    
    def _handle_add_edge(self, data):
        required_fields = ['u', 'v', 'weight']
        if not all(field in data for field in required_fields):
            self._set_headers(400)
            self.wfile.write(json.dumps(JSONView.error("Missing required fields: u, v, weight", 400)).encode())
            return
        
        graph_data = GraphData()
        result = graph_data.add_edge(data['u'], data['v'], data['weight'], data.get('constraint_value', 0))
        self._set_headers(201)
        self.wfile.write(json.dumps(JSONView.success(None, "Edge added successfully")).encode())
    
    def _handle_update_node(self, data):
        if 'id' not in data:
            self._set_headers(400)
            self.wfile.write(json.dumps(JSONView.error("Missing node id", 400)).encode())
            return
        
        graph_data = GraphData()
        result = graph_data.update_node(
            data['id'],
            data.get('x'),
            data.get('y'),
            data.get('capacity')
        )
        self._set_headers(200)
        self.wfile.write(json.dumps(JSONView.success(None, "Node updated successfully")).encode())
    
    def _handle_update_edge(self, data):
        required_fields = ['u', 'v']
        if not all(field in data for field in required_fields):
            self._set_headers(400)
            self.wfile.write(json.dumps(JSONView.error("Missing required fields: u, v", 400)).encode())
            return
        
        graph_data = GraphData()
        result = graph_data.update_edge(
            data['u'],
            data['v'],
            data.get('weight'),
            data.get('constraint_value')
        )
        self._set_headers(200)
        self.wfile.write(json.dumps(JSONView.success(None, "Edge updated successfully")).encode())
    
    def _handle_delete_node(self, query_params):
        node_id = query_params.get('id', [None])[0]
        if not node_id:
            self._set_headers(400)
            self.wfile.write(json.dumps(JSONView.error("Missing node id", 400)).encode())
            return
        
        graph_data = GraphData()
        result = graph_data.delete_node(node_id)
        self._set_headers(200)
        self.wfile.write(json.dumps(JSONView.success(None, "Node deleted successfully")).encode())
    
    def _handle_delete_edge(self, query_params):
        u = query_params.get('u', [None])[0]
        v = query_params.get('v', [None])[0]
        
        if not u or not v:
            self._set_headers(400)
            self.wfile.write(json.dumps(JSONView.error("Missing u or v parameters", 400)).encode())
            return
        
        graph_data = GraphData()
        result = graph_data.delete_edge(u, v)
        self._set_headers(200)
        self.wfile.write(json.dumps(JSONView.success(None, "Edge deleted successfully")).encode())