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
                    quantidade INTEGER NOT NULL DEFAULT 0,
                    preco REAL DEFAULT 0.0,
                    categoria TEXT DEFAULT 'Geral',
                    codigo_barras TEXT DEFAULT '',
                    data_cadastro TEXT DEFAULT '',
                    data_atualizacao TEXT DEFAULT ''
                )
            ''')
            
            # Criar tabela historico_vendas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historico_vendas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    preco_unitario REAL DEFAULT 0.0,
                    valor_total REAL DEFAULT 0.0,
                    data_hora TEXT NOT NULL,
                    vendedor TEXT DEFAULT '',
                    observacoes TEXT DEFAULT ''
                )
            ''')
            
            # Criar tabela configuracoes para versioning e configurações do sistema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configuracoes (
                    chave TEXT PRIMARY KEY,
                    valor TEXT NOT NULL,
                    data_atualizacao TEXT DEFAULT ''
                )
            ''')
            
            # Inserir configurações padrão
            cursor.execute('''
                INSERT OR IGNORE INTO configuracoes (chave, valor, data_atualizacao) 
                VALUES ('versao_sistema', '1.0.0', ?)
            ''', (datetime.now().strftime("%d/%m/%Y %H:%M:%S"),))
            
            cursor.execute('''
                INSERT OR IGNORE INTO configuracoes (chave, valor, data_atualizacao) 
                VALUES ('nome_empresa', 'Minha Lanchonete', ?)
            ''', (datetime.now().strftime("%d/%m/%Y %H:%M:%S"),))
            
            cursor.execute('''
                INSERT OR IGNORE INTO configuracoes (chave, valor, data_atualizacao) 
                VALUES ('moeda', 'R$', ?)
            ''', (datetime.now().strftime("%d/%m/%Y %H:%M:%S"),))
            
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
    def inserir_produto(self, produto, quantidade, preco=0.0, categoria='Geral', codigo_barras=''):
        """Insere um novo produto no estoque"""
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        query = """INSERT INTO estoque 
                   (produto, quantidade, preco, categoria, codigo_barras, data_cadastro, data_atualizacao) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)"""
        try:
            self.execute_insert(query, (produto, quantidade, preco, categoria, codigo_barras, data_atual, data_atual))
            return True
        except sqlite3.IntegrityError:
            # Produto já existe
            return False
        except Exception:
            return False
            
    def atualizar_quantidade(self, produto, quantidade):
        """Atualiza a quantidade de um produto"""
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        query = "UPDATE estoque SET quantidade = ?, data_atualizacao = ? WHERE produto = ?"
        rows_affected = self.execute_update(query, (quantidade, data_atual, produto))
        return rows_affected > 0
        
    def atualizar_preco(self, produto, preco):
        """Atualiza o preço de um produto"""
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        query = "UPDATE estoque SET preco = ?, data_atualizacao = ? WHERE produto = ?"
        rows_affected = self.execute_update(query, (preco, data_atual, produto))
        return rows_affected > 0
        
    def atualizar_produto_completo(self, produto, quantidade, preco, categoria, codigo_barras):
        """Atualiza todas as informações de um produto"""
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        query = """UPDATE estoque SET quantidade = ?, preco = ?, categoria = ?, 
                   codigo_barras = ?, data_atualizacao = ? WHERE produto = ?"""
        rows_affected = self.execute_update(query, (quantidade, preco, categoria, codigo_barras, data_atual, produto))
        return rows_affected > 0
        
    def consultar_produto(self, produto):
        """Consulta a quantidade de um produto específico"""
        query = "SELECT quantidade FROM estoque WHERE produto = ?"
        result = self.execute_query(query, (produto,))
        return result[0][0] if result else None
        
    def consultar_produto_completo(self, produto):
        """Consulta todas as informações de um produto"""
        query = """SELECT produto, quantidade, preco, categoria, codigo_barras, 
                   data_cadastro, data_atualizacao FROM estoque WHERE produto = ?"""
        result = self.execute_query(query, (produto,))
        return result[0] if result else None
        
    def listar_estoque(self):
        """Lista todos os produtos em estoque"""
        query = "SELECT produto, quantidade FROM estoque ORDER BY produto"
        return self.execute_query(query)
        
    def listar_estoque_completo(self):
        """Lista todos os produtos com informações completas"""
        query = """SELECT produto, quantidade, preco, categoria, codigo_barras, 
                   data_cadastro, data_atualizacao FROM estoque ORDER BY produto"""
        return self.execute_query(query)
        
    def remover_produto(self, produto):
        """Remove um produto do estoque"""
        query = "DELETE FROM estoque WHERE produto = ?"
        rows_affected = self.execute_update(query, (produto,))
        return rows_affected > 0
        
    # Métodos específicos para histórico de vendas
    def registrar_venda(self, produto, quantidade, preco_unitario=0.0, vendedor='', observacoes=''):
        """Registra uma venda no histórico"""
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        valor_total = quantidade * preco_unitario
        query = """INSERT INTO historico_vendas 
                   (produto, quantidade, preco_unitario, valor_total, data_hora, vendedor, observacoes) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)"""
        try:
            venda_id = self.execute_insert(query, (produto, quantidade, preco_unitario, valor_total, data_hora, vendedor, observacoes))
            return venda_id is not None
        except Exception:
            return False
            
    def listar_historico(self, limite=None):
        """Lista o histórico de vendas"""
        query = "SELECT id, produto, quantidade, data_hora FROM historico_vendas ORDER BY id DESC"
        if limite:
            query += f" LIMIT {limite}"
        return self.execute_query(query)
        
    def listar_historico_completo(self, limite=None):
        """Lista o histórico completo de vendas"""
        query = """SELECT id, produto, quantidade, preco_unitario, valor_total, 
                   data_hora, vendedor, observacoes FROM historico_vendas ORDER BY id DESC"""
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
        
    def obter_estatisticas_financeiras(self):
        """Obtém estatísticas financeiras de vendas"""
        query = """
            SELECT produto, SUM(quantidade) as total_vendido, 
                   SUM(valor_total) as receita_total, 
                   AVG(preco_unitario) as preco_medio,
                   COUNT(*) as num_vendas
            FROM historico_vendas 
            GROUP BY produto 
            ORDER BY receita_total DESC
        """
        return self.execute_query(query)
        
    def obter_receita_total(self):
        """Obtém a receita total de todas as vendas"""
        query = "SELECT SUM(valor_total) FROM historico_vendas"
        result = self.execute_query(query)
        return result[0][0] if result and result[0][0] else 0.0
        
    def obter_configuracao(self, chave):
        """Obtém uma configuração do sistema"""
        query = "SELECT valor FROM configuracoes WHERE chave = ?"
        result = self.execute_query(query, (chave,))
        return result[0][0] if result else None
        
    def atualizar_configuracao(self, chave, valor):
        """Atualiza uma configuração do sistema"""
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        query = """INSERT OR REPLACE INTO configuracoes 
                   (chave, valor, data_atualizacao) VALUES (?, ?, ?)"""
        rows_affected = self.execute_update(query, (chave, valor, data_atual))
        return rows_affected > 0
