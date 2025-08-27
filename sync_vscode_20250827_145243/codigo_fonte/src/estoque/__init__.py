"""
Módulo de controle de estoque
Contém a lógica de banco de dados e controle de produtos
"""

from .database import DatabaseManager
from .controller import EstoqueController

__all__ = ['DatabaseManager', 'EstoqueController']
