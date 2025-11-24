"""
Package models pour WasteGraph
Contient les modèles de données et algorithmes
"""

from .graph_data import GraphData
from .dijkstra import Dijkstra
from .coloring import Coloring

__all__ = ['GraphData', 'Dijkstra', 'Coloring']