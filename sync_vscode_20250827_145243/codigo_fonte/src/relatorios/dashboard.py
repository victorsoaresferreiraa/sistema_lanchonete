"""
📊 DASHBOARD FINANCEIRO COMPLETO - Sistema da Lanchonete

Este módulo implementa um painel executivo completo que mostra:
- Métricas financeiras em tempo real
- Gráficos de análise de vendas  
- Performance de produtos
- Tendências de horários
- Alertas de gestão

COMO FUNCIONA:
1. DatabaseManager: busca dados do banco SQLite
2. Matplotlib: cria gráficos interativos
3. Tkinter: exibe tudo em interface amigável
4. Atualização automática: dados sempre atualizados

PARA O USUÁRIO DA LANCHONETE:
- Vê quanto vendeu hoje em tempo real
- Identifica produtos que mais vendem
- Descobre melhores horários de movimento
- Recebe alertas de estoque baixo
- Acompanha crescimento do negócio
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import sqlite3
from src.estoque.database import DatabaseManager
from src.utils.helpers import centralizar_janela


class DashboardWindow:
    """
    🎯 CLASSE PRINCIPAL DO DASHBOARD
    
    Esta classe cria uma janela completa de análise financeira que ajuda
    o dono da lanchonete a entender seu negócio em tempo real.
    
    O QUE FAZ:
    - Conecta com o banco de dados para buscar informações
    - Calcula métricas importantes automaticamente  
    - Cria gráficos visuais fáceis de entender
    - Atualiza dados em tempo real
    - Mostra alertas importantes
    
    PARA QUE SERVE:
    - Saber quanto está vendendo no dia
    - Ver quais produtos vendem mais
    - Descobrir horários de pico
    - Controlar estoque baixo
    - Acompanhar crescimento do negócio
    """
    
    def __init__(self, parent):
        """
        INICIALIZAÇÃO DO DASHBOARD
        
        O que acontece aqui:
        1. Conecta com o banco de dados (self.db)
        2. Cria a janela principal (self.window)  
        3. Configura o tamanho e posição
        4. Chama setup_ui() para criar a interface
        5. Chama atualizar_dashboard() para carregar dados
        """
        self.parent = parent
        self.db = DatabaseManager()  # Conexão com banco de dados
        
        # Criar janela principal
        self.window = tk.Toplevel(parent)
        self.window.title("📊 Dashboard Executivo - Análise Financeira")
        self.window.geometry("1300x850")  # Tamanho otimizado para visualização
        self.window.resizable(True, True)
        
        # Tornar janela modal (foco exclusivo)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Configurar cores e estilo
        self.cores = {
            'receita': '#2E8B57',      # Verde para receita
            'vendas': '#4169E1',       # Azul para vendas
            'produtos': '#FF8C00',     # Laranja para produtos
            'estoque': '#DC143C',      # Vermelho para alertas
            'crescimento': '#9370DB'   # Roxo para crescimento
        }
        
        # Configurar interface
        self.setup_ui()
        centralizar_janela(self.window)
        
        # Carregar dados iniciais
        self.atualizar_dashboard()
        
    def setup_ui(self):
        """
        🎨 CONFIGURAÇÃO DA INTERFACE VISUAL
        
        Esta função cria toda a estrutura visual do dashboard.
        É como montar a "mesa" onde vamos colocar as informações.
        
        ESTRUTURA CRIADA:
        1. Frame principal (container geral)
        2. Título chamativo  
        3. Área de métricas (números importantes)
        4. Área de gráficos (análises visuais)
        5. Botões de controle (atualizar, exportar, fechar)
        
        EXPLICAÇÃO TÉCNICA:
        - ttk.Frame = caixas para organizar elementos
        - pack() = posiciona elementos na tela
        - LabelFrame = caixa com título
        - Notebook = abas para múltiplos gráficos
        """
        
        # === 1. CONTAINER PRINCIPAL ===
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # === 2. TÍTULO DO DASHBOARD ===
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="📊 Dashboard Executivo - Lanchonete",
            font=("Arial", 18, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        # Data/hora da última atualização
        self.update_time_label = ttk.Label(
            header_frame,
            text="",
            font=("Arial", 10),
            foreground="gray"
        )
        self.update_time_label.pack(side=tk.RIGHT)
        
        # === 3. ÁREA DE MÉTRICAS PRINCIPAIS ===
        metrics_frame = ttk.LabelFrame(
            main_frame, 
            text="💰 Métricas Financeiras - Visão Rápida", 
            padding="12"
        )
        metrics_frame.pack(fill=tk.X, pady=(0, 12))
        
        # Configurar grid de métricas
        self.setup_metrics_grid(metrics_frame)
        
        # === 4. ÁREA DE ALERTAS ===
        self.alerts_frame = ttk.LabelFrame(
            main_frame,
            text="🚨 Alertas de Gestão",
            padding="8"
        )
        self.alerts_frame.pack(fill=tk.X, pady=(0, 12))
        
        self.alerts_text = tk.Text(
            self.alerts_frame,
            height=2,
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        self.alerts_text.pack(fill=tk.X)
        
        # === 5. ÁREA DE GRÁFICOS ===
        charts_frame = ttk.LabelFrame(
            main_frame, 
            text="📈 Análise Visual de Desempenho", 
            padding="10"
        )
        charts_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Notebook para múltiplos gráficos
        self.notebook = ttk.Notebook(charts_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Configurar abas dos gráficos
        self.setup_chart_tabs()
        
        # === 6. BOTÕES DE CONTROLE ===
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botão atualizar
        btn_atualizar = ttk.Button(
            controls_frame,
            text="🔄 Atualizar Dados",
            command=self.atualizar_dashboard
        )
        btn_atualizar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão exportar
        btn_exportar = ttk.Button(
            controls_frame,
            text="📄 Exportar Relatório",
            command=self.exportar_relatorio
        )
        btn_exportar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão ajuda
        btn_ajuda = ttk.Button(
            controls_frame,
            text="❓ Como Usar",
            command=self.mostrar_ajuda
        )
        btn_ajuda.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão fechar
        btn_fechar = ttk.Button(
            controls_frame,
            text="❌ Fechar",
            command=self.window.destroy
        )
        btn_fechar.pack(side=tk.RIGHT)
        
    def setup_metrics_grid(self, parent):
        """
        💼 CONFIGURAÇÃO DAS MÉTRICAS PRINCIPAIS
        
        Esta função cria os "cartões" de informações importantes que
        o dono da lanchonete precisa ver rapidamente.
        
        MÉTRICAS CRIADAS:
        Linha 1: Desempenho do dia
        - Receita Hoje: quanto vendeu hoje
        - Vendas Hoje: quantas vendas fez
        - Produto Top: produto que mais vende
        - Ticket Médio: valor médio por venda
        
        Linha 2: Controle operacional  
        - Valor Estoque: quanto vale o estoque
        - Estoque Baixo: quantos produtos acabando
        - Receita Mês: total do mês atual
        - Crescimento: comparação com período anterior
        
        COMO FUNCIONA:
        1. Cria frames (caixinhas) para cada métrica
        2. Adiciona título e valor para cada uma
        3. Usa cores diferentes para fácil identificação
        4. Organiza em grid (2 linhas x 4 colunas)
        """
        
        # Dicionário para armazenar os labels das métricas
        self.metrics_labels = {}
        
        # === LINHA 1: MÉTRICAS DO DIA ===
        metrics_row1 = [
            ("receita_hoje", "💰 Receita Hoje", self.cores['receita'], "Quanto vendeu hoje"),
            ("vendas_hoje", "🛒 Vendas Hoje", self.cores['vendas'], "Número de vendas"),
            ("produto_top", "🏆 Produto Top", self.cores['produtos'], "Produto mais vendido"),
            ("ticket_medio", "🎯 Ticket Médio", self.cores['crescimento'], "Valor médio por venda")
        ]
        
        for i, (key, label, color, tooltip) in enumerate(metrics_row1):
            # Criar frame para cada métrica
            metric_frame = ttk.Frame(parent, relief="raised", borderwidth=1)
            metric_frame.grid(row=0, column=i, padx=8, pady=5, sticky=tk.EW, ipadx=10, ipady=5)
            
            # Título da métrica
            title_label = ttk.Label(
                metric_frame, 
                text=label, 
                font=("Arial", 10, "bold")
            )
            title_label.pack()
            
            # Valor da métrica (será atualizado dinamicamente)
            self.metrics_labels[key] = ttk.Label(
                metric_frame, 
                text="Carregando...", 
                font=("Arial", 16, "bold"), 
                foreground=color
            )
            self.metrics_labels[key].pack()
            
            # Tooltip explicativo
            tooltip_label = ttk.Label(
                metric_frame,
                text=tooltip,
                font=("Arial", 8),
                foreground="gray"
            )
            tooltip_label.pack()
        
        # === LINHA 2: MÉTRICAS DE CONTROLE ===
        metrics_row2 = [
            ("estoque_total", "📦 Valor Estoque", self.cores['estoque'], "Valor total em estoque"),
            ("produtos_baixo", "⚠️ Estoque Baixo", "#FF4500", "Produtos acabando"),
            ("receita_mes", "📅 Receita Mês", self.cores['receita'], "Total do mês atual"),
            ("crescimento", "📈 Crescimento", self.cores['crescimento'], "Comparação período anterior")
        ]
        
        for i, (key, label, color, tooltip) in enumerate(metrics_row2):
            # Criar frame para cada métrica
            metric_frame = ttk.Frame(parent, relief="raised", borderwidth=1)
            metric_frame.grid(row=1, column=i, padx=8, pady=5, sticky=tk.EW, ipadx=10, ipady=5)
            
            # Título da métrica
            title_label = ttk.Label(
                metric_frame, 
                text=label, 
                font=("Arial", 10, "bold")
            )
            title_label.pack()
            
            # Valor da métrica
            self.metrics_labels[key] = ttk.Label(
                metric_frame, 
                text="Carregando...", 
                font=("Arial", 16, "bold"), 
                foreground=color
            )
            self.metrics_labels[key].pack()
            
            # Tooltip explicativo
            tooltip_label = ttk.Label(
                metric_frame,
                text=tooltip,
                font=("Arial", 8),
                foreground="gray"
            )
            tooltip_label.pack()
        
        # Configurar colunas para expandir uniformemente
        for i in range(4):
            parent.grid_columnconfigure(i, weight=1)
            
    def setup_chart_tabs(self):
        """
        📈 CONFIGURAÇÃO DAS ABAS DE GRÁFICOS
        
        Esta função cria as abas onde ficarão os gráficos visuais.
        Cada aba mostra uma análise diferente dos dados.
        
        ABAS CRIADAS:
        1. Vendas Diárias: gráfico de receita por dia
        2. Performance Produtos: quais produtos vendem mais
        3. Análise Horários: melhores horários do dia
        4. Comparação Mensal: evolução mês a mês
        
        EXPLICAÇÃO TÉCNICA:
        - ttk.Notebook = container de abas
        - ttk.Frame = cada aba é um frame
        - notebook.add() = adiciona aba ao container
        """
        
        # Aba 1: Análise de Vendas Diárias
        self.tab_vendas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_vendas, text="📊 Vendas Diárias")
        
        # Aba 2: Performance dos Produtos
        self.tab_produtos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_produtos, text="🏆 Top Produtos")
        
        # Aba 3: Análise por Horário
        self.tab_horarios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_horarios, text="🕐 Horários de Pico")
        
        # Aba 4: Comparação Mensal
        self.tab_comparacao = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_comparacao, text="📅 Evolução Mensal")
        
    def atualizar_dashboard(self):
        """
        🔄 ATUALIZAÇÃO COMPLETA DO DASHBOARD
        
        Esta é a função principal que busca todos os dados novos
        e atualiza a interface visual com as informações atuais.
        
        SEQUÊNCIA DE ATUALIZAÇÃO:
        1. Atualizar métricas numéricas
        2. Atualizar alertas de gestão
        3. Atualizar todos os gráficos
        4. Marcar horário da atualização
        
        É chamada automaticamente quando:
        - Dashboard é aberto
        - Usuário clica em "Atualizar"
        - Periodicamente (se configurado)
        """
        try:
            print("🔄 Iniciando atualização do dashboard...")
            
            # 1. Atualizar métricas principais
            self.atualizar_metricas()
            
            # 2. Atualizar alertas
            self.atualizar_alertas()
            
            # 3. Atualizar gráficos
            self.atualizar_graficos()
            
            # 4. Marcar horário da atualização
            agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.update_time_label.config(text=f"Última atualização: {agora}")
            
            print("✅ Dashboard atualizado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro na atualização: {e}")
            messagebox.showerror("Erro", f"Erro ao atualizar dashboard: {str(e)}")
        
    def atualizar_metricas(self):
        """
        💰 ATUALIZAÇÃO DAS MÉTRICAS FINANCEIRAS
        
        Esta função busca no banco de dados todos os números importantes
        e atualiza os cartões de métricas na interface.
        
        MÉTRICAS CALCULADAS:
        1. Receita do dia atual
        2. Número de vendas realizadas
        3. Produto mais vendido
        4. Ticket médio (receita ÷ número de vendas)
        5. Valor total do estoque
        6. Produtos com estoque baixo
        7. Receita do mês
        8. Crescimento comparado
        
        COMO FUNCIONA:
        - Busca dados do banco com self.db.método()
        - Calcula valores quando necessário
        - Atualiza os labels visuais com .config(text=...)
        - Trata erros para não quebrar o sistema
        """
        try:
            print("📊 Atualizando métricas...")
            
            # Data de hoje no formato brasileiro
            hoje = datetime.now().strftime("%d/%m/%Y")
            
            # === RECEITA HOJE ===
            receita_hoje = self.db.obter_receita_periodo(hoje, hoje)
            self.metrics_labels["receita_hoje"].config(
                text=f"R$ {receita_hoje:.2f}".replace('.', ',')
            )
            
            # === VENDAS HOJE ===
            vendas_hoje = self.db.contar_vendas_periodo(hoje, hoje)
            self.metrics_labels["vendas_hoje"].config(text=str(vendas_hoje))
            
            # === PRODUTO TOP ===
            produto_top = self.db.obter_produto_mais_vendido()
            # Limitar tamanho do nome para caber no cartão
            if len(produto_top) > 15:
                produto_top = produto_top[:12] + "..."
            self.metrics_labels["produto_top"].config(text=produto_top or "Nenhum")
            
            # === TICKET MÉDIO ===
            # Calcular: receita total ÷ número de vendas
            if vendas_hoje > 0:
                ticket_medio = receita_hoje / vendas_hoje
                self.metrics_labels["ticket_medio"].config(
                    text=f"R$ {ticket_medio:.2f}".replace('.', ',')
                )
            else:
                self.metrics_labels["ticket_medio"].config(text="R$ 0,00")
            
            # === VALOR TOTAL DO ESTOQUE ===
            estoque_total = self.db.obter_valor_total_estoque()
            self.metrics_labels["estoque_total"].config(
                text=f"R$ {estoque_total:.2f}".replace('.', ',')
            )
            
            # === PRODUTOS COM ESTOQUE BAIXO ===
            # Considerar baixo: menos de 5 unidades
            produtos_baixo = self.db.contar_produtos_estoque_baixo(5)
            self.metrics_labels["produtos_baixo"].config(text=str(produtos_baixo))
            
            # === RECEITA DO MÊS ===
            # Do dia 1 até hoje
            inicio_mes = datetime.now().replace(day=1).strftime("%d/%m/%Y")
            receita_mes = self.db.obter_receita_periodo(inicio_mes, hoje)
            self.metrics_labels["receita_mes"].config(
                text=f"R$ {receita_mes:.2f}".replace('.', ',')
            )
            
            # === CRESCIMENTO ===
            # Comparar hoje com mesmo dia da semana passada
            semana_passada = (datetime.now() - timedelta(days=7)).strftime("%d/%m/%Y")
            receita_semana_passada = self.db.obter_receita_periodo(semana_passada, semana_passada)
            
            if receita_semana_passada > 0:
                crescimento = ((receita_hoje - receita_semana_passada) / receita_semana_passada) * 100
                sinal = "+" if crescimento >= 0 else ""
                self.metrics_labels["crescimento"].config(text=f"{sinal}{crescimento:.1f}%")
            else:
                self.metrics_labels["crescimento"].config(text="N/A")
            
            print("✅ Métricas atualizadas")
            
        except Exception as e:
            print(f"❌ Erro ao atualizar métricas: {e}")
            # Em caso de erro, mostrar valores padrão
            for key in self.metrics_labels:
                self.metrics_labels[key].config(text="Erro")
    
    def atualizar_alertas(self):
        """
        🚨 ATUALIZAÇÃO DOS ALERTAS DE GESTÃO
        
        Esta função analisa a situação atual e gera alertas importantes
        para o dono da lanchonete tomar decisões rápidas.
        
        TIPOS DE ALERTAS:
        1. Estoque baixo - produtos acabando
        2. Sem vendas - dia sem movimento
        3. Produto em alta - vendendo muito
        4. Meta alcançada - bom desempenho
        
        COMO FUNCIONA:
        - Analisa dados atuais
        - Identifica situações importantes
        - Cria mensagens de alerta
        - Exibe na área de alertas
        """
        try:
            alertas = []
            hoje = datetime.now().strftime("%d/%m/%Y")
            
            # Verificar estoque baixo
            produtos_baixo = self.db.contar_produtos_estoque_baixo(5)
            if produtos_baixo > 0:
                alertas.append(f"⚠️ {produtos_baixo} produto(s) com estoque baixo (menos de 5 unidades)")
            
            # Verificar se há vendas hoje
            vendas_hoje = self.db.contar_vendas_periodo(hoje, hoje)
            if vendas_hoje == 0:
                alertas.append("📢 Nenhuma venda registrada hoje. Verifique se o sistema está sendo usado.")
            elif vendas_hoje >= 10:
                alertas.append(f"🎉 Ótimo! Já foram {vendas_hoje} vendas hoje!")
            
            # Verificar receita do dia
            receita_hoje = self.db.obter_receita_periodo(hoje, hoje)
            if receita_hoje >= 500:
                alertas.append(f"💰 Excelente! Receita de hoje já passou de R$ {receita_hoje:.2f}!")
            
            # Verificar produto em alta
            produto_top = self.db.obter_produto_mais_vendido()
            if produto_top and produto_top != "Nenhum":
                alertas.append(f"🔥 {produto_top} está em alta hoje!")
            
            # Se não há alertas, mostrar mensagem positiva
            if not alertas:
                alertas.append("✅ Tudo funcionando bem! Nenhum alerta no momento.")
            
            # Exibir alertas na interface
            self.alerts_text.delete(1.0, tk.END)
            self.alerts_text.insert(tk.END, "\n".join(alertas))
            
        except Exception as e:
            print(f"❌ Erro ao atualizar alertas: {e}")
            self.alerts_text.delete(1.0, tk.END)
            self.alerts_text.insert(tk.END, "❌ Erro ao carregar alertas")
            
    def atualizar_graficos(self):
        """
        📈 ATUALIZAÇÃO DE TODOS OS GRÁFICOS
        
        Esta função atualiza todas as análises visuais do dashboard.
        Cada gráfico mostra uma perspectiva diferente dos dados.
        
        GRÁFICOS ATUALIZADOS:
        1. Vendas diárias - tendência de receita
        2. Performance produtos - ranking de vendas
        3. Análise horários - picos de movimento
        4. Comparação mensal - evolução do negócio
        """
        try:
            print("📈 Atualizando gráficos...")
            
            # Configurar matplotlib para melhor aparência
            plt.style.use('default')
            plt.rcParams['font.size'] = 10
            plt.rcParams['figure.facecolor'] = 'white'
            
            # Atualizar cada gráfico
            self.criar_grafico_vendas_diarias()
            self.criar_grafico_produtos_performance()
            self.criar_grafico_analise_horarios()
            self.criar_grafico_comparacao_mensal()
            
            print("✅ Gráficos atualizados")
            
        except Exception as e:
            print(f"❌ Erro ao atualizar gráficos: {e}")
        
    def criar_grafico_vendas_diarias(self):
        """
        📊 GRÁFICO DE VENDAS DIÁRIAS
        
        Este gráfico mostra a evolução das vendas dos últimos 7 dias.
        Ajuda o dono da lanchonete a entender:
        - Se as vendas estão crescendo ou caindo
        - Quais dias da semana vendem mais
        - Tendências de receita e quantidade
        
        DADOS MOSTRADOS:
        - Linha superior: receita em R$ por dia
        - Linha inferior: quantidade de itens vendidos por dia
        
        COMO FUNCIONA:
        1. Busca dados dos últimos 7 dias no banco
        2. Cria dois gráficos: receita (linha) e quantidade (barras)
        3. Usa matplotlib para criar gráficos bonitos
        4. Integra com tkinter usando FigureCanvasTkAgg
        """
        try:
            print("📊 Criando gráfico de vendas diárias...")
            
            # Limpar aba antes de criar novo gráfico
            for widget in self.tab_vendas.winfo_children():
                widget.destroy()
                
            # Buscar dados dos últimos 7 dias
            dados_vendas = self.db.obter_vendas_ultimos_dias(7)
            
            if not dados_vendas:
                # Se não há dados, mostrar mensagem explicativa
                no_data_frame = ttk.Frame(self.tab_vendas)
                no_data_frame.pack(expand=True, fill=tk.BOTH)
                
                ttk.Label(
                    no_data_frame, 
                    text="📈 Nenhuma venda registrada ainda",
                    font=("Arial", 14, "bold")
                ).pack(pady=50)
                
                ttk.Label(
                    no_data_frame,
                    text="Este gráfico aparecerá quando houver vendas registradas.\nComece registrando algumas vendas no sistema!",
                    font=("Arial", 11),
                    justify=tk.CENTER
                ).pack()
                return
                
            # Preparar dados para o gráfico
            datas = [item[0] for item in dados_vendas]  # DD/MM/YYYY
            receitas = [float(item[1]) for item in dados_vendas]  # Valores em R$
            quantidades = [int(item[2]) for item in dados_vendas]  # Número de itens
            
            # Criar figura com dois subgráficos (tamanho otimizado)
            fig = Figure(figsize=(13, 7), facecolor='white')
            
            # === GRÁFICO 1: RECEITA DIÁRIA (LINHA) ===
            ax1 = fig.add_subplot(2, 1, 1)
            linha_receita = ax1.plot(
                datas, receitas, 
                marker='o', 
                linewidth=3, 
                markersize=8,
                color=self.cores['receita'],
                markerfacecolor='white',
                markeredgewidth=2
            )
            
            ax1.set_title('💰 Receita Diária (Últimos 7 Dias)', fontsize=14, fontweight='bold', pad=20)
            ax1.set_ylabel('Receita (R$)', fontsize=12)
            ax1.grid(True, alpha=0.3, linestyle='--')
            ax1.set_facecolor('#f8f9fa')
            
            # Adicionar valores nos pontos
            for i, (data, receita) in enumerate(zip(datas, receitas)):
                ax1.annotate(
                    f'R$ {receita:.0f}', 
                    (i, receita),
                    textcoords="offset points",
                    xytext=(0,10),
                    ha='center',
                    fontsize=9,
                    fontweight='bold'
                )
            
            # === GRÁFICO 2: QUANTIDADE VENDIDA (BARRAS) ===
            ax2 = fig.add_subplot(2, 1, 2)
            barras = ax2.bar(
                datas, quantidades, 
                color=self.cores['vendas'], 
                alpha=0.8,
                edgecolor='white',
                linewidth=2
            )
            
            ax2.set_title('🛒 Quantidade Vendida por Dia', fontsize=14, fontweight='bold', pad=20)
            ax2.set_ylabel('Unidades Vendidas', fontsize=12)
            ax2.set_xlabel('Data', fontsize=12)
            ax2.grid(True, alpha=0.3, linestyle='--')
            ax2.set_facecolor('#f8f9fa')
            
            # Adicionar valores nas barras
            for i, (barra, quantidade) in enumerate(zip(barras, quantidades)):
                altura = barra.get_height()
                ax2.text(
                    barra.get_x() + barra.get_width()/2., 
                    altura + 0.5,
                    f'{int(quantidade)}',
                    ha='center', 
                    va='bottom',
                    fontsize=10,
                    fontweight='bold'
                )
            
            # Melhorar formatação dos eixos
            for ax in [ax1, ax2]:
                ax.tick_params(axis='x', rotation=45)
                for spine in ax.spines.values():
                    spine.set_linewidth(0.5)
            
            # Ajustar layout
            fig.tight_layout(pad=3.0)
            
            # Adicionar ao tkinter
            canvas = FigureCanvasTkAgg(fig, self.tab_vendas)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            print("✅ Gráfico de vendas diárias criado")
            
        except Exception as e:
            print(f"❌ Erro ao criar gráfico de vendas: {e}")
            # Mostrar erro na interface
            error_frame = ttk.Frame(self.tab_vendas)
            error_frame.pack(expand=True, fill=tk.BOTH)
            
            ttk.Label(
                error_frame, 
                text="❌ Erro ao carregar gráfico de vendas",
                font=("Arial", 12, "bold")
            ).pack(pady=20)
            
            ttk.Label(
                error_frame,
                text=f"Detalhes: {str(e)}",
                font=("Arial", 10)
            ).pack()
            
    def criar_grafico_produtos_performance(self):
        """
        🏆 GRÁFICO DE PERFORMANCE DOS PRODUTOS
        
        Este gráfico mostra quais produtos estão vendendo mais.
        Ajuda o dono da lanchonete a:
        - Identificar produtos campeões de venda
        - Focar no que o cliente mais gosta
        - Decidir quais produtos promover
        - Planejar compras de estoque
        
        DADOS MOSTRADOS:
        - Lado esquerdo: receita por produto (em R$)
        - Lado direito: quantidade vendida por produto
        
        EXPLICAÇÃO TÉCNICA:
        1. Busca top 10 produtos por receita total
        2. Cria gráficos de barras horizontais
        3. Mostra valores nas barras para fácil leitura
        4. Usa cores diferentes para receita vs quantidade
        """
        try:
            print("🏆 Criando gráfico de performance dos produtos...")
            
            # Limpar aba
            for widget in self.tab_produtos.winfo_children():
                widget.destroy()
                
            # Buscar top 10 produtos por receita
            produtos_performance = self.db.obter_top_produtos_receita(10)
            
            if not produtos_performance:
                # Se não há dados, mostrar mensagem
                no_data_frame = ttk.Frame(self.tab_produtos)
                no_data_frame.pack(expand=True, fill=tk.BOTH)
                
                ttk.Label(
                    no_data_frame, 
                    text="🏆 Nenhum produto vendido ainda",
                    font=("Arial", 14, "bold")
                ).pack(pady=50)
                
                ttk.Label(
                    no_data_frame,
                    text="Registre algumas vendas para ver\nquais produtos são os campeões!",
                    font=("Arial", 11),
                    justify=tk.CENTER
                ).pack()
                return
                
            # Preparar dados
            produtos = [item[0] for item in produtos_performance]
            receitas = [float(item[1]) for item in produtos_performance]
            quantidades = [int(item[2]) for item in produtos_performance]
            
            # Limitar nome dos produtos para caber no gráfico
            produtos_formatados = []
            for produto in produtos:
                if len(produto) > 20:
                    produtos_formatados.append(produto[:17] + "...")
                else:
                    produtos_formatados.append(produto)
            
            # Criar figura (produtos performance)
            fig = Figure(figsize=(13, 7), facecolor='white')
            
            # === GRÁFICO 1: RECEITA POR PRODUTO ===
            ax1 = fig.add_subplot(1, 2, 1)
            bars1 = ax1.barh(
                produtos_formatados, receitas, 
                color=self.cores['receita'],
                alpha=0.8,
                edgecolor='white',
                linewidth=1
            )
            
            ax1.set_title('💰 Top 10 Produtos por Receita', fontsize=14, fontweight='bold', pad=20)
            ax1.set_xlabel('Receita Total (R$)', fontsize=12)
            ax1.grid(True, alpha=0.3, linestyle='--', axis='x')
            ax1.set_facecolor('#f8f9fa')
            
            # Adicionar valores nas barras
            for bar, valor in zip(bars1, receitas):
                largura = bar.get_width()
                ax1.text(
                    largura + max(receitas) * 0.01,  # Pequeno offset
                    bar.get_y() + bar.get_height()/2, 
                    f'R$ {valor:.0f}', 
                    ha='left', 
                    va='center',
                    fontsize=10,
                    fontweight='bold'
                )
            
            # === GRÁFICO 2: QUANTIDADE POR PRODUTO ===
            ax2 = fig.add_subplot(1, 2, 2)
            bars2 = ax2.barh(
                produtos_formatados, quantidades, 
                color=self.cores['vendas'],
                alpha=0.8,
                edgecolor='white',
                linewidth=1
            )
            
            ax2.set_title('🛒 Top 10 Produtos por Quantidade', fontsize=14, fontweight='bold', pad=20)
            ax2.set_xlabel('Unidades Vendidas', fontsize=12)
            ax2.grid(True, alpha=0.3, linestyle='--', axis='x')
            ax2.set_facecolor('#f8f9fa')
            
            # Adicionar valores nas barras
            for bar, valor in zip(bars2, quantidades):
                largura = bar.get_width()
                ax2.text(
                    largura + max(quantidades) * 0.01,  # Pequeno offset
                    bar.get_y() + bar.get_height()/2, 
                    f'{valor:.0f}', 
                    ha='left', 
                    va='center',
                    fontsize=10,
                    fontweight='bold'
                )
            
            # Melhorar formatação
            for ax in [ax1, ax2]:
                ax.tick_params(axis='y', labelsize=9)
                ax.tick_params(axis='x', labelsize=10)
                for spine in ax.spines.values():
                    spine.set_linewidth(0.5)
            
            # Ajustar layout
            fig.tight_layout(pad=3.0)
            
            # Adicionar ao tkinter
            canvas = FigureCanvasTkAgg(fig, self.tab_produtos)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            print("✅ Gráfico de performance de produtos criado")
            
        except Exception as e:
            print(f"❌ Erro ao criar gráfico de produtos: {e}")
            # Mostrar erro na interface
            error_frame = ttk.Frame(self.tab_produtos)
            error_frame.pack(expand=True, fill=tk.BOTH)
            
            ttk.Label(
                error_frame, 
                text="❌ Erro ao carregar gráfico de produtos",
                font=("Arial", 12, "bold")
            ).pack(pady=20)
            
    def criar_grafico_analise_horarios(self):
        """
        🕐 GRÁFICO DE ANÁLISE POR HORÁRIOS
        
        Este gráfico mostra em quais horários a lanchonete vende mais.
        Muito útil para:
        - Descobrir horários de pico de movimento
        - Planejar escalas de funcionários
        - Ajustar horários de funcionamento
        - Preparar estoque nos horários certos
        
        DADOS MOSTRADOS:
        - Receita por hora do dia (0h às 23h)
        - Área preenchida para destacar volumes
        - Pontos marcados para horários de pico
        
        INTERPRETAÇÃO PRÁTICA:
        - Picos = horários para ter mais funcionários
        - Vales = horários para reduzir custos
        - Tendências = padrões de comportamento dos clientes
        """
        try:
            print("🕐 Criando gráfico de análise por horários...")
            
            # Limpar aba
            for widget in self.tab_horarios.winfo_children():
                widget.destroy()
                
            # Buscar vendas por horário
            vendas_horario = self.db.obter_vendas_por_horario()
            
            if not vendas_horario:
                # Se não há dados, mostrar mensagem
                no_data_frame = ttk.Frame(self.tab_horarios)
                no_data_frame.pack(expand=True, fill=tk.BOTH)
                
                ttk.Label(
                    no_data_frame, 
                    text="🕐 Nenhuma venda com horário registrada",
                    font=("Arial", 14, "bold")
                ).pack(pady=50)
                
                ttk.Label(
                    no_data_frame,
                    text="Este gráfico mostrará os horários de pico\nquando houver mais vendas registradas.",
                    font=("Arial", 11),
                    justify=tk.CENTER
                ).pack()
                return
                
            # Preparar dados - criar array completo de 24 horas
            receita_por_hora = [0.0] * 24  # 0h às 23h
            
            # Preencher com dados reais
            for hora, receita in vendas_horario:
                if 0 <= hora <= 23:
                    receita_por_hora[hora] = float(receita)
            
            horarios = list(range(24))  # 0 a 23
            
            # Criar figura (análise horários)
            fig = Figure(figsize=(13, 6), facecolor='white')
            ax = fig.add_subplot(1, 1, 1)
            
            # === GRÁFICO DE ÁREA ===
            linha = ax.plot(
                horarios, receita_por_hora, 
                marker='o', 
                linewidth=4, 
                markersize=6,
                color=self.cores['crescimento'],
                markerfacecolor='white',
                markeredgewidth=2,
                label='Receita por Hora'
            )
            
            # Área preenchida
            ax.fill_between(
                horarios, receita_por_hora, 
                alpha=0.3, 
                color=self.cores['crescimento']
            )
            
            # Destacar horários de pico (se receita > média)
            receita_media = sum(receita_por_hora) / len(receita_por_hora) if receita_por_hora else 0
            for i, receita in enumerate(receita_por_hora):
                if receita > receita_media and receita > 0:
                    ax.plot(i, receita, 'o', markersize=12, color='red', alpha=0.7)
                    ax.annotate(
                        f'PICO\nR$ {receita:.0f}', 
                        (i, receita),
                        textcoords="offset points",
                        xytext=(0,20),
                        ha='center',
                        fontsize=8,
                        fontweight='bold',
                        bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7)
                    )
            
            # Configurações do gráfico
            ax.set_title('🕐 Análise de Vendas por Horário do Dia', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Horário do Dia', fontsize=12)
            ax.set_ylabel('Receita (R$)', fontsize=12)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_facecolor('#f8f9fa')
            
            # Configurar eixo X (horários)
            ax.set_xticks(range(0, 24, 2))  # De 2 em 2 horas
            ax.set_xticklabels([f"{h:02d}h" for h in range(0, 24, 2)])
            
            # Adicionar linha da média
            if receita_media > 0:
                ax.axhline(
                    y=receita_media, 
                    color='orange', 
                    linestyle='--', 
                    alpha=0.8,
                    label=f'Média: R$ {receita_media:.2f}'
                )
            
            # Legenda
            ax.legend(loc='upper right', fontsize=10)
            
            # Melhorar formatação
            ax.tick_params(axis='both', labelsize=10)
            for spine in ax.spines.values():
                spine.set_linewidth(0.5)
            
            # Ajustar layout
            fig.tight_layout(pad=3.0)
            
            # Adicionar ao tkinter
            canvas = FigureCanvasTkAgg(fig, self.tab_horarios)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            print("✅ Gráfico de análise por horários criado")
            
        except Exception as e:
            print(f"❌ Erro ao criar gráfico de horários: {e}")
            # Mostrar erro na interface
            error_frame = ttk.Frame(self.tab_horarios)
            error_frame.pack(expand=True, fill=tk.BOTH)
            
            ttk.Label(
                error_frame, 
                text="❌ Erro ao carregar gráfico de horários",
                font=("Arial", 12, "bold")
            ).pack(pady=20)
    
    def criar_grafico_comparacao_mensal(self):
        """
        📅 GRÁFICO DE EVOLUÇÃO MENSAL
        
        Este gráfico mostra como o negócio está evoluindo ao longo dos meses.
        Fundamental para:
        - Acompanhar crescimento do negócio
        - Identificar sazonalidades
        - Comparar performance entre meses
        - Projetar tendências futuras
        
        DADOS MOSTRADOS:
        - Receita mensal dos últimos 6 meses
        - Linha de tendência
        - Percentual de crescimento
        - Metas e comparações
        
        INTERPRETAÇÃO PARA O NEGÓCIO:
        - Linha ascendente = negócio crescendo
        - Linha descendente = precisa ação corretiva
        - Variações = sazonalidade ou eventos específicos
        """
        try:
            print("📅 Criando gráfico de evolução mensal...")
            
            # Limpar aba
            for widget in self.tab_comparacao.winfo_children():
                widget.destroy()
                
            # Calcular dados dos últimos 6 meses
            dados_mensais = []
            hoje = datetime.now()
            
            for i in range(6):
                # Calcular mês
                mes_atual = hoje.replace(day=1) - timedelta(days=30*i)
                inicio_mes = mes_atual.strftime("%d/%m/%Y")
                
                # Último dia do mês
                if mes_atual.month == 12:
                    fim_mes = mes_atual.replace(year=mes_atual.year + 1, month=1, day=1) - timedelta(days=1)
                else:
                    fim_mes = mes_atual.replace(month=mes_atual.month + 1, day=1) - timedelta(days=1)
                fim_mes_str = fim_mes.strftime("%d/%m/%Y")
                
                # Buscar receita do mês
                receita_mes = self.db.obter_receita_periodo(inicio_mes, fim_mes_str)
                vendas_mes = self.db.contar_vendas_periodo(inicio_mes, fim_mes_str)
                
                dados_mensais.append({
                    'mes': mes_atual.strftime("%m/%Y"),
                    'receita': receita_mes,
                    'vendas': vendas_mes
                })
            
            # Inverter para ordem cronológica
            dados_mensais = dados_mensais[::-1]
            
            if not any(d['receita'] > 0 for d in dados_mensais):
                # Se não há dados, mostrar mensagem
                no_data_frame = ttk.Frame(self.tab_comparacao)
                no_data_frame.pack(expand=True, fill=tk.BOTH)
                
                ttk.Label(
                    no_data_frame, 
                    text="📅 Dados insuficientes para análise mensal",
                    font=("Arial", 14, "bold")
                ).pack(pady=50)
                
                ttk.Label(
                    no_data_frame,
                    text="Este gráfico mostrará a evolução do negócio\nquando houver dados de múltiplos meses.",
                    font=("Arial", 11),
                    justify=tk.CENTER
                ).pack()
                return
                
            # Preparar dados para gráfico
            meses = [d['mes'] for d in dados_mensais]
            receitas = [d['receita'] for d in dados_mensais]
            vendas = [d['vendas'] for d in dados_mensais]
            
            # Criar figura (evolução mensal)
            fig = Figure(figsize=(13, 7), facecolor='white')
            
            # === GRÁFICO 1: RECEITA MENSAL ===
            ax1 = fig.add_subplot(2, 1, 1)
            
            # Gráfico de barras para receita
            bars = ax1.bar(
                meses, receitas, 
                color=self.cores['receita'],
                alpha=0.8,
                edgecolor='white',
                linewidth=2,
                label='Receita Mensal'
            )
            
            # Linha de tendência
            if len(receitas) > 1:
                ax1.plot(
                    meses, receitas, 
                    color='red', 
                    linewidth=3, 
                    marker='o', 
                    markersize=8,
                    label='Tendência'
                )
            
            ax1.set_title('💰 Evolução da Receita Mensal', fontsize=14, fontweight='bold', pad=20)
            ax1.set_ylabel('Receita (R$)', fontsize=12)
            ax1.grid(True, alpha=0.3, linestyle='--')
            ax1.set_facecolor('#f8f9fa')
            ax1.legend()
            
            # Adicionar valores nas barras
            for bar, valor in zip(bars, receitas):
                altura = bar.get_height()
                ax1.text(
                    bar.get_x() + bar.get_width()/2., 
                    altura + max(receitas) * 0.01,
                    f'R$ {valor:.0f}',
                    ha='center', 
                    va='bottom',
                    fontsize=10,
                    fontweight='bold'
                )
            
            # === GRÁFICO 2: NÚMERO DE VENDAS MENSAIS ===
            ax2 = fig.add_subplot(2, 1, 2)
            
            # Gráfico de linha para vendas
            ax2.plot(
                meses, vendas, 
                marker='s', 
                linewidth=4, 
                markersize=8,
                color=self.cores['vendas'],
                markerfacecolor='white',
                markeredgewidth=2,
                label='Vendas Mensais'
            )
            
            # Área preenchida
            ax2.fill_between(
                meses, vendas, 
                alpha=0.3, 
                color=self.cores['vendas']
            )
            
            ax2.set_title('🛒 Evolução do Número de Vendas', fontsize=14, fontweight='bold', pad=20)
            ax2.set_ylabel('Número de Vendas', fontsize=12)
            ax2.set_xlabel('Mês/Ano', fontsize=12)
            ax2.grid(True, alpha=0.3, linestyle='--')
            ax2.set_facecolor('#f8f9fa')
            ax2.legend()
            
            # Adicionar valores nos pontos
            for i, (mes, venda) in enumerate(zip(meses, vendas)):
                ax2.annotate(
                    f'{int(venda)}', 
                    (i, venda),
                    textcoords="offset points",
                    xytext=(0,15),
                    ha='center',
                    fontsize=10,
                    fontweight='bold'
                )
            
            # Calcular e mostrar crescimento
            if len(receitas) >= 2:
                crescimento = ((receitas[-1] - receitas[-2]) / receitas[-2]) * 100 if receitas[-2] > 0 else 0
                cor_crescimento = 'green' if crescimento >= 0 else 'red'
                sinal = '+' if crescimento >= 0 else ''
                
                # Adicionar texto de crescimento
                fig.suptitle(
                    f'Crescimento último mês: {sinal}{crescimento:.1f}%',
                    fontsize=12,
                    color=cor_crescimento,
                    y=0.02
                )
            
            # Melhorar formatação
            for ax in [ax1, ax2]:
                ax.tick_params(axis='x', rotation=45, labelsize=10)
                ax.tick_params(axis='y', labelsize=10)
                for spine in ax.spines.values():
                    spine.set_linewidth(0.5)
            
            # Ajustar layout
            fig.tight_layout(pad=3.0)
            
            # Adicionar ao tkinter
            canvas = FigureCanvasTkAgg(fig, self.tab_comparacao)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            print("✅ Gráfico de evolução mensal criado")
            
        except Exception as e:
            print(f"❌ Erro ao criar gráfico mensal: {e}")
            # Mostrar erro na interface
            error_frame = ttk.Frame(self.tab_comparacao)
            error_frame.pack(expand=True, fill=tk.BOTH)
            
            ttk.Label(
                error_frame, 
                text="❌ Erro ao carregar gráfico mensal",
                font=("Arial", 12, "bold")
            ).pack(pady=20)
    
    def mostrar_ajuda(self):
        """
        ❓ JANELA DE AJUDA PARA O USUÁRIO
        
        Cria uma janela com explicações detalhadas sobre como usar
        o dashboard e interpretar os dados mostrados.
        
        CONTEÚDO DA AJUDA:
        1. Como navegar no dashboard
        2. O que cada métrica significa
        3. Como interpretar os gráficos
        4. Dicas para usar as informações no negócio
        """
        ajuda_window = tk.Toplevel(self.window)
        ajuda_window.title("💡 Como Usar o Dashboard")
        ajuda_window.geometry("800x600")
        centralizar_janela(ajuda_window)
        
        # Criar scrollable text
        frame_main = ttk.Frame(ajuda_window)
        frame_main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        ttk.Label(
            frame_main,
            text="💡 Guia Completo do Dashboard Financeiro",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))
        
        # Texto de ajuda
        ajuda_text = tk.Text(
            frame_main,
            wrap=tk.WORD,
            font=("Arial", 11),
            padx=10,
            pady=10
        )
        ajuda_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(ajuda_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        ajuda_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=ajuda_text.yview)
        
        conteudo_ajuda = """
📊 DASHBOARD FINANCEIRO - GUIA COMPLETO

Este dashboard foi criado para ajudar você a entender e controlar sua lanchonete de forma profissional.

═══════════════════════════════════════════════════════════════════

📋 MÉTRICAS PRINCIPAIS

💰 Receita Hoje: Quanto dinheiro você faturou hoje
🛒 Vendas Hoje: Quantas vendas foram feitas hoje  
🏆 Produto Top: Qual produto está vendendo mais hoje
🎯 Ticket Médio: Valor médio de cada venda (receita ÷ vendas)
📦 Valor Estoque: Quanto vale todo seu estoque atual
⚠️ Estoque Baixo: Quantos produtos estão acabando (menos de 5 unidades)
📅 Receita Mês: Total faturado no mês atual
📈 Crescimento: Comparação com a semana passada

═══════════════════════════════════════════════════════════════════

📈 GRÁFICOS E ANÁLISES

📊 VENDAS DIÁRIAS
- Mostra receita e quantidade dos últimos 7 dias
- Use para: identificar dias da semana que vendem mais
- Dica: se um dia vende menos, faça promoções especiais

🏆 TOP PRODUTOS  
- Ranking dos produtos que mais vendem
- Use para: focar nos produtos que o cliente mais gosta
- Dica: mantenha sempre em estoque os produtos do topo

🕐 HORÁRIOS DE PICO
- Mostra quais horários vendem mais
- Use para: escalar funcionários nos horários certos
- Dica: prepare mais estoque antes dos horários de pico

📅 EVOLUÇÃO MENSAL
- Compara receita dos últimos meses
- Use para: acompanhar crescimento do negócio
- Dica: linha subindo = negócio crescendo, linha descendo = revisar estratégia

═══════════════════════════════════════════════════════════════════

🚨 ALERTAS E O QUE FAZER

⚠️ Estoque Baixo: Compre mais produtos antes que acabem
📢 Sem Vendas: Verifique se está registrando as vendas no sistema
🎉 Muitas Vendas: Ótimo! Continue fazendo o que está dando certo
💰 Boa Receita: Dia produtivo, mantenha o padrão
🔥 Produto em Alta: Produto vendendo muito, não deixe faltar

═══════════════════════════════════════════════════════════════════

💡 DICAS PARA USAR NO SEU NEGÓCIO

1. HORÁRIOS DE PICO
   - Tenha mais funcionários nos horários que mais vendem
   - Prepare ingredientes antes dos picos
   - Evite fazer limpeza pesada nos horários de movimento

2. PRODUTOS CAMPEÕES
   - Sempre tenha em estoque os produtos do top 10
   - Considere aumentar a margem dos produtos que vendem muito
   - Use os campeões para atrair clientes (combos, promoções)

3. DIAS DA SEMANA
   - Faça promoções nos dias que vendem menos
   - Programe limpeza e manutenção nos dias mais fracos
   - Ajuste compras baseado no padrão semanal

4. CRESCIMENTO MENSAL
   - Se crescendo: continue a estratégia atual
   - Se estável: teste novas promoções ou produtos
   - Se caindo: revisar preços, qualidade, atendimento

5. TICKET MÉDIO
   - Se baixo: ofereça combos e adicionais
   - Se alto: mantenha a qualidade que justifica o preço
   - Meta: sempre buscar aumentar sem perder clientes

═══════════════════════════════════════════════════════════════════

🔄 ATUALIZANDO OS DADOS

• Clique em "🔄 Atualizar Dados" para buscar informações mais recentes
• O dashboard mostra a última atualização no canto superior direito
• Dados são calculados em tempo real a partir das vendas registradas
• Para dados precisos, sempre registre vendas no momento que acontecem

═══════════════════════════════════════════════════════════════════

❓ DÚVIDAS FREQUENTES

P: Por que alguns gráficos estão vazios?
R: Precisa ter vendas registradas no sistema. Comece registrando vendas!

P: Os valores estão corretos?
R: Os valores vêm das vendas registradas. Sempre registre preço e quantidade.

P: Como interpretar o crescimento?
R: + significa crescendo, - significa diminuindo comparado à semana passada.

P: O que fazer se estoque baixo?
R: Comprar mais produtos antes que acabem e percam vendas.

P: Como usar o horário de pico?
R: Tenha mais funcionários e estoque preparado nesses horários.

═══════════════════════════════════════════════════════════════════

🎯 LEMBRE-SE

Este dashboard é sua ferramenta de gestão profissional. Use os dados para:
✓ Tomar decisões baseadas em fatos, não intuição
✓ Identificar oportunidades de crescimento  
✓ Evitar problemas antes que aconteçam
✓ Maximizar seus lucros de forma inteligente

Sucesso no seu negócio! 🚀
        """
        
        ajuda_text.insert(1.0, conteudo_ajuda)
        ajuda_text.config(state=tk.DISABLED)  # Read-only
        
        # Botão fechar
        ttk.Button(
            frame_main,
            text="Fechar",
            command=ajuda_window.destroy
        ).pack(pady=(10, 0))
    
    def exportar_relatorio(self):
        """
        📄 EXPORTAÇÃO DE RELATÓRIO COMPLETO
        
        Gera um arquivo Excel com todos os dados do dashboard
        para análise offline ou envio para contador/sócios.
        
        CONTEÚDO DO RELATÓRIO:
        1. Resumo executivo com métricas principais
        2. Dados de vendas detalhados
        3. Análise de produtos
        4. Estatísticas por período
        
        ARQUIVO GERADO:
        - Formato Excel (.xlsx)
        - Múltiplas abas organizadas
        - Dados formatados e legíveis
        - Salvo na pasta 'data/relatorios/'
        """
        try:
            print("📄 Gerando relatório completo...")
            
            # Importar pandas para exportação
            import pandas as pd
            from datetime import datetime
            import os
            
            # Criar pasta de relatórios se não existir
            os.makedirs("data/relatorios", exist_ok=True)
            
            # Nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/relatorios/dashboard_relatorio_{timestamp}.xlsx"
            
            # Criar writer do Excel
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                
                # === ABA 1: RESUMO EXECUTIVO ===
                hoje = datetime.now().strftime("%d/%m/%Y")
                receita_hoje = self.db.obter_receita_periodo(hoje, hoje)
                vendas_hoje = self.db.contar_vendas_periodo(hoje, hoje)
                produto_top = self.db.obter_produto_mais_vendido()
                estoque_total = self.db.obter_valor_total_estoque()
                produtos_baixo = self.db.contar_produtos_estoque_baixo(5)
                
                resumo_data = {
                    'Métrica': [
                        'Receita Hoje', 'Vendas Hoje', 'Produto Mais Vendido',
                        'Ticket Médio', 'Valor Estoque Total', 'Produtos Estoque Baixo'
                    ],
                    'Valor': [
                        f'R$ {receita_hoje:.2f}',
                        vendas_hoje,
                        produto_top,
                        f'R$ {(receita_hoje/vendas_hoje if vendas_hoje > 0 else 0):.2f}',
                        f'R$ {estoque_total:.2f}',
                        produtos_baixo
                    ]
                }
                
                df_resumo = pd.DataFrame(resumo_data)
                df_resumo.to_excel(writer, sheet_name='Resumo Executivo', index=False)
                
                # === ABA 2: VENDAS DOS ÚLTIMOS 7 DIAS ===
                dados_vendas = self.db.obter_vendas_ultimos_dias(7)
                if dados_vendas:
                    df_vendas = pd.DataFrame(dados_vendas, columns=['Data', 'Receita', 'Quantidade'])
                    df_vendas.to_excel(writer, sheet_name='Vendas 7 Dias', index=False)
                
                # === ABA 3: TOP PRODUTOS ===
                produtos_performance = self.db.obter_top_produtos_receita(20)
                if produtos_performance:
                    df_produtos = pd.DataFrame(produtos_performance, columns=['Produto', 'Receita Total', 'Quantidade Total'])
                    df_produtos.to_excel(writer, sheet_name='Top Produtos', index=False)
                
                # === ABA 4: HISTÓRICO COMPLETO ===
                historico_completo = self.db.listar_historico_completo(100)  # Últimas 100 vendas
                if historico_completo:
                    df_historico = pd.DataFrame(
                        historico_completo, 
                        columns=['ID', 'Produto', 'Quantidade', 'Preço Unit.', 'Total', 'Data/Hora', 'Vendedor', 'Obs.']
                    )
                    df_historico.to_excel(writer, sheet_name='Histórico Vendas', index=False)
                
                # === ABA 5: ESTOQUE ATUAL ===
                estoque_completo = self.db.listar_estoque_completo()
                if estoque_completo:
                    df_estoque = pd.DataFrame(
                        estoque_completo,
                        columns=['Produto', 'Quantidade', 'Preço', 'Categoria', 'Código', 'Cadastro', 'Atualização']
                    )
                    df_estoque.to_excel(writer, sheet_name='Estoque Atual', index=False)
            
            # Sucesso
            messagebox.showinfo(
                "Relatório Exportado",
                f"Relatório salvo com sucesso!\n\nArquivo: {filename}\n\n"
                f"O arquivo contém:\n"
                f"• Resumo executivo\n"
                f"• Dados de vendas\n" 
                f"• Performance dos produtos\n"
                f"• Histórico detalhado\n"
                f"• Situação do estoque\n\n"
                f"Use este relatório para análises ou envio ao contador."
            )
            
            print(f"✅ Relatório exportado para: {filename}")
            
        except Exception as e:
            print(f"❌ Erro ao exportar relatório: {e}")
            messagebox.showerror(
                "Erro na Exportação", 
                f"Não foi possível gerar o relatório.\n\nErro: {str(e)}\n\n"
                f"Verifique se você tem permissão para escrever na pasta 'data/relatorios/'."
            )
            
    def exportar_relatorio(self):
        """Exporta relatório executivo"""
        try:
            from src.relatorios.relatorio_executivo import RelatorioExecutivo
            relatorio = RelatorioExecutivo()
            arquivo = relatorio.gerar_relatorio_completo()
            
            if arquivo:
                messagebox.showinfo(
                    "Sucesso", 
                    f"Relatório executivo exportado:\n{arquivo}"
                )
            else:
                messagebox.showerror("Erro", "Falha ao exportar relatório")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")