import http.server
import socketserver
import json
from urllib.parse import urlparse
from controllers.api_controller import APIController
from config import Config

class WasteGraphHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.api_controller = APIController()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Gérer les requêtes GET"""
        self.handle_api_request('GET')
    
    def do_POST(self):
        """Gérer les requêtes POST"""
        self.handle_api_request('POST')
    
    def do_PUT(self):
        """Gérer les requêtes PUT"""
        self.handle_api_request('PUT')
    
    def do_DELETE(self):
        """Gérer les requêtes DELETE"""
        self.handle_api_request('DELETE')
    
    def handle_api_request(self, method):
        """Traiter les requêtes API"""
        # Lire le corps de la requête
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else None
        
        # Traiter la requête via le contrôleur
        response = self.api_controller.handle_request(method, self.path, body)
        
        # Envoyer la réponse
        self.send_response(response.get('status', 200))
        
        # Headers CORS pour permettre les requêtes cross-origin
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        if 'content_type' in response:
            self.send_header('Content-Type', response['content_type'])
        else:
            self.send_header('Content-Type', 'application/json')
        
        self.end_headers()
        
        # Envoyer le corps de la réponse
        if 'body' in response:
            self.wfile.write(response['body'].encode('utf-8'))
        else:
            response_body = json.dumps(response)
            self.wfile.write(response_body.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Gérer les requêtes OPTIONS pour CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server():
    """Lancer le serveur HTTP"""
    handler = WasteGraphHTTPRequestHandler
    
    with socketserver.TCPServer((Config.SERVER_HOST, Config.SERVER_PORT), handler) as httpd:
        print(f"Serveur WasteGraph démarré sur http://{Config.SERVER_HOST}:{Config.SERVER_PORT}")
        print("Appuyez sur Ctrl+C pour arrêter le serveur")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nArrêt du serveur...")
            httpd.shutdown()

if __name__ == '__main__':
    run_server()