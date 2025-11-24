# Dans config.py, modifier directement :
class Config:
    DB_HOST = 'localhost'
    DB_PORT = '5433'
    DB_NAME = 'wastegraph'
    DB_USER = 'postgres'
    DB_PASSWORD = '5751'
    
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"