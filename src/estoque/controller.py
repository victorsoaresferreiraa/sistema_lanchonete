"""
Controlador para gerenciamento de estoque
"""

from .database import DatabaseManager


class EstoqueController:
    def __init__(self):
        self.db = DatabaseManager()
        
    def adicionar_produto(self, produto, quantidade):
        """Adiciona um novo produto ao estoque"""
        if not produto or not produto.strip():
            raise ValueError("Nome do produto não pode estar vazio")
            
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")
            
        produto = produto.strip().title()  # Capitalizar nome do produto
        return self.db.inserir_produto(produto, quantidade)
        
    def atualizar_produto(self, produto, quantidade):
        """Atualiza a quantidade de um produto existente"""
        if not produto or not produto.strip():
            raise ValueError("Nome do produto não pode estar vazio")
            
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")
            
        produto = produto.strip().title()
        return self.db.atualizar_quantidade(produto, quantidade)
        
    def consultar_produto(self, produto):
        """Consulta a quantidade disponível de um produto"""
        if not produto or not produto.strip():
            return None
            
        produto = produto.strip().title()
        return self.db.consultar_produto(produto)
        
    def listar_estoque(self):
        """Lista todos os produtos em estoque"""
        return self.db.listar_estoque()
        
    def remover_produto(self, produto):
        """Remove um produto do estoque"""
        if not produto or not produto.strip():
            raise ValueError("Nome do produto não pode estar vazio")
            
        produto = produto.strip().title()
        return self.db.remover_produto(produto)
        
    def verificar_estoque_baixo(self, limite=5):
        """Verifica produtos com estoque baixo"""
        estoque = self.listar_estoque()
        produtos_baixo = []
        
        for produto, quantidade in estoque:
            if quantidade <= limite:
                produtos_baixo.append((produto, quantidade))
                
        return produtos_baixo
        
    def obter_valor_total_estoque(self, precos=None):
        """Calcula o valor total do estoque (se preços forem fornecidos)"""
        if not precos:
            return None
            
        estoque = self.listar_estoque()
        valor_total = 0
        
        for produto, quantidade in estoque:
            if produto in precos:
                valor_total += quantidade * precos[produto]
                
        return valor_total
        
    def buscar_produtos(self, termo):
        """Busca produtos por termo"""
        if not termo or not termo.strip():
            return self.listar_estoque()
            
        termo = termo.strip().lower()
        estoque = self.listar_estoque()
        produtos_encontrados = []
        
        for produto, quantidade in estoque:
            if termo in produto.lower():
                produtos_encontrados.append((produto, quantidade))
                
        return produtos_encontrados
