"""
Controlador para exportação de dados
"""

import pandas as pd
from datetime import datetime
import os
from src.estoque.database import DatabaseManager


class ExportController:
    def __init__(self):
        self.db = DatabaseManager()
        
    def exportar_estoque(self, arquivo=None):
        """Exporta dados do estoque para Excel"""
        try:
            # Buscar dados do estoque
            estoque = self.db.listar_estoque()
            
            if not estoque:
                raise ValueError("Nenhum produto encontrado no estoque")
                
            # Criar DataFrame
            df = pd.DataFrame(estoque, columns=['Produto', 'Quantidade'])
            
            # Gerar nome do arquivo se não fornecido
            if not arquivo:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                arquivo = f"data/estoque_{timestamp}.xlsx"
                
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(arquivo), exist_ok=True)
            
            # Exportar para Excel
            with pd.ExcelWriter(arquivo, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Estoque', index=False)
                
                # Formatação básica
                worksheet = writer.sheets['Estoque']
                worksheet.column_dimensions['A'].width = 30
                worksheet.column_dimensions['B'].width = 15
                
            return arquivo
            
        except Exception as e:
            print(f"Erro ao exportar estoque: {str(e)}")
            return None
            
    def exportar_historico(self, arquivo=None):
        """Exporta histórico de vendas para Excel"""
        try:
            # Buscar dados do histórico
            historico = self.db.listar_historico()
            
            if not historico:
                raise ValueError("Nenhuma venda encontrada no histórico")
                
            # Criar DataFrame
            df = pd.DataFrame(historico, columns=['ID', 'Produto', 'Quantidade', 'Data/Hora'])
            
            # Gerar nome do arquivo se não fornecido
            if not arquivo:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                arquivo = f"data/historico_{timestamp}.xlsx"
                
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(arquivo), exist_ok=True)
            
            # Exportar para Excel
            with pd.ExcelWriter(arquivo, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Histórico', index=False)
                
                # Formatação básica
                worksheet = writer.sheets['Histórico']
                worksheet.column_dimensions['A'].width = 10
                worksheet.column_dimensions['B'].width = 25
                worksheet.column_dimensions['C'].width = 12
                worksheet.column_dimensions['D'].width = 20
                
            return arquivo
            
        except Exception as e:
            print(f"Erro ao exportar histórico: {str(e)}")
            return None
            
    def exportar_estatisticas(self, arquivo=None):
        """Exporta estatísticas de vendas para Excel"""
        try:
            # Buscar estatísticas
            estatisticas = self.db.obter_estatisticas_vendas()
            
            if not estatisticas:
                raise ValueError("Nenhuma estatística encontrada")
                
            # Criar DataFrame
            df = pd.DataFrame(estatisticas, columns=['Produto', 'Total Vendido', 'Número de Vendas'])
            
            # Gerar nome do arquivo se não fornecido
            if not arquivo:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                arquivo = f"data/estatisticas_{timestamp}.xlsx"
                
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(arquivo), exist_ok=True)
            
            # Exportar para Excel
            with pd.ExcelWriter(arquivo, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Estatísticas', index=False)
                
                # Formatação básica
                worksheet = writer.sheets['Estatísticas']
                worksheet.column_dimensions['A'].width = 25
                worksheet.column_dimensions['B'].width = 15
                worksheet.column_dimensions['C'].width = 18
                
            return arquivo
            
        except Exception as e:
            print(f"Erro ao exportar estatísticas: {str(e)}")
            return None
            
    def exportar_relatorio_completo(self, arquivo=None):
        """Exporta um relatório completo com todas as informações"""
        try:
            # Buscar todos os dados
            estoque = self.db.listar_estoque()
            historico = self.db.listar_historico()
            estatisticas = self.db.obter_estatisticas_vendas()
            
            # Gerar nome do arquivo se não fornecido
            if not arquivo:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                arquivo = f"data/relatorio_completo_{timestamp}.xlsx"
                
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(arquivo), exist_ok=True)
            
            # Criar arquivo Excel com múltiplas abas
            with pd.ExcelWriter(arquivo, engine='openpyxl') as writer:
                
                # Aba Estoque
                if estoque:
                    df_estoque = pd.DataFrame(estoque, columns=['Produto', 'Quantidade'])
                    df_estoque.to_excel(writer, sheet_name='Estoque', index=False)
                    
                    worksheet = writer.sheets['Estoque']
                    worksheet.column_dimensions['A'].width = 30
                    worksheet.column_dimensions['B'].width = 15
                
                # Aba Histórico
                if historico:
                    df_historico = pd.DataFrame(historico, columns=['ID', 'Produto', 'Quantidade', 'Data/Hora'])
                    df_historico.to_excel(writer, sheet_name='Histórico', index=False)
                    
                    worksheet = writer.sheets['Histórico']
                    worksheet.column_dimensions['A'].width = 10
                    worksheet.column_dimensions['B'].width = 25
                    worksheet.column_dimensions['C'].width = 12
                    worksheet.column_dimensions['D'].width = 20
                
                # Aba Estatísticas
                if estatisticas:
                    df_stats = pd.DataFrame(estatisticas, columns=['Produto', 'Total Vendido', 'Número de Vendas'])
                    df_stats.to_excel(writer, sheet_name='Estatísticas', index=False)
                    
                    worksheet = writer.sheets['Estatísticas']
                    worksheet.column_dimensions['A'].width = 25
                    worksheet.column_dimensions['B'].width = 15
                    worksheet.column_dimensions['C'].width = 18
                
            return arquivo
            
        except Exception as e:
            print(f"Erro ao exportar relatório completo: {str(e)}")
            return None
