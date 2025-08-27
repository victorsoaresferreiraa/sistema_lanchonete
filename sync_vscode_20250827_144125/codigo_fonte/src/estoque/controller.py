"""
Controlador para gerenciamento de estoque
"""

from .database import DatabaseManager


class EstoqueController:
    def __init__(self):
        self.db = DatabaseManager()
        
    def adicionar_produto(self, produto, quantidade, preco=0.0, categoria='Geral', codigo_barras=''):
        """Adiciona um novo produto ao estoque"""
        if not produto or not produto.strip():
            raise ValueError("Nome do produto não pode estar vazio")
            
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")
            
        if preco < 0:
            raise ValueError("Preço não pode ser negativo")
            
        produto = produto.strip().title()  # Capitalizar nome do produto
        categoria = categoria.strip().title() if categoria else 'Geral'
        codigo_barras = codigo_barras.strip() if codigo_barras else ''
        
        return self.db.inserir_produto(produto, quantidade, preco, categoria, codigo_barras)
        
    def atualizar_produto(self, produto, quantidade, preco=None):
        """Atualiza a quantidade de um produto existente"""
        if not produto or not produto.strip():
            raise ValueError("Nome do produto não pode estar vazio")
            
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")
            
        produto = produto.strip().title()
        
        if preco is not None:
            if preco < 0:
                raise ValueError("Preço não pode ser negativo")
            # Atualizar quantidade e preço
            sucesso_qtd = self.db.atualizar_quantidade(produto, quantidade)
            sucesso_preco = self.db.atualizar_preco(produto, preco)
            return sucesso_qtd and sucesso_preco
        else:
            # Atualizar apenas quantidade
            return self.db.atualizar_quantidade(produto, quantidade)
            
    def atualizar_produto_completo(self, produto, quantidade, preco, categoria, codigo_barras):
        """Atualiza todas as informações de um produto"""
        if not produto or not produto.strip():
            raise ValueError("Nome do produto não pode estar vazio")
            
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")
            
        if preco < 0:
            raise ValueError("Preço não pode ser negativo")
            
        produto = produto.strip().title()
        categoria = categoria.strip().title() if categoria else 'Geral'
        codigo_barras = codigo_barras.strip() if codigo_barras else ''
        
        return self.db.atualizar_produto_completo(produto, quantidade, preco, categoria, codigo_barras)
        
    def consultar_produto(self, produto):
        """Consulta a quantidade disponível de um produto"""
        if not produto or not produto.strip():
            return None
            
        produto = produto.strip().title()
        return self.db.consultar_produto(produto)
        
    def consultar_produto_completo(self, produto):
        """Consulta todas as informações de um produto"""
        if not produto or not produto.strip():
            return None
            
        produto = produto.strip().title()
        return self.db.consultar_produto_completo(produto)
        
    def listar_estoque(self):
        """Lista todos os produtos em estoque"""
        return self.db.listar_estoque()
        
    def listar_estoque_completo(self):
        """Lista todos os produtos com informações completas"""
        return self.db.listar_estoque_completo()
        
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
        
    def obter_valor_total_estoque(self):
        """Calcula o valor total do estoque usando preços cadastrados"""
        estoque = self.listar_estoque_completo()
        valor_total = 0
        
        for item in estoque:
            produto, quantidade, preco = item[0], item[1], item[2]
            valor_total += quantidade * preco
                
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
