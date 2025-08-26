"""
Controlador para gerenciamento de histórico de vendas
"""

from src.estoque.database import DatabaseManager
from datetime import datetime, timedelta


class HistoricoController:
    def __init__(self):
        self.db = DatabaseManager()
        
    def registrar_venda(self, produto, quantidade):
        """Registra uma nova venda"""
        if not produto or not produto.strip():
            raise ValueError("Nome do produto não pode estar vazio")
            
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
            
        produto = produto.strip().title()
        return self.db.registrar_venda(produto, quantidade)
        
    def listar_historico(self, limite=None):
        """Lista o histórico de vendas"""
        return self.db.listar_historico(limite)
        
    def buscar_vendas_produto(self, produto):
        """Busca vendas de um produto específico"""
        if not produto or not produto.strip():
            return []
            
        produto = produto.strip()
        return self.db.buscar_vendas_por_produto(produto)
        
    def obter_estatisticas(self):
        """Obtém estatísticas de vendas"""
        return self.db.obter_estatisticas_vendas()
        
    def vendas_por_periodo(self, data_inicio=None, data_fim=None):
        """Obtém vendas por período específico"""
        historico = self.listar_historico()
        
        if not data_inicio and not data_fim:
            return historico
            
        vendas_periodo = []
        
        for venda in historico:
            venda_id, produto, quantidade, data_hora_str = venda
            
            try:
                # Converter string de data para datetime
                data_venda = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M:%S")
                
                # Verificar se está no período
                dentro_periodo = True
                
                if data_inicio:
                    if data_venda.date() < data_inicio:
                        dentro_periodo = False
                        
                if data_fim:
                    if data_venda.date() > data_fim:
                        dentro_periodo = False
                        
                if dentro_periodo:
                    vendas_periodo.append(venda)
                    
            except ValueError:
                # Se não conseguir converter a data, incluir na lista
                vendas_periodo.append(venda)
                
        return vendas_periodo
        
    def vendas_hoje(self):
        """Obtém vendas do dia atual"""
        hoje = datetime.now().date()
        return self.vendas_por_periodo(hoje, hoje)
        
    def vendas_semana(self):
        """Obtém vendas da semana atual"""
        hoje = datetime.now().date()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        return self.vendas_por_periodo(inicio_semana, hoje)
        
    def vendas_mes(self):
        """Obtém vendas do mês atual"""
        hoje = datetime.now().date()
        inicio_mes = hoje.replace(day=1)
        return self.vendas_por_periodo(inicio_mes, hoje)
        
    def produto_mais_vendido(self):
        """Retorna o produto mais vendido"""
        estatisticas = self.obter_estatisticas()
        
        if not estatisticas:
            return None
            
        # As estatísticas já vêm ordenadas por total vendido (DESC)
        produto, total_vendido, num_vendas = estatisticas[0]
        return {
            'produto': produto,
            'total_vendido': total_vendido,
            'num_vendas': num_vendas
        }
        
    def relatorio_vendas(self):
        """Gera um relatório completo de vendas"""
        historico = self.listar_historico()
        estatisticas = self.obter_estatisticas()
        
        # Calcular totais
        total_vendas = len(historico)
        total_itens = sum(venda[2] for venda in historico)  # venda[2] é a quantidade
        
        # Vendas por período
        vendas_hoje = len(self.vendas_hoje())
        vendas_semana = len(self.vendas_semana())
        vendas_mes = len(self.vendas_mes())
        
        # Produto mais vendido
        mais_vendido = self.produto_mais_vendido()
        
        relatorio = {
            'total_vendas': total_vendas,
            'total_itens': total_itens,
            'vendas_hoje': vendas_hoje,
            'vendas_semana': vendas_semana,
            'vendas_mes': vendas_mes,
            'produto_mais_vendido': mais_vendido,
            'estatisticas_produtos': estatisticas
        }
        
        return relatorio
