from http.server import HTTPServer
from controllers.router import Router
from database import Database
import signal
import sys

class WasteGraphApp:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.server = None
        self.db = Database()
    
    def run(self):
        try:
            self.server = HTTPServer((self.host, self.port), Router)
            print(f"Server running on http://{self.host}:{self.port}")
            print("Available endpoints:")
            print("  GET  /graph - Get graph data")
            print("  POST /graph/node - Add node")
            print("  POST /graph/edge - Add edge")
            print("  PUT  /graph/node - Update node")
            print("  PUT  /graph/edge - Update edge")
            print("  DELETE /graph/node - Delete node")
            print("  DELETE /graph/edge - Delete edge")
            print("  GET  /algo/dijkstra?src=A&dst=Z - Shortest path")
            print("  GET  /algo/coloring - Graph coloring")
            print("  GET  /stats - Graph statistics")
            
            # Gestion propre de l'arrêt
            signal.signal(signal.SIGINT, self._shutdown)
            signal.signal(signal.SIGTERM, self._shutdown)
            
            self.server.serve_forever()
        
        except Exception as e:
            print(f"Error starting server: {e}")
            sys.exit(1)
    
    def _shutdown(self, signum, frame):
        print("\nShutting down server...")
        if self.server:
            self.server.shutdown()
        self.db.close()
        sys.exit(0)

if __name__ == '__main__':
    app = WasteGraphApp()
    app.run()