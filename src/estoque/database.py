"""
Gerenciador de banco de dados SQLite
"""

import sqlite3
import os
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_path="data/banco.db"):
        self.db_path = db_path
        # Garantir que diretório existe
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_database()
        
    def init_database(self):
        """Inicializa o banco de dados e cria as tabelas necessárias"""
        # Criar diretório data se não existir
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Verificar se precisa fazer migração da estrutura antiga
            self._migrar_estrutura_antiga(cursor)
            
            # Criar tabela estoque
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS estoque (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto TEXT NOT NULL,
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
                VALUES ('versao_sistema', '2.0.0', ?)
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
            
    def _migrar_estrutura_antiga(self, cursor):
        """Migra estruturas antigas do banco de dados"""
        try:
            # Verificar se tabela estoque existe e tem estrutura antiga
            cursor.execute("PRAGMA table_info(estoque)")
            colunas_estoque = [col[1] for col in cursor.fetchall()]
            
            if 'estoque' in [table[0] for table in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
                # Se tabela existe mas não tem coluna preço, adicionar
                if 'preco' not in colunas_estoque:
                    cursor.execute('ALTER TABLE estoque ADD COLUMN preco REAL DEFAULT 0.0')
                if 'categoria' not in colunas_estoque:
                    cursor.execute('ALTER TABLE estoque ADD COLUMN categoria TEXT DEFAULT "Geral"')
                if 'codigo_barras' not in colunas_estoque:
                    cursor.execute('ALTER TABLE estoque ADD COLUMN codigo_barras TEXT DEFAULT ""')
                if 'data_cadastro' not in colunas_estoque:
                    cursor.execute('ALTER TABLE estoque ADD COLUMN data_cadastro TEXT DEFAULT ""')
                if 'data_atualizacao' not in colunas_estoque:
                    cursor.execute('ALTER TABLE estoque ADD COLUMN data_atualizacao TEXT DEFAULT ""')
            
            # Verificar se tabela historico_vendas existe e tem estrutura antiga
            cursor.execute("PRAGMA table_info(historico_vendas)")
            colunas_historico = [col[1] for col in cursor.fetchall()]
            
            if 'historico_vendas' in [table[0] for table in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
                # Se tabela existe mas não tem colunas de preço, adicionar
                if 'preco_unitario' not in colunas_historico:
                    cursor.execute('ALTER TABLE historico_vendas ADD COLUMN preco_unitario REAL DEFAULT 0.0')
                if 'valor_total' not in colunas_historico:
                    cursor.execute('ALTER TABLE historico_vendas ADD COLUMN valor_total REAL DEFAULT 0.0')
                if 'vendedor' not in colunas_historico:
                    cursor.execute('ALTER TABLE historico_vendas ADD COLUMN vendedor TEXT DEFAULT ""')
                if 'observacoes' not in colunas_historico:
                    cursor.execute('ALTER TABLE historico_vendas ADD COLUMN observacoes TEXT DEFAULT ""')
                
                # Atualizar registros antigos que não têm valores financeiros
                cursor.execute('''
                    UPDATE historico_vendas 
                    SET preco_unitario = 0.0, valor_total = 0.0 
                    WHERE preco_unitario IS NULL OR valor_total IS NULL
                ''')
            
        except Exception as e:
            print(f"Aviso: Erro na migração do banco de dados: {e}")
            # Continuar mesmo com erro de migração
            
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
        """Lista todos os produtos em estoque (formato básico para compatibilidade)"""
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
    
    # === MÉTODOS PARA DASHBOARD FINANCEIRO ===
    
    def obter_receita_periodo(self, data_inicio, data_fim):
        """Obtém receita total de um período específico"""
        try:
            # Converter datas DD/MM/YYYY para formato SQLite YYYY-MM-DD
            def converter_data(data_str):
                partes = data_str.split('/')
                if len(partes) == 3:
                    return f"{partes[2]}-{partes[1].zfill(2)}-{partes[0].zfill(2)}"
                return data_str
            
            data_inicio_sql = converter_data(data_inicio)
            data_fim_sql = converter_data(data_fim)
            
            query = """
                SELECT COALESCE(SUM(valor_total), 0) 
                FROM historico_vendas 
                WHERE DATE(SUBSTR(data_hora, 7, 4) || '-' || 
                          SUBSTR(data_hora, 4, 2) || '-' || 
                          SUBSTR(data_hora, 1, 2)) 
                BETWEEN ? AND ?
            """
            result = self.execute_query(query, (data_inicio_sql, data_fim_sql))
            return result[0][0] if result else 0.0
        except Exception as e:
            print(f"Erro ao obter receita do período: {e}")
            return 0.0
    
    def contar_vendas_periodo(self, data_inicio, data_fim):
        """Conta número de vendas em um período"""
        try:
            def converter_data(data_str):
                partes = data_str.split('/')
                if len(partes) == 3:
                    return f"{partes[2]}-{partes[1].zfill(2)}-{partes[0].zfill(2)}"
                return data_str
            
            data_inicio_sql = converter_data(data_inicio)
            data_fim_sql = converter_data(data_fim)
            
            query = """
                SELECT COUNT(*) 
                FROM historico_vendas 
                WHERE DATE(SUBSTR(data_hora, 7, 4) || '-' || 
                          SUBSTR(data_hora, 4, 2) || '-' || 
                          SUBSTR(data_hora, 1, 2)) 
                BETWEEN ? AND ?
            """
            result = self.execute_query(query, (data_inicio_sql, data_fim_sql))
            return result[0][0] if result else 0
        except Exception as e:
            print(f"Erro ao contar vendas do período: {e}")
            return 0
    
    def obter_produto_mais_vendido(self):
        """Obtém o produto mais vendido do dia atual"""
        try:
            hoje = datetime.now().strftime("%d/%m/%Y")
            query = """
                SELECT produto, SUM(quantidade) as total_vendido
                FROM historico_vendas 
                WHERE SUBSTR(data_hora, 1, 10) = ?
                GROUP BY produto 
                ORDER BY total_vendido DESC 
                LIMIT 1
            """
            result = self.execute_query(query, (hoje,))
            return result[0][0] if result else "Nenhum"
        except Exception as e:
            print(f"Erro ao obter produto mais vendido: {e}")
            return "Erro"
    
    def obter_valor_total_estoque(self):
        """Calcula valor total do estoque atual"""
        try:
            query = "SELECT COALESCE(SUM(quantidade * preco), 0) FROM estoque"
            result = self.execute_query(query)
            return result[0][0] if result else 0.0
        except Exception as e:
            print(f"Erro ao calcular valor do estoque: {e}")
            return 0.0
    
    def contar_produtos_estoque_baixo(self, limite=5):
        """Conta produtos com estoque abaixo do limite"""
        try:
            query = "SELECT COUNT(*) FROM estoque WHERE quantidade < ?"
            result = self.execute_query(query, (limite,))
            return result[0][0] if result else 0
        except Exception as e:
            print(f"Erro ao contar produtos com estoque baixo: {e}")
            return 0
    
    def obter_vendas_ultimos_dias(self, dias=7):
        """Obtém dados de vendas dos últimos X dias"""
        try:
            query = """
                SELECT 
                    SUBSTR(data_hora, 1, 10) as data,
                    COALESCE(SUM(valor_total), 0) as receita,
                    COALESCE(SUM(quantidade), 0) as quantidade_total
                FROM historico_vendas 
                GROUP BY SUBSTR(data_hora, 1, 10)
                ORDER BY DATE(SUBSTR(data_hora, 7, 4) || '-' || 
                            SUBSTR(data_hora, 4, 2) || '-' || 
                            SUBSTR(data_hora, 1, 2)) DESC
                LIMIT ?
            """
            result = self.execute_query(query, (dias,))
            return result[::-1]  # Inverter para ordem cronológica
        except Exception as e:
            print(f"Erro ao obter vendas dos últimos dias: {e}")
            return []
    
    def obter_top_produtos_receita(self, limite=10):
        """Obtém top produtos por receita total"""
        try:
            query = """
                SELECT 
                    produto,
                    COALESCE(SUM(valor_total), 0) as receita_total,
                    COALESCE(SUM(quantidade), 0) as quantidade_total
                FROM historico_vendas 
                GROUP BY produto 
                ORDER BY receita_total DESC 
                LIMIT ?
            """
            result = self.execute_query(query, (limite,))
            return result
        except Exception as e:
            print(f"Erro ao obter top produtos por receita: {e}")
            return []
    
    def obter_vendas_por_horario(self):
        """Obtém análise de vendas por horário do dia"""
        try:
            query = """
                SELECT 
                    CAST(SUBSTR(data_hora, 12, 2) AS INTEGER) as hora,
                    COALESCE(SUM(valor_total), 0) as receita_hora
                FROM historico_vendas 
                WHERE LENGTH(data_hora) >= 13
                GROUP BY CAST(SUBSTR(data_hora, 12, 2) AS INTEGER)
                ORDER BY hora
            """
            result = self.execute_query(query)
            return result
        except Exception as e:
            print(f"Erro ao obter vendas por horário: {e}")
            return []
