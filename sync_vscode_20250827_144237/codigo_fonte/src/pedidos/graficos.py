"""
Controlador para geração de gráficos
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os
from src.estoque.database import DatabaseManager


class GraficoController:
    def __init__(self):
        self.db = DatabaseManager()
        
    def gerar_grafico_vendas(self):
        """Gera gráfico de vendas por produto"""
        try:
            # Configurar matplotlib para interface gráfica
            plt.rcParams['font.size'] = 10
            plt.rcParams['figure.figsize'] = (15, 12)
            
            # Buscar estatísticas financeiras de vendas
            estatisticas = self.db.obter_estatisticas_financeiras()
            
            if not estatisticas:
                raise ValueError("Nenhuma venda encontrada para gerar gráfico")
                
            # Limitar a 10 produtos mais vendidos para melhor visualização
            estatisticas = estatisticas[:10]
            
            # Extrair dados
            produtos = [stat[0] for stat in estatisticas]
            quantidades = [stat[1] for stat in estatisticas]
            receitas = [stat[2] for stat in estatisticas]
            
            # Criar figura com subplots 2x2
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
            
            # Gráfico 1: Barras - Quantidade vendida
            bars1 = ax1.bar(produtos, quantidades, color='skyblue', edgecolor='navy', alpha=0.7)
            ax1.set_title('Produtos Mais Vendidos (Quantidade)', fontsize=12, fontweight='bold')
            ax1.set_xlabel('Produtos')
            ax1.set_ylabel('Quantidade Vendida')
            ax1.tick_params(axis='x', rotation=45)
            
            # Adicionar valores nas barras
            for bar, quantidade in zip(bars1, quantidades):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(quantidade)}', ha='center', va='bottom')
            
            # Gráfico 2: Barras - Receita por produto
            bars2 = ax2.bar(produtos, receitas, color='lightgreen', edgecolor='darkgreen', alpha=0.7)
            ax2.set_title('Receita por Produto (R$)', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Produtos')
            ax2.set_ylabel('Receita (R$)')
            ax2.tick_params(axis='x', rotation=45)
            
            # Adicionar valores nas barras
            for bar, receita in zip(bars2, receitas):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'R$ {receita:.0f}', ha='center', va='bottom')
            
            # Gráfico 3: Pizza - Distribuição de quantidade
            colors1 = plt.cm.Set3(range(len(produtos)))
            wedges1, texts1, autotexts1 = ax3.pie(quantidades, labels=produtos, autopct='%1.1f%%',
                                                 colors=colors1, startangle=90)
            ax3.set_title('Distribuição de Vendas (Quantidade)', fontsize=12, fontweight='bold')
            
            # Gráfico 4: Pizza - Distribuição de receita
            colors2 = plt.cm.Pastel1(range(len(produtos)))
            wedges2, texts2, autotexts2 = ax4.pie(receitas, labels=produtos, autopct='%1.1f%%',
                                                 colors=colors2, startangle=90)
            ax4.set_title('Distribuição de Receita (R$)', fontsize=12, fontweight='bold')
            
            # Melhorar aparência do gráfico de pizza
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            # Ajustar layout
            plt.tight_layout()
            
            # Salvar gráfico
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_grafico = f"data/grafico_vendas_{timestamp}.png"
            
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(arquivo_grafico), exist_ok=True)
            
            plt.savefig(arquivo_grafico, dpi=300, bbox_inches='tight')
            
            # Exibir gráfico
            plt.show()
            
            return arquivo_grafico
            
        except Exception as e:
            print(f"Erro ao gerar gráfico: {str(e)}")
            raise e
            
    def gerar_grafico_estoque(self):
        """Gera gráfico do estoque atual"""
        try:
            plt.rcParams['font.size'] = 10
            plt.rcParams['figure.figsize'] = (10, 6)
            
            # Buscar dados do estoque
            estoque = self.db.listar_estoque()
            
            if not estoque:
                raise ValueError("Nenhum produto encontrado no estoque")
                
            # Extrair dados
            produtos = [item[0] for item in estoque]
            quantidades = [item[1] for item in estoque]
            
            # Criar gráfico de barras horizontais
            fig, ax = plt.subplots(figsize=(10, max(6, len(produtos) * 0.5)))
            
            bars = ax.barh(produtos, quantidades, color='lightgreen', edgecolor='darkgreen', alpha=0.7)
            ax.set_title('Estoque Atual de Produtos', fontsize=14, fontweight='bold')
            ax.set_xlabel('Quantidade em Estoque')
            ax.set_ylabel('Produtos')
            
            # Adicionar valores nas barras
            for bar, quantidade in zip(bars, quantidades):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2.,
                       f'{int(quantidade)}', ha='left', va='center', fontweight='bold')
            
            # Destacar produtos com estoque baixo (<=5)
            for i, (bar, quantidade) in enumerate(zip(bars, quantidades)):
                if quantidade <= 5:
                    bar.set_color('lightcoral')
                    bar.set_edgecolor('darkred')
            
            # Adicionar legenda
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='lightgreen', edgecolor='darkgreen', label='Estoque Normal'),
                Patch(facecolor='lightcoral', edgecolor='darkred', label='Estoque Baixo (≤5)')
            ]
            ax.legend(handles=legend_elements, loc='lower right')
            
            plt.tight_layout()
            
            # Salvar gráfico
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_grafico = f"data/grafico_estoque_{timestamp}.png"
            
            os.makedirs(os.path.dirname(arquivo_grafico), exist_ok=True)
            plt.savefig(arquivo_grafico, dpi=300, bbox_inches='tight')
            
            # Exibir gráfico
            plt.show()
            
            return arquivo_grafico
            
        except Exception as e:
            print(f"Erro ao gerar gráfico de estoque: {str(e)}")
            raise e
            
    def gerar_grafico_vendas_tempo(self):
        """Gera gráfico de vendas ao longo do tempo"""
        try:
            plt.rcParams['font.size'] = 10
            plt.rcParams['figure.figsize'] = (12, 6)
            
            # Buscar histórico de vendas
            historico = self.db.listar_historico()
            
            if not historico:
                raise ValueError("Nenhuma venda encontrada no histórico")
                
            # Processar dados por data
            vendas_por_data = {}
            
            for venda in historico:
                venda_id, produto, quantidade, data_hora_str = venda
                
                try:
                    # Converter para datetime e extrair apenas a data
                    data_hora = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M:%S")
                    data = data_hora.date()
                    
                    if data not in vendas_por_data:
                        vendas_por_data[data] = 0
                    vendas_por_data[data] += quantidade
                    
                except ValueError:
                    # Ignorar registros com formato de data inválido
                    continue
                    
            if not vendas_por_data:
                raise ValueError("Nenhuma venda com data válida encontrada")
                
            # Ordenar por data
            datas = sorted(vendas_por_data.keys())
            quantidades = [vendas_por_data[data] for data in datas]
            
            # Criar gráfico de linha
            fig, ax = plt.subplots(figsize=(12, 6))
            
            ax.plot(datas, quantidades, marker='o', linestyle='-', linewidth=2, markersize=6,
                   color='blue', markerfacecolor='red', alpha=0.7)
            
            ax.set_title('Evolução das Vendas ao Longo do Tempo', fontsize=14, fontweight='bold')
            ax.set_xlabel('Data')
            ax.set_ylabel('Quantidade Vendida')
            
            # Formatação das datas no eixo X
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(datas)//10)))
            
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            
            # Grid para melhor visualização
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Salvar gráfico
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_grafico = f"data/grafico_vendas_tempo_{timestamp}.png"
            
            os.makedirs(os.path.dirname(arquivo_grafico), exist_ok=True)
            plt.savefig(arquivo_grafico, dpi=300, bbox_inches='tight')
            
            # Exibir gráfico
            plt.show()
            
            return arquivo_grafico
            
        except Exception as e:
            print(f"Erro ao gerar gráfico de vendas por tempo: {str(e)}")
            raise e
