import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.connection = psycopg2.connect(Config.DATABASE_URL)
        self.create_tables()
    
    def create_tables(self):
        with self.connection.cursor() as cursor:
            # Table des nœuds
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS nodes (
                    id VARCHAR(50) PRIMARY KEY,
                    x FLOAT NOT NULL,
                    y FLOAT NOT NULL,
                    capacity INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table des arêtes avec contraintes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS edges (
                    id SERIAL PRIMARY KEY,
                    u VARCHAR(50) NOT NULL,
                    v VARCHAR(50) NOT NULL,
                    weight FLOAT NOT NULL,
                    constraint_value FLOAT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (u) REFERENCES nodes(id) ON DELETE CASCADE,
                    FOREIGN KEY (v) REFERENCES nodes(id) ON DELETE CASCADE,
                    UNIQUE(u, v)
                )
            """)
            
            self.connection.commit()
    
    def execute_query(self, query, params=None):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            self.connection.commit()
            return cursor.rowcount
    
    def close(self):
        if self.connection:
            self.connection.close()