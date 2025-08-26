"""
Gerenciador de banco de dados SQLite
"""

import sqlite3
import os
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_path="data/banco.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Inicializa o banco de dados e cria as tabelas necessárias"""
        # Criar diretório data se não existir
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Criar tabela estoque
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS estoque (
                    produto TEXT PRIMARY KEY,
                    quantidade INTEGER NOT NULL DEFAULT 0
                )
            ''')
            
            # Criar tabela historico_vendas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historico_vendas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    data_hora TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            
    def get_connection(self):
        """Retorna uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_path)
        
    def execute_query(self, query, params=None):
        """Executa uma query e retorna os resultados"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
            
    def execute_update(self, query, params=None):
        """Executa uma query de atualização e retorna o número de linhas afetadas"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
            
    def execute_insert(self, query, params=None):
        """Executa uma query de inserção e retorna o ID da linha inserida"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.lastrowid
            
    # Métodos específicos para estoque
    def inserir_produto(self, produto, quantidade):
        """Insere um novo produto no estoque"""
        query = "INSERT INTO estoque (produto, quantidade) VALUES (?, ?)"
        try:
            self.execute_insert(query, (produto, quantidade))
            return True
        except sqlite3.IntegrityError:
            # Produto já existe
            return False
        except Exception:
            return False
            
    def atualizar_quantidade(self, produto, quantidade):
        """Atualiza a quantidade de um produto"""
        query = "UPDATE estoque SET quantidade = ? WHERE produto = ?"
        rows_affected = self.execute_update(query, (quantidade, produto))
        return rows_affected > 0
        
    def consultar_produto(self, produto):
        """Consulta a quantidade de um produto específico"""
        query = "SELECT quantidade FROM estoque WHERE produto = ?"
        result = self.execute_query(query, (produto,))
        return result[0][0] if result else None
        
    def listar_estoque(self):
        """Lista todos os produtos em estoque"""
        query = "SELECT produto, quantidade FROM estoque ORDER BY produto"
        return self.execute_query(query)
        
    def remover_produto(self, produto):
        """Remove um produto do estoque"""
        query = "DELETE FROM estoque WHERE produto = ?"
        rows_affected = self.execute_update(query, (produto,))
        return rows_affected > 0
        
    # Métodos específicos para histórico de vendas
    def registrar_venda(self, produto, quantidade):
        """Registra uma venda no histórico"""
        query = "INSERT INTO historico_vendas (produto, quantidade, data_hora) VALUES (?, ?, ?)"
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            venda_id = self.execute_insert(query, (produto, quantidade, data_hora))
            return venda_id is not None
        except Exception:
            return False
            
    def listar_historico(self, limite=None):
        """Lista o histórico de vendas"""
        query = "SELECT id, produto, quantidade, data_hora FROM historico_vendas ORDER BY id DESC"
        if limite:
            query += f" LIMIT {limite}"
        return self.execute_query(query)
        
    def buscar_vendas_por_produto(self, produto):
        """Busca vendas de um produto específico"""
        query = "SELECT id, produto, quantidade, data_hora FROM historico_vendas WHERE produto LIKE ? ORDER BY id DESC"
        return self.execute_query(query, (f"%{produto}%",))
        
    def obter_estatisticas_vendas(self):
        """Obtém estatísticas de vendas por produto"""
        query = """
            SELECT produto, SUM(quantidade) as total_vendido, COUNT(*) as num_vendas
            FROM historico_vendas 
            GROUP BY produto 
            ORDER BY total_vendido DESC
        """
        return self.execute_query(query)
