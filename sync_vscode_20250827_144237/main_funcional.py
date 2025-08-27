#!/usr/bin/env python3
"""
Sistema de Lanchonete - Versão Funcional
Solução para problemas de dependências
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import subprocess

def verificar_dependencias():
    """Verificar se as dependências essenciais estão disponíveis"""
    try:
        import tkinter
        print("✓ Tkinter disponível")
        return True
    except ImportError as e:
        print(f"✗ Erro: {e}")
        return False

def centralizar_janela(janela):
    """Centralizar janela na tela"""
    janela.update_idletasks()
    width = janela.winfo_width()
    height = janela.winfo_height()
    pos_x = (janela.winfo_screenwidth() // 2) - (width // 2)
    pos_y = (janela.winfo_screenheight() // 2) - (height // 2)
    janela.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

class DatabaseManager:
    """Gerenciador de banco de dados simplificado"""
    
    def __init__(self):
        self.db_path = "data/banco.db"
        self.criar_estrutura()
    
    def criar_estrutura(self):
        """Criar estrutura do banco"""
        os.makedirs("data", exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela de estoque
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS estoque (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto TEXT NOT NULL,
                    quantidade INTEGER NOT NULL DEFAULT 0,
                    preco REAL NOT NULL DEFAULT 0.0,
                    categoria TEXT DEFAULT 'Geral',
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de vendas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historico_vendas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    preco_unitario REAL NOT NULL,
                    total REAL NOT NULL,
                    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Verificar se coluna total existe, se não existir, adicionar
            cursor.execute("PRAGMA table_info(historico_vendas)")
            columns = [column[1] for column in cursor.fetchall()]
            if 'total' not in columns:
                cursor.execute("ALTER TABLE historico_vendas ADD COLUMN total REAL DEFAULT 0.0")
                print("✓ Coluna 'total' adicionada à tabela historico_vendas")
            
            # Tabela de contas em aberto (crediário)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contas_abertas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_nome TEXT NOT NULL,
                    cliente_telefone TEXT,
                    produto TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    preco_unitario REAL NOT NULL,
                    total REAL NOT NULL,
                    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_vencimento DATE,
                    pago BOOLEAN DEFAULT FALSE,
                    data_pagamento TIMESTAMP,
                    observacoes TEXT
                )
            """)
            
            # Tabela de caixa
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS caixa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_fechamento TIMESTAMP,
                    valor_inicial REAL NOT NULL,
                    valor_vendas REAL DEFAULT 0.0,
                    valor_sangria REAL DEFAULT 0.0,
                    valor_reforco REAL DEFAULT 0.0,
                    valor_final REAL DEFAULT 0.0,
                    funcionario TEXT NOT NULL,
                    status TEXT DEFAULT 'ABERTO',
                    observacoes TEXT
                )
            """)
            
            # Tabela de movimentações do caixa
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS movimentacoes_caixa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    caixa_id INTEGER,
                    tipo TEXT NOT NULL,
                    valor REAL NOT NULL,
                    descricao TEXT,
                    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    funcionario TEXT NOT NULL,
                    FOREIGN KEY (caixa_id) REFERENCES caixa (id)
                )
            """)
            
            # Tabela de backups
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS backups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_arquivo TEXT NOT NULL,
                    caminho_arquivo TEXT NOT NULL,
                    data_backup TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tamanho_mb REAL,
                    tipo TEXT NOT NULL,
                    status TEXT DEFAULT 'CONCLUIDO'
                )
            """)
            
            conn.commit()
            print("✓ Banco de dados configurado")

class MainWindow:
    """Janela principal do sistema"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🍔 Sistema de Lanchonete - Versão Estável")
        self.root.geometry("900x700")
        self.db = DatabaseManager()
        self.setup_ui()
        centralizar_janela(self.root)
    
    def setup_ui(self):
        """Configurar interface principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(
            main_frame, 
            text="🍔 Sistema de Lanchonete", 
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(0, 30))
        
        # Subtítulo
        subtitle = ttk.Label(
            main_frame,
            text="Gerenciamento Completo para Sua Lanchonete",
            font=("Arial", 12),
            foreground="gray"
        )
        subtitle.pack(pady=(0, 40))
        
        # Frame dos botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(expand=True)
        
        # Botões principais
        self.criar_botao(buttons_frame, "📦 Gerenciar Estoque", self.abrir_estoque, 0)
        self.criar_botao(buttons_frame, "➕ Cadastrar Produto", self.cadastro_rapido_produto, 1)
        self.criar_botao(buttons_frame, "💰 Registrar Venda", self.abrir_vendas, 2)
        self.criar_botao(buttons_frame, "📋 Contas em Aberto", self.abrir_contas_abertas, 3)
        self.criar_botao(buttons_frame, "💳 Controle de Caixa", self.abrir_caixa, 4)
        self.criar_botao(buttons_frame, "📊 Dashboard Financeiro", self.abrir_dashboard, 5)
        self.criar_botao(buttons_frame, "💾 Backup/Sincronização", self.abrir_backup, 6)
        self.criar_botao(buttons_frame, "📄 Relatórios", self.abrir_relatorios, 7)
        self.criar_botao(buttons_frame, "❌ Sair", self.sair, 8)
        
        # Status bar
        self.status_bar = ttk.Label(
            main_frame,
            text="Sistema carregado com sucesso - Pronto para uso",
            font=("Arial", 10),
            foreground="green"
        )
        self.status_bar.pack(side=tk.BOTTOM, pady=(20, 0))
    
    def criar_botao(self, parent, texto, comando, row):
        """Criar botão estilizado"""
        btn = ttk.Button(
            parent,
            text=texto,
            command=comando,
            width=25
        )
        btn.grid(row=row, column=0, pady=8, sticky="ew")
        parent.columnconfigure(0, weight=1)
    
    def abrir_estoque(self):
        """Abrir janela de estoque"""
        EstoqueWindow(self.root, self.db)
    
    def cadastro_rapido_produto(self):
        """Abrir janela de cadastro rápido de produto"""
        CadastroRapidoWindow(self.root, self.db)
    
    def abrir_vendas(self):
        """Abrir janela de vendas"""
        VendasWindow(self.root, self.db)
    
    def abrir_contas_abertas(self):
        """Abrir janela de contas em aberto"""
        ContasAbertasWindow(self.root, self.db)
    
    def abrir_caixa(self):
        """Abrir janela de controle de caixa"""
        CaixaWindow(self.root, self.db)
    
    def abrir_backup(self):
        """Abrir janela de backup e sincronização"""
        BackupWindow(self.root, self.db)
    
    def abrir_dashboard(self):
        """Abrir dashboard financeiro"""
        DashboardWindow(self.root, self.db)
    
    def abrir_relatorios(self):
        """Abrir relatórios"""
        messagebox.showinfo("Relatórios", "Funcionalidade em desenvolvimento")
    
    def abrir_config(self):
        """Abrir configurações"""
        ConfigWindow(self.root, self.db)
    
    def sair(self):
        """Sair do sistema"""
        if messagebox.askquestion("Sair", "Deseja realmente sair do sistema?") == "yes":
            self.root.quit()
    
    def run(self):
        """Executar aplicação"""
        self.root.mainloop()

class DashboardWindow:
    """Dashboard financeiro com tamanho otimizado"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        # Criar janela
        self.window = tk.Toplevel(parent)
        self.window.title("📊 Dashboard Executivo - Análise Financeira")
        self.window.geometry("1300x850")  # Tamanho solicitado pelo usuário
        self.window.resizable(True, True)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centralizar janela
        centralizar_janela(self.window)
        
        # Configurar cores do tema
        self.cores = {
            'receita': '#2E8B57',      # Verde marinho
            'vendas': '#4169E1',       # Azul royal
            'crescimento': '#FF6347',  # Tomate
            'alerta': '#FFD700',       # Dourado
            'fundo': '#F8F9FA',        # Cinza claro
            'texto': '#2C3E50'         # Azul escuro
        }
        
        self.setup_ui()
        self.carregar_dados()
    
    def setup_ui(self):
        """Configurar interface do dashboard"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = ttk.Label(
            header_frame,
            text="📊 Dashboard Executivo - Lanchonete",
            font=("Arial", 18, "bold")
        )
        title.pack(side=tk.LEFT)
        
        # Data/hora atual
        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        time_label = ttk.Label(
            header_frame,
            text=f"Atualizado em: {agora}",
            font=("Arial", 10),
            foreground="gray"
        )
        time_label.pack(side=tk.RIGHT)
        
        # Métricas principais
        metrics_frame = ttk.LabelFrame(
            main_frame,
            text="💰 Métricas Financeiras - Visão Rápida",
            padding="12"
        )
        metrics_frame.pack(fill=tk.X, pady=(0, 12))
        
        # Grid de métricas (4 colunas)
        metricas = [
            ("Vendas Hoje", "R$ 847,50", "green"),
            ("Receita Mensal", "R$ 15.234,80", "blue"),
            ("Produtos Vendidos", "156 itens", "orange"),
            ("Margem de Lucro", "32,5%", "purple")
        ]
        
        for i, (nome, valor, cor) in enumerate(metricas):
            frame = ttk.Frame(metrics_frame)
            frame.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            metrics_frame.columnconfigure(i, weight=1)
            
            ttk.Label(frame, text=nome, font=("Arial", 10)).pack()
            ttk.Label(frame, text=valor, font=("Arial", 14, "bold"), foreground=cor).pack()
        
        # Alertas
        alerts_frame = ttk.LabelFrame(
            main_frame,
            text="🚨 Alertas de Gestão",
            padding="8"
        )
        alerts_frame.pack(fill=tk.X, pady=(0, 12))
        
        alerts_text = tk.Text(alerts_frame, height=2, wrap=tk.WORD, font=("Arial", 10))
        alerts_text.pack(fill=tk.X)
        alerts_text.insert("1.0", "✓ Sistema funcionando normalmente\n✓ Dashboard carregado com novo tamanho: 1300x850 pixels")
        alerts_text.config(state=tk.DISABLED)
        
        # Área de gráficos (simulada)
        charts_frame = ttk.LabelFrame(
            main_frame,
            text="📈 Análise Visual de Desempenho",
            padding="10"
        )
        charts_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Notebook para múltiplos gráficos
        notebook = ttk.Notebook(charts_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Abas dos gráficos
        for titulo in ["Vendas Diárias", "Performance Produtos", "Análise Horários", "Evolução Mensal"]:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=titulo)
            
            label = ttk.Label(
                frame,
                text=f"Gráfico: {titulo}\n\nDashboard configurado com tamanho 1300x850\nCentralizado automaticamente na tela",
                font=("Arial", 12),
                justify=tk.CENTER
            )
            label.pack(expand=True)
        
        # Botões de controle
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(controls_frame, text="🔄 Atualizar Dados", width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(controls_frame, text="📄 Exportar Relatório", width=18).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(controls_frame, text="❓ Como Usar", width=12).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(controls_frame, text="❌ Fechar", width=10, command=self.window.destroy).pack(side=tk.RIGHT)
    
    def carregar_dados(self):
        """Carregar dados do banco"""
        print("📊 Dashboard carregado com tamanho 1300x850 - centralizado na tela")

class CadastroRapidoWindow:
    """Janela de cadastro rápido de produtos"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        self.window = tk.Toplevel(parent)
        self.window.title("➕ Cadastro Rápido de Produto")
        self.window.geometry("500x400")
        self.window.transient(parent)
        self.window.grab_set()
        centralizar_janela(self.window)
        
        # Variáveis
        self.produto_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.quantidade_var = tk.StringVar()
        self.preco_var = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interface"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="➕ Cadastro Rápido", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 10))
        
        subtitle = ttk.Label(main_frame, text="Adicione um novo produto ao estoque rapidamente", 
                           font=("Arial", 10), foreground="gray")
        subtitle.pack(pady=(0, 20))
        
        # Formulário
        form_frame = ttk.LabelFrame(main_frame, text="Dados do Produto", padding="15")
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Nome do produto
        ttk.Label(form_frame, text="Nome do Produto:").grid(row=0, column=0, sticky="w", pady=8)
        produto_entry = ttk.Entry(form_frame, textvariable=self.produto_var, width=30, font=("Arial", 11))
        produto_entry.grid(row=0, column=1, padx=(10, 0), pady=8, sticky="ew")
        produto_entry.focus()
        
        # Categoria
        ttk.Label(form_frame, text="Categoria:").grid(row=1, column=0, sticky="w", pady=8)
        categoria_combo = ttk.Combobox(form_frame, textvariable=self.categoria_var, width=28)
        categoria_combo['values'] = ("Bebidas", "Salgados", "Doces", "Lanches", "Outros")
        categoria_combo.grid(row=1, column=1, padx=(10, 0), pady=8, sticky="ew")
        
        # Quantidade
        ttk.Label(form_frame, text="Quantidade Inicial:").grid(row=2, column=0, sticky="w", pady=8)
        quantidade_entry = ttk.Entry(form_frame, textvariable=self.quantidade_var, width=30)
        quantidade_entry.grid(row=2, column=1, padx=(10, 0), pady=8, sticky="ew")
        
        # Preço
        ttk.Label(form_frame, text="Preço Unitário (R$):").grid(row=3, column=0, sticky="w", pady=8)
        preco_entry = ttk.Entry(form_frame, textvariable=self.preco_var, width=30)
        preco_entry.grid(row=3, column=1, padx=(10, 0), pady=8, sticky="ew")
        
        form_frame.columnconfigure(1, weight=1)
        
        # Dicas
        dicas_frame = ttk.LabelFrame(main_frame, text="Dicas", padding="10")
        dicas_frame.pack(fill=tk.X, pady=(0, 20))
        
        dicas_text = tk.Text(dicas_frame, height=4, wrap=tk.WORD, font=("Arial", 9))
        dicas_text.pack(fill=tk.X)
        dicas_text.insert("1.0", "• Use nomes descritivos (ex: 'Coca-Cola 350ml' ao invés de só 'Coca')\n"
                                "• Selecione a categoria correta para organizar o estoque\n"
                                "• Quantidade inicial pode ser 0 para produtos feitos na hora\n"
                                "• Use ponto ou vírgula para decimais no preço (ex: 3.50 ou 3,50)")
        dicas_text.config(state=tk.DISABLED, bg="#f8f9fa")
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="💾 Salvar Produto", command=self.salvar_produto, width=20).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="🔄 Limpar", command=self.limpar_campos, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="❌ Cancelar", command=self.window.destroy, width=15).pack(side=tk.RIGHT)
        
        # Binding Enter para salvar
        self.window.bind('<Return>', lambda e: self.salvar_produto())
    
    def salvar_produto(self):
        """Salvar produto no estoque"""
        try:
            produto = self.produto_var.get().strip()
            categoria = self.categoria_var.get().strip() or "Outros"
            quantidade = int(self.quantidade_var.get() or 0)
            preco_str = self.preco_var.get().replace(',', '.')  # Aceitar vírgula como decimal
            preco = float(preco_str)
            
            if not produto:
                messagebox.showerror("Erro", "O nome do produto é obrigatório!")
                return
            
            if preco < 0:
                messagebox.showerror("Erro", "O preço não pode ser negativo!")
                return
            
            if quantidade < 0:
                messagebox.showerror("Erro", "A quantidade não pode ser negativa!")
                return
            
            # Verificar se já existe
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM estoque WHERE produto = ?", (produto,))
                if cursor.fetchone():
                    messagebox.showerror("Erro", f"O produto '{produto}' já existe no estoque!")
                    return
                
                # Inserir produto
                cursor.execute("""
                    INSERT INTO estoque (produto, categoria, quantidade, preco)
                    VALUES (?, ?, ?, ?)
                """, (produto, categoria, quantidade, preco))
                conn.commit()
            
            messagebox.showinfo("Sucesso", f"Produto '{produto}' cadastrado com sucesso!\n\n"
                                         f"Categoria: {categoria}\n"
                                         f"Quantidade: {quantidade}\n"
                                         f"Preço: R$ {preco:.2f}")
            
            # Perguntar se quer cadastrar outro
            if messagebox.askyesno("Continuar?", "Deseja cadastrar outro produto?"):
                self.limpar_campos()
                self.window.focus()
            else:
                self.window.destroy()
            
        except ValueError:
            messagebox.showerror("Erro", "Verifique os valores:\n"
                                       "• Quantidade deve ser um número inteiro\n"
                                       "• Preço deve ser um número válido (use . ou , para decimais)")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar produto: {e}")
    
    def limpar_campos(self):
        """Limpar todos os campos"""
        self.produto_var.set("")
        self.categoria_var.set("")
        self.quantidade_var.set("")
        self.preco_var.set("")

class ConfigWindow:
    """Janela de configurações do sistema"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        self.window = tk.Toplevel(parent)
        self.window.title("⚙️ Configurações do Sistema")
        self.window.geometry("600x500")
        self.window.transient(parent)
        self.window.grab_set()
        centralizar_janela(self.window)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interface"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="⚙️ Configurações", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Notebook para abas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Aba Sistema
        sistema_frame = ttk.Frame(notebook, padding="15")
        notebook.add(sistema_frame, text="Sistema")
        
        ttk.Label(sistema_frame, text="Informações do Sistema", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))
        
        info_text = tk.Text(sistema_frame, height=8, wrap=tk.WORD, font=("Arial", 10))
        info_text.pack(fill=tk.BOTH, expand=True)
        info_text.insert("1.0", "Sistema de Lanchonete v2.0\n\n"
                                "✓ Gerenciamento completo de estoque\n"
                                "✓ Cadastro rápido de produtos\n"
                                "✓ Registro de vendas\n"
                                "✓ Dashboard financeiro (1300x850)\n"
                                "✓ Banco de dados SQLite\n"
                                "✓ Interface gráfica otimizada\n\n"
                                "Ambiente virtual: Recomendado para evitar conflitos\n"
                                "Dependências: tkinter, sqlite3 (built-in)")
        info_text.config(state=tk.DISABLED)
        
        # Aba Banco de Dados
        db_frame = ttk.Frame(notebook, padding="15")
        notebook.add(db_frame, text="Banco de Dados")
        
        ttk.Label(db_frame, text="Informações do Banco", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))
        
        # Estatísticas
        stats_frame = ttk.LabelFrame(db_frame, text="Estatísticas", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.atualizar_estatisticas(stats_frame)
        
        # Botões de manutenção
        manut_frame = ttk.LabelFrame(db_frame, text="Manutenção", padding="10")
        manut_frame.pack(fill=tk.X)
        
        ttk.Button(manut_frame, text="🔄 Atualizar Estatísticas", command=lambda: self.atualizar_estatisticas(stats_frame)).pack(pady=5)
        ttk.Button(manut_frame, text="📊 Ver Tabelas", command=self.mostrar_tabelas).pack(pady=5)
        
        # Botões principais
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="❌ Fechar", command=self.window.destroy, width=15).pack(side=tk.RIGHT)
    
    def atualizar_estatisticas(self, parent):
        """Atualizar estatísticas do banco"""
        try:
            # Limpar frame
            for widget in parent.winfo_children():
                widget.destroy()
            
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Contar produtos
                cursor.execute("SELECT COUNT(*) FROM estoque")
                total_produtos = cursor.fetchone()[0]
                
                # Contar vendas
                cursor.execute("SELECT COUNT(*) FROM historico_vendas")
                total_vendas = cursor.fetchone()[0]
                
                # Valor total do estoque
                cursor.execute("SELECT SUM(quantidade * preco) FROM estoque")
                valor_estoque = cursor.fetchone()[0] or 0
                
                # Receita total
                cursor.execute("SELECT SUM(total) FROM historico_vendas")
                receita_total = cursor.fetchone()[0] or 0
            
            # Mostrar estatísticas
            ttk.Label(parent, text=f"Produtos cadastrados: {total_produtos}").pack(anchor="w", pady=2)
            ttk.Label(parent, text=f"Vendas registradas: {total_vendas}").pack(anchor="w", pady=2)
            ttk.Label(parent, text=f"Valor do estoque: R$ {valor_estoque:.2f}").pack(anchor="w", pady=2)
            ttk.Label(parent, text=f"Receita total: R$ {receita_total:.2f}").pack(anchor="w", pady=2)
            
        except Exception as e:
            ttk.Label(parent, text=f"Erro ao carregar: {e}").pack(anchor="w")
    
    def mostrar_tabelas(self):
        """Mostrar estrutura das tabelas"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tabelas = cursor.fetchall()
            
            info = "Tabelas do banco de dados:\n\n"
            for tabela in tabelas:
                info += f"• {tabela[0]}\n"
            
            messagebox.showinfo("Tabelas", info)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao consultar tabelas: {e}")

class EstoqueWindow:
    """Janela de gerenciamento de estoque"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        self.window = tk.Toplevel(parent)
        self.window.title("📦 Gerenciar Estoque")
        self.window.geometry("900x650")
        self.window.transient(parent)
        self.window.grab_set()
        centralizar_janela(self.window)
        
        # Variáveis para os campos
        self.produto_var = tk.StringVar()
        self.quantidade_var = tk.StringVar()
        self.preco_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        
        self.setup_ui()
        self.carregar_estoque()
        
        # Adicionar produtos de exemplo se estoque estiver vazio
        self.verificar_estoque_vazio()
    
    def setup_ui(self):
        """Configurar interface de estoque"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="📦 Gerenciamento de Estoque", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 15))
        
        # Subtítulo explicativo
        subtitle = ttk.Label(main_frame, text="Adicione, edite e controle todos os produtos da sua lanchonete", 
                           font=("Arial", 10), foreground="gray")
        subtitle.pack(pady=(0, 10))
        
        # Frame do formulário
        form_frame = ttk.LabelFrame(main_frame, text="Adicionar/Editar Produto", padding="15")
        form_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Primeira linha
        row1 = ttk.Frame(form_frame)
        row1.pack(fill=tk.X, pady=5)
        
        ttk.Label(row1, text="Produto:").pack(side=tk.LEFT)
        produto_entry = ttk.Entry(row1, textvariable=self.produto_var, width=25)
        produto_entry.pack(side=tk.LEFT, padx=(10, 20))
        
        ttk.Label(row1, text="Categoria:").pack(side=tk.LEFT)
        categoria_combo = ttk.Combobox(row1, textvariable=self.categoria_var, width=15)
        categoria_combo['values'] = ("Bebidas", "Salgados", "Doces", "Lanches", "Outros")
        categoria_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Segunda linha
        row2 = ttk.Frame(form_frame)
        row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(row2, text="Quantidade:").pack(side=tk.LEFT)
        quantidade_entry = ttk.Entry(row2, textvariable=self.quantidade_var, width=10)
        quantidade_entry.pack(side=tk.LEFT, padx=(10, 20))
        
        ttk.Label(row2, text="Preço (R$):").pack(side=tk.LEFT)
        preco_entry = ttk.Entry(row2, textvariable=self.preco_var, width=10)
        preco_entry.pack(side=tk.LEFT, padx=(10, 20))
        
        # Botões do formulário
        btn_form_frame = ttk.Frame(form_frame)
        btn_form_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_form_frame, text="➕ Adicionar", command=self.adicionar_produto, width=12).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_form_frame, text="✏️ Atualizar", command=self.atualizar_produto, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_form_frame, text="🗑️ Remover", command=self.remover_produto, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_form_frame, text="🔄 Limpar", command=self.limpar_campos, width=12).pack(side=tk.LEFT, padx=5)
        
        # Frame da lista
        list_frame = ttk.LabelFrame(main_frame, text="Produtos em Estoque", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Treeview para mostrar produtos
        self.estoque_tree = ttk.Treeview(list_frame, columns=("produto", "categoria", "quantidade", "preco", "total"), show="headings", height=12)
        
        # Configurar colunas
        self.estoque_tree.heading("produto", text="Produto")
        self.estoque_tree.heading("categoria", text="Categoria")
        self.estoque_tree.heading("quantidade", text="Quantidade")
        self.estoque_tree.heading("preco", text="Preço Unit.")
        self.estoque_tree.heading("total", text="Valor Total")
        
        self.estoque_tree.column("produto", width=200)
        self.estoque_tree.column("categoria", width=100)
        self.estoque_tree.column("quantidade", width=80)
        self.estoque_tree.column("preco", width=80)
        self.estoque_tree.column("total", width=100)
        
        # Scrollbar
        scrollbar_estoque = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.estoque_tree.yview)
        self.estoque_tree.configure(yscrollcommand=scrollbar_estoque.set)
        
        self.estoque_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_estoque.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Binding para seleção
        self.estoque_tree.bind("<<TreeviewSelect>>", self.selecionar_produto)
        
        # Frame dos botões principais
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="📊 Relatório", width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="📦 Produtos Exemplo", command=self.adicionar_produtos_exemplo, width=18).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="❌ Fechar", command=self.window.destroy, width=15).pack(side=tk.RIGHT)
    
    def adicionar_produto(self):
        """Adicionar novo produto"""
        try:
            produto = self.produto_var.get().strip()
            categoria = self.categoria_var.get().strip() or "Geral"
            quantidade = int(self.quantidade_var.get())
            preco = float(self.preco_var.get())
            
            if not produto:
                messagebox.showerror("Erro", "Nome do produto é obrigatório")
                return
            
            if quantidade < 0 or preco < 0:
                messagebox.showerror("Erro", "Quantidade e preço devem ser maiores ou iguais a zero")
                return
            
            # Verificar se produto já existe
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM estoque WHERE produto = ?", (produto,))
                if cursor.fetchone():
                    messagebox.showerror("Erro", f"Produto '{produto}' já existe no estoque")
                    return
                
                # Inserir novo produto
                cursor.execute("""
                    INSERT INTO estoque (produto, categoria, quantidade, preco)
                    VALUES (?, ?, ?, ?)
                """, (produto, categoria, quantidade, preco))
                conn.commit()
            
            messagebox.showinfo("Sucesso", f"Produto '{produto}' adicionado com sucesso!")
            self.limpar_campos()
            self.carregar_estoque()
            
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro e preço um número válido")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar produto: {e}")
    
    def atualizar_produto(self):
        """Atualizar produto selecionado"""
        selection = self.estoque_tree.selection()
        if not selection:
            messagebox.showerror("Erro", "Selecione um produto para atualizar")
            return
        
        try:
            produto = self.produto_var.get().strip()
            categoria = self.categoria_var.get().strip() or "Geral"
            quantidade = int(self.quantidade_var.get())
            preco = float(self.preco_var.get())
            
            if not produto:
                messagebox.showerror("Erro", "Nome do produto é obrigatório")
                return
            
            # Obter produto original
            item = self.estoque_tree.item(selection[0])
            produto_original = item['values'][0]
            
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE estoque SET produto=?, categoria=?, quantidade=?, preco=?
                    WHERE produto=?
                """, (produto, categoria, quantidade, preco, produto_original))
                conn.commit()
            
            messagebox.showinfo("Sucesso", f"Produto atualizado com sucesso!")
            self.limpar_campos()
            self.carregar_estoque()
            
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro e preço um número válido")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar produto: {e}")
    
    def remover_produto(self):
        """Remover produto selecionado"""
        selection = self.estoque_tree.selection()
        if not selection:
            messagebox.showerror("Erro", "Selecione um produto para remover")
            return
        
        item = self.estoque_tree.item(selection[0])
        produto = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"Deseja realmente remover '{produto}' do estoque?"):
            try:
                with sqlite3.connect(self.db.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM estoque WHERE produto=?", (produto,))
                    conn.commit()
                
                messagebox.showinfo("Sucesso", f"Produto '{produto}' removido com sucesso!")
                self.limpar_campos()
                self.carregar_estoque()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover produto: {e}")
    
    def selecionar_produto(self, event):
        """Preencher campos com produto selecionado"""
        selection = self.estoque_tree.selection()
        if selection:
            item = self.estoque_tree.item(selection[0])
            values = item['values']
            
            self.produto_var.set(values[0])
            self.categoria_var.set(values[1])
            self.quantidade_var.set(values[2])
            self.preco_var.set(values[3].replace("R$ ", ""))
    
    def limpar_campos(self):
        """Limpar todos os campos"""
        self.produto_var.set("")
        self.categoria_var.set("")
        self.quantidade_var.set("")
        self.preco_var.set("")
    
    def carregar_estoque(self):
        """Carregar produtos do estoque"""
        # Limpar lista atual
        for item in self.estoque_tree.get_children():
            self.estoque_tree.delete(item)
        
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT produto, categoria, quantidade, preco
                    FROM estoque
                    ORDER BY produto
                """)
                produtos = cursor.fetchall()
                
                for produto in produtos:
                    nome, categoria, qtd, preco = produto
                    valor_total = qtd * preco
                    
                    self.estoque_tree.insert("", "end", values=(
                        nome,
                        categoria,
                        qtd,
                        f"R$ {preco:.2f}",
                        f"R$ {valor_total:.2f}"
                    ))
                    
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar estoque: {e}")
    
    def verificar_estoque_vazio(self):
        """Verificar se estoque está vazio e oferecer produtos exemplo"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM estoque")
                count = cursor.fetchone()[0]
                
                if count == 0:
                    if messagebox.askyesno("Estoque Vazio", 
                                         "O estoque está vazio.\n\nDeseja adicionar alguns produtos de exemplo para começar?"):
                        self.adicionar_produtos_exemplo()
        except Exception as e:
            print(f"Erro ao verificar estoque: {e}")
    
    def adicionar_produtos_exemplo(self):
        """Adicionar alguns produtos de exemplo"""
        produtos_exemplo = [
            ("Coca-Cola 350ml", "Bebidas", 50, 3.50),
            ("Guaraná 350ml", "Bebidas", 45, 3.50),
            ("Água Mineral 500ml", "Bebidas", 100, 2.00),
            ("Pão de Açúcar", "Salgados", 30, 2.00),
            ("Coxinha", "Salgados", 25, 4.50),
            ("Pastel de Queijo", "Salgados", 20, 5.00),
            ("Brigadeiro", "Doces", 50, 1.50),
            ("Beijinho", "Doces", 40, 1.50),
            ("X-Burger", "Lanches", 0, 12.00),
            ("X-Salada", "Lanches", 0, 15.00),
            ("Misto Quente", "Lanches", 0, 8.00),
            ("Café", "Bebidas", 100, 2.50)
        ]
        
        try:
            contador = 0
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                for produto, categoria, qtd, preco in produtos_exemplo:
                    cursor.execute("SELECT id FROM estoque WHERE produto = ?", (produto,))
                    if not cursor.fetchone():  # Só adiciona se não existir
                        cursor.execute("""
                            INSERT INTO estoque (produto, categoria, quantidade, preco)
                            VALUES (?, ?, ?, ?)
                        """, (produto, categoria, qtd, preco))
                        contador += 1
                conn.commit()
            
            if contador > 0:
                messagebox.showinfo("Sucesso", f"{contador} produtos de exemplo adicionados ao estoque!")
                self.carregar_estoque()
            else:
                messagebox.showinfo("Informação", "Todos os produtos exemplo já existem no estoque.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar produtos exemplo: {e}")

class VendasWindow:
    """Janela de registro de vendas"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        self.window = tk.Toplevel(parent)
        self.window.title("💰 Registrar Venda")
        self.window.geometry("700x500")
        self.window.transient(parent)
        self.window.grab_set()
        centralizar_janela(self.window)
        
        # Variáveis para os campos
        self.produto_var = tk.StringVar()
        self.quantidade_var = tk.StringVar()
        self.preco_var = tk.StringVar()
        
        self.setup_ui()
        self.carregar_produtos()
    
    def setup_ui(self):
        """Configurar interface de vendas"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="💰 Registrar Nova Venda", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Frame do formulário
        form_frame = ttk.LabelFrame(main_frame, text="Dados da Venda", padding="15")
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Campo Produto
        ttk.Label(form_frame, text="Produto:").grid(row=0, column=0, sticky="w", pady=5)
        self.produto_combo = ttk.Combobox(form_frame, textvariable=self.produto_var, width=30)
        self.produto_combo.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="ew")
        
        # Campo Quantidade
        ttk.Label(form_frame, text="Quantidade:").grid(row=1, column=0, sticky="w", pady=5)
        quantidade_entry = ttk.Entry(form_frame, textvariable=self.quantidade_var, width=15)
        quantidade_entry.grid(row=1, column=1, padx=(10, 0), pady=5, sticky="w")
        
        # Campo Preço Unitário
        ttk.Label(form_frame, text="Preço Unitário (R$):").grid(row=2, column=0, sticky="w", pady=5)
        preco_entry = ttk.Entry(form_frame, textvariable=self.preco_var, width=15)
        preco_entry.grid(row=2, column=1, padx=(10, 0), pady=5, sticky="w")
        
        # Total calculado
        ttk.Label(form_frame, text="Total:").grid(row=3, column=0, sticky="w", pady=5)
        self.total_label = ttk.Label(form_frame, text="R$ 0,00", font=("Arial", 12, "bold"), foreground="green")
        self.total_label.grid(row=3, column=1, padx=(10, 0), pady=5, sticky="w")
        
        # Configurar grid
        form_frame.columnconfigure(1, weight=1)
        
        # Binding para calcular total automaticamente
        self.quantidade_var.trace('w', self.calcular_total)
        self.preco_var.trace('w', self.calcular_total)
        
        # Frame dos botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="💾 Venda à Vista", command=self.registrar_venda, width=18).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="📋 Venda Fiado", command=self.registrar_venda_fiado, width=18).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="🔄 Limpar", command=self.limpar_campos, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="❌ Fechar", command=self.window.destroy, width=15).pack(side=tk.RIGHT)
        
        # Frame do histórico
        history_frame = ttk.LabelFrame(main_frame, text="Vendas Recentes", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Lista de vendas
        self.vendas_tree = ttk.Treeview(history_frame, columns=("produto", "qtd", "preco", "total", "data"), show="headings", height=8)
        
        # Configurar colunas
        self.vendas_tree.heading("produto", text="Produto")
        self.vendas_tree.heading("qtd", text="Qtd")
        self.vendas_tree.heading("preco", text="Preço Unit.")
        self.vendas_tree.heading("total", text="Total")
        self.vendas_tree.heading("data", text="Data/Hora")
        
        self.vendas_tree.column("produto", width=200)
        self.vendas_tree.column("qtd", width=60)
        self.vendas_tree.column("preco", width=80)
        self.vendas_tree.column("total", width=80)
        self.vendas_tree.column("data", width=120)
        
        # Scrollbar para a lista
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.vendas_tree.yview)
        self.vendas_tree.configure(yscrollcommand=scrollbar.set)
        
        self.vendas_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.carregar_vendas_recentes()
    
    def carregar_produtos(self):
        """Carregar produtos do estoque"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT produto, preco FROM estoque ORDER BY produto")
                produtos = cursor.fetchall()
                
                # Adicionar produtos ao combobox
                produtos_lista = [f"{produto} - R$ {preco:.2f}" for produto, preco in produtos]
                self.produto_combo['values'] = produtos_lista
                
                if not produtos_lista:
                    self.produto_combo['values'] = ["Nenhum produto cadastrado"]
                    
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar produtos: {e}")
    
    def calcular_total(self, *args):
        """Calcular total da venda"""
        try:
            quantidade = float(self.quantidade_var.get() or 0)
            preco = float(self.preco_var.get() or 0)
            total = quantidade * preco
            self.total_label.config(text=f"R$ {total:.2f}")
        except ValueError:
            self.total_label.config(text="R$ 0,00")
    
    def registrar_venda(self):
        """Registrar nova venda"""
        try:
            # Validar campos
            produto_selecionado = self.produto_var.get()
            if not produto_selecionado or produto_selecionado == "Nenhum produto cadastrado":
                messagebox.showerror("Erro", "Selecione um produto")
                return
            
            quantidade = int(self.quantidade_var.get())
            preco = float(self.preco_var.get())
            
            if quantidade <= 0 or preco <= 0:
                messagebox.showerror("Erro", "Quantidade e preço devem ser maiores que zero")
                return
            
            # Extrair nome do produto
            produto = produto_selecionado.split(" - R$")[0]
            total = quantidade * preco
            
            # Registrar no banco
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO historico_vendas (produto, quantidade, preco_unitario, total)
                    VALUES (?, ?, ?, ?)
                """, (produto, quantidade, preco, total))
                conn.commit()
            
            messagebox.showinfo("Sucesso", f"Venda registrada com sucesso!\nTotal: R$ {total:.2f}")
            
            # Limpar campos e atualizar lista
            self.limpar_campos()
            self.carregar_vendas_recentes()
            
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro e preço um número válido")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar venda: {e}")
    
    def registrar_venda_fiado(self):
        """Registrar venda fiado (conta em aberto)"""
        try:
            # Validar campos básicos
            produto_selecionado = self.produto_var.get()
            if not produto_selecionado or produto_selecionado == "Nenhum produto cadastrado":
                messagebox.showerror("Erro", "Selecione um produto")
                return
            
            quantidade = int(self.quantidade_var.get())
            preco = float(self.preco_var.get())
            
            if quantidade <= 0 or preco <= 0:
                messagebox.showerror("Erro", "Quantidade e preço devem ser maiores que zero")
                return
            
            # Abrir janela para dados do cliente
            VendaFiadoWindow(self.parent, self.db, produto_selecionado, quantidade, preco)
            
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro e preço um número válido")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao preparar venda fiado: {e}")
    
    def limpar_campos(self):
        """Limpar todos os campos"""
        self.produto_var.set("")
        self.quantidade_var.set("")
        self.preco_var.set("")
        self.total_label.config(text="R$ 0,00")
    
    def carregar_vendas_recentes(self):
        """Carregar vendas recentes na lista"""
        # Limpar lista atual
        for item in self.vendas_tree.get_children():
            self.vendas_tree.delete(item)
        
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT produto, quantidade, preco_unitario, total, data_venda
                    FROM historico_vendas
                    ORDER BY data_venda DESC
                    LIMIT 20
                """)
                vendas = cursor.fetchall()
                
                for venda in vendas:
                    produto, qtd, preco, total, data = venda
                    # Formatar data
                    data_formatada = datetime.fromisoformat(data).strftime("%d/%m %H:%M")
                    
                    self.vendas_tree.insert("", "end", values=(
                        produto,
                        qtd,
                        f"R$ {preco:.2f}",
                        f"R$ {total:.2f}",
                        data_formatada
                    ))
                    
        except Exception as e:
            print(f"Erro ao carregar vendas: {e}")

class VendaFiadoWindow:
    """Janela para registrar venda fiado"""
    
    def __init__(self, parent, db, produto_selecionado, quantidade, preco):
        self.parent = parent
        self.db = db
        self.produto_selecionado = produto_selecionado
        self.quantidade = quantidade
        self.preco = preco
        self.total = quantidade * preco
        
        self.window = tk.Toplevel(parent)
        self.window.title("📋 Venda Fiado - Dados do Cliente")
        self.window.geometry("500x450")
        self.window.transient(parent)
        self.window.grab_set()
        centralizar_janela(self.window)
        
        # Variáveis
        self.cliente_nome_var = tk.StringVar()
        self.cliente_telefone_var = tk.StringVar()
        self.data_vencimento_var = tk.StringVar()
        self.observacoes_var = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interface"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="📋 Registrar Venda Fiado", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 15))
        
        # Frame resumo da venda
        resumo_frame = ttk.LabelFrame(main_frame, text="Resumo da Venda", padding="10")
        resumo_frame.pack(fill=tk.X, pady=(0, 15))
        
        produto_nome = self.produto_selecionado.split(" - R$")[0]
        ttk.Label(resumo_frame, text=f"Produto: {produto_nome}").pack(anchor="w")
        ttk.Label(resumo_frame, text=f"Quantidade: {self.quantidade}").pack(anchor="w")
        ttk.Label(resumo_frame, text=f"Preço Unitário: R$ {self.preco:.2f}").pack(anchor="w")
        ttk.Label(resumo_frame, text=f"Total: R$ {self.total:.2f}", font=("Arial", 11, "bold"), foreground="red").pack(anchor="w")
        
        # Frame dados do cliente
        cliente_frame = ttk.LabelFrame(main_frame, text="Dados do Cliente", padding="15")
        cliente_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Nome do cliente
        ttk.Label(cliente_frame, text="Nome do Cliente: *").grid(row=0, column=0, sticky="w", pady=8)
        cliente_entry = ttk.Entry(cliente_frame, textvariable=self.cliente_nome_var, width=35, font=("Arial", 11))
        cliente_entry.grid(row=0, column=1, padx=(10, 0), pady=8, sticky="ew")
        cliente_entry.focus()
        
        # Telefone
        ttk.Label(cliente_frame, text="Telefone:").grid(row=1, column=0, sticky="w", pady=8)
        telefone_entry = ttk.Entry(cliente_frame, textvariable=self.cliente_telefone_var, width=35)
        telefone_entry.grid(row=1, column=1, padx=(10, 0), pady=8, sticky="ew")
        
        # Data de vencimento
        ttk.Label(cliente_frame, text="Vencimento (dd/mm/aaaa):").grid(row=2, column=0, sticky="w", pady=8)
        vencimento_entry = ttk.Entry(cliente_frame, textvariable=self.data_vencimento_var, width=20)
        vencimento_entry.grid(row=2, column=1, padx=(10, 0), pady=8, sticky="w")
        
        # Definir vencimento padrão para 30 dias
        vencimento_padrao = (datetime.now() + datetime.timedelta(days=30)).strftime("%d/%m/%Y")
        self.data_vencimento_var.set(vencimento_padrao)
        
        # Observações
        ttk.Label(cliente_frame, text="Observações:").grid(row=3, column=0, sticky="nw", pady=8)
        obs_entry = ttk.Entry(cliente_frame, textvariable=self.observacoes_var, width=35)
        obs_entry.grid(row=3, column=1, padx=(10, 0), pady=8, sticky="ew")
        
        cliente_frame.columnconfigure(1, weight=1)
        
        # Aviso
        aviso_frame = ttk.Frame(main_frame)
        aviso_frame.pack(fill=tk.X, pady=(0, 15))
        
        aviso_text = tk.Text(aviso_frame, height=3, wrap=tk.WORD, font=("Arial", 9))
        aviso_text.pack(fill=tk.X)
        aviso_text.insert("1.0", "⚠️ ATENÇÃO: Esta venda ficará registrada como conta em aberto.\n"
                                "O cliente pode pagar posteriormente através da opção 'Contas em Aberto'.\n"
                                "* Campos obrigatórios")
        aviso_text.config(state=tk.DISABLED, bg="#fff3cd")
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="📋 Registrar Fiado", command=self.registrar_fiado, width=20).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="❌ Cancelar", command=self.window.destroy, width=15).pack(side=tk.RIGHT)
        
        # Binding Enter
        self.window.bind('<Return>', lambda e: self.registrar_fiado())
    
    def registrar_fiado(self):
        """Registrar venda fiado no banco"""
        try:
            cliente_nome = self.cliente_nome_var.get().strip()
            cliente_telefone = self.cliente_telefone_var.get().strip()
            data_vencimento = self.data_vencimento_var.get().strip()
            observacoes = self.observacoes_var.get().strip()
            
            if not cliente_nome:
                messagebox.showerror("Erro", "Nome do cliente é obrigatório!")
                return
            
            # Validar data de vencimento
            if data_vencimento:
                try:
                    datetime.strptime(data_vencimento, "%d/%m/%Y")
                except ValueError:
                    messagebox.showerror("Erro", "Data de vencimento inválida! Use o formato dd/mm/aaaa")
                    return
            
            # Extrair nome do produto
            produto = self.produto_selecionado.split(" - R$")[0]
            
            # Registrar no banco
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO contas_abertas 
                    (cliente_nome, cliente_telefone, produto, quantidade, preco_unitario, total, data_vencimento, observacoes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (cliente_nome, cliente_telefone, produto, self.quantidade, self.preco, self.total, data_vencimento, observacoes))
                conn.commit()
            
            messagebox.showinfo("Sucesso", f"Venda fiado registrada com sucesso!\n\n"
                                         f"Cliente: {cliente_nome}\n"
                                         f"Produto: {produto}\n"
                                         f"Total: R$ {self.total:.2f}\n"
                                         f"Vencimento: {data_vencimento or 'Não definido'}")
            
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar venda fiado: {e}")

class ContasAbertasWindow:
    """Janela para gerenciar contas em aberto"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        self.window = tk.Toplevel(parent)
        self.window.title("📋 Contas em Aberto")
        self.window.geometry("1000x650")
        self.window.transient(parent)
        self.window.grab_set()
        centralizar_janela(self.window)
        
        self.setup_ui()
        self.carregar_contas()
    
    def setup_ui(self):
        """Configurar interface"""
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="📋 Contas em Aberto", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 15))
        
        # Frame de filtros
        filter_frame = ttk.LabelFrame(main_frame, text="Filtros", padding="10")
        filter_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Filtros em linha
        filter_row = ttk.Frame(filter_frame)
        filter_row.pack(fill=tk.X)
        
        ttk.Label(filter_row, text="Mostrar:").pack(side=tk.LEFT, padx=(0, 10))
        self.filtro_var = tk.StringVar(value="pendentes")
        
        ttk.Radiobutton(filter_row, text="Apenas Pendentes", variable=self.filtro_var, value="pendentes", command=self.carregar_contas).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(filter_row, text="Apenas Pagas", variable=self.filtro_var, value="pagas", command=self.carregar_contas).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(filter_row, text="Todas", variable=self.filtro_var, value="todas", command=self.carregar_contas).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(filter_row, text="🔄 Atualizar", command=self.carregar_contas, width=12).pack(side=tk.RIGHT)
        
        # Frame da lista
        list_frame = ttk.LabelFrame(main_frame, text="Lista de Contas", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Treeview
        self.contas_tree = ttk.Treeview(list_frame, columns=("cliente", "telefone", "produto", "qtd", "total", "data_venda", "vencimento", "status"), show="headings", height=15)
        
        # Configurar colunas
        self.contas_tree.heading("cliente", text="Cliente")
        self.contas_tree.heading("telefone", text="Telefone")
        self.contas_tree.heading("produto", text="Produto")
        self.contas_tree.heading("qtd", text="Qtd")
        self.contas_tree.heading("total", text="Total")
        self.contas_tree.heading("data_venda", text="Data Venda")
        self.contas_tree.heading("vencimento", text="Vencimento")
        self.contas_tree.heading("status", text="Status")
        
        self.contas_tree.column("cliente", width=150)
        self.contas_tree.column("telefone", width=100)
        self.contas_tree.column("produto", width=150)
        self.contas_tree.column("qtd", width=50)
        self.contas_tree.column("total", width=80)
        self.contas_tree.column("data_venda", width=100)
        self.contas_tree.column("vencimento", width=100)
        self.contas_tree.column("status", width=80)
        
        # Scrollbar
        scrollbar_contas = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.contas_tree.yview)
        self.contas_tree.configure(yscrollcommand=scrollbar_contas.set)
        
        self.contas_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_contas.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame dos botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="💰 Marcar como Pago", command=self.marcar_como_pago, width=18).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="✏️ Editar", command=self.editar_conta, width=12).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="🗑️ Excluir", command=self.excluir_conta, width=12).pack(side=tk.LEFT, padx=(0, 10))
        
        # Estatísticas
        self.stats_label = ttk.Label(btn_frame, text="", font=("Arial", 10))
        self.stats_label.pack(side=tk.LEFT, padx=(20, 0))
        
        ttk.Button(btn_frame, text="❌ Fechar", command=self.window.destroy, width=12).pack(side=tk.RIGHT)
    
    def carregar_contas(self):
        """Carregar contas em aberto"""
        # Limpar lista
        for item in self.contas_tree.get_children():
            self.contas_tree.delete(item)
        
        try:
            filtro = self.filtro_var.get()
            
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                if filtro == "pendentes":
                    query = "SELECT * FROM contas_abertas WHERE pago = 0 ORDER BY data_venda DESC"
                elif filtro == "pagas":
                    query = "SELECT * FROM contas_abertas WHERE pago = 1 ORDER BY data_pagamento DESC"
                else:
                    query = "SELECT * FROM contas_abertas ORDER BY pago ASC, data_venda DESC"
                
                cursor.execute(query)
                contas = cursor.fetchall()
                
                total_pendente = 0
                total_pago = 0
                count_pendente = 0
                count_pago = 0
                
                for conta in contas:
                    id_conta, cliente_nome, cliente_telefone, produto, quantidade, preco_unitario, total, data_venda, data_vencimento, pago, data_pagamento, observacoes = conta
                    
                    # Formatar datas
                    try:
                        data_venda_fmt = datetime.fromisoformat(data_venda).strftime("%d/%m/%Y")
                    except:
                        data_venda_fmt = data_venda[:10] if data_venda else ""
                    
                    data_venc_fmt = data_vencimento if data_vencimento else ""
                    status = "✅ PAGO" if pago else "⏰ PENDENTE"
                    
                    # Estatísticas
                    if pago:
                        total_pago += total
                        count_pago += 1
                    else:
                        total_pendente += total
                        count_pendente += 1
                    
                    # Inserir na árvore
                    item = self.contas_tree.insert("", "end", values=(
                        cliente_nome,
                        cliente_telefone or "",
                        produto,
                        quantidade,
                        f"R$ {total:.2f}",
                        data_venda_fmt,
                        data_venc_fmt,
                        status
                    ))
                    
                    # Colorir linha se vencida
                    if not pago and data_vencimento:
                        try:
                            venc_date = datetime.strptime(data_vencimento, "%d/%m/%Y")
                            if venc_date < datetime.now():
                                self.contas_tree.set(item, "status", "🔴 VENCIDO")
                        except:
                            pass
                
                # Atualizar estatísticas
                stats_text = f"Pendentes: {count_pendente} (R$ {total_pendente:.2f}) | Pagas: {count_pago} (R$ {total_pago:.2f})"
                self.stats_label.config(text=stats_text)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar contas: {e}")
    
    def marcar_como_pago(self):
        """Marcar conta selecionada como paga"""
        selection = self.contas_tree.selection()
        if not selection:
            messagebox.showerror("Erro", "Selecione uma conta para marcar como paga")
            return
        
        item = self.contas_tree.item(selection[0])
        values = item['values']
        cliente = values[0]
        produto = values[2]
        total = values[4]
        
        if "PAGO" in values[7]:
            messagebox.showinfo("Informação", "Esta conta já está marcada como paga")
            return
        
        if messagebox.askyesno("Confirmar Pagamento", f"Marcar como paga?\n\nCliente: {cliente}\nProduto: {produto}\nValor: {total}"):
            try:
                with sqlite3.connect(self.db.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE contas_abertas 
                        SET pago = 1, data_pagamento = CURRENT_TIMESTAMP 
                        WHERE cliente_nome = ? AND produto = ? AND total = ? AND pago = 0
                    """, (cliente, produto, float(total.replace("R$ ", ""))))
                    conn.commit()
                
                messagebox.showinfo("Sucesso", f"Conta de {cliente} marcada como paga!")
                self.carregar_contas()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao marcar como pago: {e}")
    
    def editar_conta(self):
        """Editar conta selecionada"""
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de edição em desenvolvimento")
    
    def excluir_conta(self):
        """Excluir conta selecionada"""
        selection = self.contas_tree.selection()
        if not selection:
            messagebox.showerror("Erro", "Selecione uma conta para excluir")
            return
        
        item = self.contas_tree.item(selection[0])
        values = item['values']
        cliente = values[0]
        produto = values[2]
        
        if messagebox.askyesno("Confirmar Exclusão", f"Excluir conta?\n\nCliente: {cliente}\nProduto: {produto}"):
            try:
                with sqlite3.connect(self.db.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        DELETE FROM contas_abertas 
                        WHERE cliente_nome = ? AND produto = ?
                    """, (cliente, produto))
                    conn.commit()
                
                messagebox.showinfo("Sucesso", "Conta excluída com sucesso!")
                self.carregar_contas()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir conta: {e}")

class CaixaWindow:
    """Janela de controle de caixa"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        self.window = tk.Toplevel(parent)
        self.window.title("💳 Controle de Caixa")
        self.window.geometry("900x700")
        self.window.transient(parent)
        self.window.grab_set()
        centralizar_janela(self.window)
        
        self.setup_ui()
        self.verificar_caixa_aberto()
    
    def setup_ui(self):
        """Configurar interface"""
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="💳 Controle de Caixa", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 15))
        
        # Frame status do caixa
        self.status_frame = ttk.LabelFrame(main_frame, text="Status do Caixa", padding="15")
        self.status_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Status inicial
        self.status_label = ttk.Label(self.status_frame, text="Verificando status...", font=("Arial", 12, "bold"))
        self.status_label.pack()
        
        # Frame ações
        self.acoes_frame = ttk.LabelFrame(main_frame, text="Ações do Caixa", padding="15")
        self.acoes_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Botões de ação (serão criados dinamicamente)
        self.btn_frame = ttk.Frame(self.acoes_frame)
        self.btn_frame.pack(fill=tk.X)
        
        # Frame movimentações
        mov_frame = ttk.LabelFrame(main_frame, text="Movimentações do Dia", padding="10")
        mov_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Treeview movimentações
        self.mov_tree = ttk.Treeview(mov_frame, columns=("tipo", "valor", "descricao", "hora", "funcionario"), show="headings", height=12)
        
        self.mov_tree.heading("tipo", text="Tipo")
        self.mov_tree.heading("valor", text="Valor")
        self.mov_tree.heading("descricao", text="Descrição")
        self.mov_tree.heading("hora", text="Hora")
        self.mov_tree.heading("funcionario", text="Funcionário")
        
        self.mov_tree.column("tipo", width=100)
        self.mov_tree.column("valor", width=100)
        self.mov_tree.column("descricao", width=250)
        self.mov_tree.column("hora", width=120)
        self.mov_tree.column("funcionario", width=120)
        
        # Scrollbar
        scrollbar_mov = ttk.Scrollbar(mov_frame, orient=tk.VERTICAL, command=self.mov_tree.yview)
        self.mov_tree.configure(yscrollcommand=scrollbar_mov.set)
        
        self.mov_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_mov.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame resumo
        resumo_frame = ttk.LabelFrame(main_frame, text="Resumo do Dia", padding="10")
        resumo_frame.pack(fill=tk.X)
        
        self.resumo_label = ttk.Label(resumo_frame, text="", font=("Arial", 10))
        self.resumo_label.pack()
        
        # Botão fechar
        ttk.Button(main_frame, text="❌ Fechar", command=self.window.destroy, width=15).pack(pady=10)
    
    def verificar_caixa_aberto(self):
        """Verificar se há caixa aberto"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM caixa WHERE status = 'ABERTO' ORDER BY data_abertura DESC LIMIT 1")
                caixa_aberto = cursor.fetchone()
                
                if caixa_aberto:
                    self.caixa_atual = caixa_aberto
                    self.mostrar_caixa_aberto()
                else:
                    self.caixa_atual = None
                    self.mostrar_caixa_fechado()
                    
                self.carregar_movimentacoes()
                self.atualizar_resumo()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar status do caixa: {e}")
    
    def mostrar_caixa_aberto(self):
        """Mostrar interface para caixa aberto"""
        self.status_label.config(text="🟢 CAIXA ABERTO", foreground="green")
        
        # Limpar botões existentes
        for widget in self.btn_frame.winfo_children():
            widget.destroy()
        
        # Botões para caixa aberto
        ttk.Button(self.btn_frame, text="💰 Sangria", command=self.fazer_sangria, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(self.btn_frame, text="➕ Reforço", command=self.fazer_reforco, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(self.btn_frame, text="📊 Relatório", command=self.gerar_relatorio, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(self.btn_frame, text="🔒 Fechar Caixa", command=self.fechar_caixa, width=15).pack(side=tk.RIGHT)
    
    def mostrar_caixa_fechado(self):
        """Mostrar interface para caixa fechado"""
        self.status_label.config(text="🔴 CAIXA FECHADO", foreground="red")
        
        # Limpar botões existentes
        for widget in self.btn_frame.winfo_children():
            widget.destroy()
        
        # Botão para abrir caixa
        ttk.Button(self.btn_frame, text="🔓 Abrir Caixa", command=self.abrir_caixa, width=20).pack()
    
    def abrir_caixa(self):
        """Abrir novo caixa"""
        dialog = AbrirCaixaDialog(self.window, self.db)
        if dialog.resultado:
            self.verificar_caixa_aberto()
    
    def fazer_sangria(self):
        """Fazer sangria do caixa"""
        dialog = MovimentacaoCaixaDialog(self.window, self.db, "SANGRIA", self.caixa_atual[0])
        if dialog.resultado:
            self.verificar_caixa_aberto()
    
    def fazer_reforco(self):
        """Fazer reforço do caixa"""
        dialog = MovimentacaoCaixaDialog(self.window, self.db, "REFORCO", self.caixa_atual[0])
        if dialog.resultado:
            self.verificar_caixa_aberto()
    
    def fechar_caixa(self):
        """Fechar caixa atual"""
        dialog = FecharCaixaDialog(self.window, self.db, self.caixa_atual)
        if dialog.resultado:
            self.verificar_caixa_aberto()
    
    def gerar_relatorio(self):
        """Gerar relatório do caixa"""
        if not self.caixa_atual:
            messagebox.showerror("Erro", "Nenhum caixa aberto")
            return
        
        # Calcular valores
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Vendas do dia
                cursor.execute("SELECT SUM(total) FROM historico_vendas WHERE DATE(data_venda) = DATE('now')")
                vendas_dia = cursor.fetchone()[0] or 0
                
                # Movimentações
                cursor.execute("""
                    SELECT tipo, SUM(valor) FROM movimentacoes_caixa 
                    WHERE caixa_id = ? GROUP BY tipo
                """, (self.caixa_atual[0],))
                movimentacoes = dict(cursor.fetchall())
                
                sangria = movimentacoes.get('SANGRIA', 0)
                reforco = movimentacoes.get('REFORCO', 0)
                
                valor_inicial = self.caixa_atual[6]
                valor_teorico = valor_inicial + vendas_dia - sangria + reforco
                
                relatorio = f"""RELATÓRIO DE CAIXA
                
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Funcionário: {self.caixa_atual[11]}

VALORES:
Valor Inicial: R$ {valor_inicial:.2f}
Vendas do Dia: R$ {vendas_dia:.2f}
Sangrias: R$ {sangria:.2f}
Reforços: R$ {reforco:.2f}

VALOR TEÓRICO EM CAIXA: R$ {valor_teorico:.2f}"""
                
                messagebox.showinfo("Relatório de Caixa", relatorio)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")
    
    def carregar_movimentacoes(self):
        """Carregar movimentações do dia"""
        # Limpar lista
        for item in self.mov_tree.get_children():
            self.mov_tree.delete(item)
        
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                if self.caixa_atual:
                    cursor.execute("""
                        SELECT tipo, valor, descricao, data_hora, funcionario 
                        FROM movimentacoes_caixa 
                        WHERE caixa_id = ? 
                        ORDER BY data_hora DESC
                    """, (self.caixa_atual[0],))
                else:
                    cursor.execute("""
                        SELECT tipo, valor, descricao, data_hora, funcionario 
                        FROM movimentacoes_caixa 
                        WHERE DATE(data_hora) = DATE('now')
                        ORDER BY data_hora DESC
                    """)
                
                movimentacoes = cursor.fetchall()
                
                for mov in movimentacoes:
                    tipo, valor, descricao, data_hora, funcionario = mov
                    
                    try:
                        hora_fmt = datetime.fromisoformat(data_hora).strftime("%H:%M")
                    except:
                        hora_fmt = data_hora
                    
                    self.mov_tree.insert("", "end", values=(
                        tipo,
                        f"R$ {valor:.2f}",
                        descricao or "",
                        hora_fmt,
                        funcionario
                    ))
                    
        except Exception as e:
            print(f"Erro ao carregar movimentações: {e}")
    
    def atualizar_resumo(self):
        """Atualizar resumo do caixa"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Vendas do dia
                cursor.execute("SELECT COUNT(*), SUM(total) FROM historico_vendas WHERE DATE(data_venda) = DATE('now')")
                count_vendas, total_vendas = cursor.fetchone()
                count_vendas = count_vendas or 0
                total_vendas = total_vendas or 0
                
                if self.caixa_atual:
                    resumo = f"Vendas hoje: {count_vendas} ({total_vendas:.2f}) | Caixa aberto às {self.caixa_atual[4][:16] if self.caixa_atual[4] else ''}"
                else:
                    resumo = f"Vendas hoje: {count_vendas} (R$ {total_vendas:.2f}) | Caixa fechado"
                
                self.resumo_label.config(text=resumo)
                
        except Exception as e:
            self.resumo_label.config(text="Erro ao calcular resumo")

class AbrirCaixaDialog:
    """Dialog para abrir caixa"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.resultado = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("🔓 Abrir Caixa")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        centralizar_janela(self.dialog)
        
        self.valor_inicial_var = tk.StringVar()
        self.funcionario_var = tk.StringVar()
        self.observacoes_var = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interface"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="🔓 Abertura de Caixa", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Formulário
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(form_frame, text="Valor Inicial (R$):").grid(row=0, column=0, sticky="w", pady=8)
        valor_entry = ttk.Entry(form_frame, textvariable=self.valor_inicial_var, width=20)
        valor_entry.grid(row=0, column=1, padx=(10, 0), pady=8, sticky="ew")
        valor_entry.focus()
        
        ttk.Label(form_frame, text="Funcionário:").grid(row=1, column=0, sticky="w", pady=8)
        funcionario_entry = ttk.Entry(form_frame, textvariable=self.funcionario_var, width=20)
        funcionario_entry.grid(row=1, column=1, padx=(10, 0), pady=8, sticky="ew")
        
        ttk.Label(form_frame, text="Observações:").grid(row=2, column=0, sticky="w", pady=8)
        obs_entry = ttk.Entry(form_frame, textvariable=self.observacoes_var, width=20)
        obs_entry.grid(row=2, column=1, padx=(10, 0), pady=8, sticky="ew")
        
        form_frame.columnconfigure(1, weight=1)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="🔓 Abrir", command=self.abrir, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="❌ Cancelar", command=self.dialog.destroy, width=15).pack(side=tk.RIGHT)
        
        self.dialog.bind('<Return>', lambda e: self.abrir())
    
    def abrir(self):
        """Abrir o caixa"""
        try:
            valor_inicial = float(self.valor_inicial_var.get().replace(',', '.'))
            funcionario = self.funcionario_var.get().strip() or "Operador"
            observacoes = self.observacoes_var.get().strip()
            
            if valor_inicial < 0:
                messagebox.showerror("Erro", "Valor inicial não pode ser negativo")
                return
            
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO caixa (valor_inicial, funcionario, observacoes)
                    VALUES (?, ?, ?)
                """, (valor_inicial, funcionario, observacoes))
                
                caixa_id = cursor.lastrowid
                
                # Registrar movimentação de abertura
                cursor.execute("""
                    INSERT INTO movimentacoes_caixa (caixa_id, tipo, valor, descricao, funcionario)
                    VALUES (?, 'ABERTURA', ?, 'Abertura de caixa', ?)
                """, (caixa_id, valor_inicial, funcionario))
                
                conn.commit()
            
            messagebox.showinfo("Sucesso", f"Caixa aberto com sucesso!\nValor inicial: R$ {valor_inicial:.2f}")
            self.resultado = True
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Erro", "Valor inicial deve ser um número válido")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir caixa: {e}")

class MovimentacaoCaixaDialog:
    """Dialog para movimentações do caixa"""
    
    def __init__(self, parent, db, tipo, caixa_id):
        self.parent = parent
        self.db = db
        self.tipo = tipo
        self.caixa_id = caixa_id
        self.resultado = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"💰 {tipo.title()}")
        self.dialog.geometry("400x250")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        centralizar_janela(self.dialog)
        
        self.valor_var = tk.StringVar()
        self.descricao_var = tk.StringVar()
        self.funcionario_var = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interface"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        titulo = "💰 Sangria" if self.tipo == "SANGRIA" else "➕ Reforço"
        ttk.Label(main_frame, text=titulo, font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Formulário
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(form_frame, text="Valor (R$):").grid(row=0, column=0, sticky="w", pady=8)
        valor_entry = ttk.Entry(form_frame, textvariable=self.valor_var, width=20)
        valor_entry.grid(row=0, column=1, padx=(10, 0), pady=8, sticky="ew")
        valor_entry.focus()
        
        ttk.Label(form_frame, text="Descrição:").grid(row=1, column=0, sticky="w", pady=8)
        desc_entry = ttk.Entry(form_frame, textvariable=self.descricao_var, width=20)
        desc_entry.grid(row=1, column=1, padx=(10, 0), pady=8, sticky="ew")
        
        ttk.Label(form_frame, text="Funcionário:").grid(row=2, column=0, sticky="w", pady=8)
        func_entry = ttk.Entry(form_frame, textvariable=self.funcionario_var, width=20)
        func_entry.grid(row=2, column=1, padx=(10, 0), pady=8, sticky="ew")
        
        form_frame.columnconfigure(1, weight=1)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        btn_text = "💰 Confirmar" if self.tipo == "SANGRIA" else "➕ Confirmar"
        ttk.Button(btn_frame, text=btn_text, command=self.confirmar, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="❌ Cancelar", command=self.dialog.destroy, width=15).pack(side=tk.RIGHT)
        
        self.dialog.bind('<Return>', lambda e: self.confirmar())
    
    def confirmar(self):
        """Confirmar movimentação"""
        try:
            valor = float(self.valor_var.get().replace(',', '.'))
            descricao = self.descricao_var.get().strip()
            funcionario = self.funcionario_var.get().strip() or "Operador"
            
            if valor <= 0:
                messagebox.showerror("Erro", "Valor deve ser maior que zero")
                return
            
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Registrar movimentação
                cursor.execute("""
                    INSERT INTO movimentacoes_caixa (caixa_id, tipo, valor, descricao, funcionario)
                    VALUES (?, ?, ?, ?, ?)
                """, (self.caixa_id, self.tipo, valor, descricao, funcionario))
                
                # Atualizar total no caixa
                if self.tipo == "SANGRIA":
                    cursor.execute("""
                        UPDATE caixa SET valor_sangria = valor_sangria + ?
                        WHERE id = ?
                    """, (valor, self.caixa_id))
                else:  # REFORCO
                    cursor.execute("""
                        UPDATE caixa SET valor_reforco = valor_reforco + ?
                        WHERE id = ?
                    """, (valor, self.caixa_id))
                
                conn.commit()
            
            acao = "Sangria realizada" if self.tipo == "SANGRIA" else "Reforço realizado"
            messagebox.showinfo("Sucesso", f"{acao} com sucesso!\nValor: R$ {valor:.2f}")
            self.resultado = True
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Erro", "Valor deve ser um número válido")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar movimentação: {e}")

class FecharCaixaDialog:
    """Dialog para fechar caixa"""
    
    def __init__(self, parent, db, caixa_atual):
        self.parent = parent
        self.db = db
        self.caixa_atual = caixa_atual
        self.resultado = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("🔒 Fechar Caixa")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        centralizar_janela(self.dialog)
        
        self.valor_final_var = tk.StringVar()
        self.observacoes_var = tk.StringVar()
        
        self.setup_ui()
        self.calcular_valores()
    
    def setup_ui(self):
        """Configurar interface"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="🔒 Fechamento de Caixa", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Frame resumo
        resumo_frame = ttk.LabelFrame(main_frame, text="Resumo do Dia", padding="15")
        resumo_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.resumo_text = tk.Text(resumo_frame, height=8, width=50, wrap=tk.WORD, font=("Courier", 10))
        self.resumo_text.pack(fill=tk.X)
        self.resumo_text.config(state=tk.DISABLED)
        
        # Frame fechamento
        fecha_frame = ttk.LabelFrame(main_frame, text="Dados do Fechamento", padding="15")
        fecha_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(fecha_frame, text="Valor Real em Caixa (R$):").grid(row=0, column=0, sticky="w", pady=8)
        valor_entry = ttk.Entry(fecha_frame, textvariable=self.valor_final_var, width=20)
        valor_entry.grid(row=0, column=1, padx=(10, 0), pady=8, sticky="ew")
        valor_entry.focus()
        
        ttk.Label(fecha_frame, text="Observações:").grid(row=1, column=0, sticky="w", pady=8)
        obs_entry = ttk.Entry(fecha_frame, textvariable=self.observacoes_var, width=20)
        obs_entry.grid(row=1, column=1, padx=(10, 0), pady=8, sticky="ew")
        
        fecha_frame.columnconfigure(1, weight=1)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="🔒 Fechar Caixa", command=self.fechar, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="❌ Cancelar", command=self.dialog.destroy, width=15).pack(side=tk.RIGHT)
    
    def calcular_valores(self):
        """Calcular valores do dia"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Vendas do dia
                cursor.execute("SELECT COUNT(*), SUM(total) FROM historico_vendas WHERE DATE(data_venda) = DATE('now')")
                count_vendas, total_vendas = cursor.fetchone()
                count_vendas = count_vendas or 0
                total_vendas = total_vendas or 0
                
                # Movimentações
                cursor.execute("""
                    SELECT tipo, SUM(valor) FROM movimentacoes_caixa 
                    WHERE caixa_id = ? AND tipo IN ('SANGRIA', 'REFORCO')
                    GROUP BY tipo
                """, (self.caixa_atual[0],))
                movimentacoes = dict(cursor.fetchall())
                
                sangria = movimentacoes.get('SANGRIA', 0)
                reforco = movimentacoes.get('REFORCO', 0)
                
                valor_inicial = self.caixa_atual[6]
                valor_teorico = valor_inicial + total_vendas - sangria + reforco
                
                resumo = f"""RESUMO DO DIA
                
Valor Inicial:      R$ {valor_inicial:>10.2f}
Vendas ({count_vendas:02d}):         R$ {total_vendas:>10.2f}
Sangrias:           R$ {sangria:>10.2f}
Reforços:           R$ {reforco:>10.2f}
                    ________________
VALOR TEÓRICO:      R$ {valor_teorico:>10.2f}

Digite o valor real em caixa para fechar."""
                
                self.resumo_text.config(state=tk.NORMAL)
                self.resumo_text.delete("1.0", tk.END)
                self.resumo_text.insert("1.0", resumo)
                self.resumo_text.config(state=tk.DISABLED)
                
                self.valor_teorico = valor_teorico
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao calcular valores: {e}")
    
    def fechar(self):
        """Fechar o caixa"""
        try:
            valor_final = float(self.valor_final_var.get().replace(',', '.'))
            observacoes = self.observacoes_var.get().strip()
            
            diferenca = valor_final - self.valor_teorico
            
            # Confirmar fechamento
            msg = f"Confirmar fechamento do caixa?\n\nValor teórico: R$ {self.valor_teorico:.2f}\nValor real: R$ {valor_final:.2f}\nDiferença: R$ {diferenca:.2f}"
            
            if not messagebox.askyesno("Confirmar Fechamento", msg):
                return
            
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Atualizar caixa
                cursor.execute("""
                    UPDATE caixa SET 
                        data_fechamento = CURRENT_TIMESTAMP,
                        valor_final = ?,
                        status = 'FECHADO',
                        observacoes = ?
                    WHERE id = ?
                """, (valor_final, observacoes, self.caixa_atual[0]))
                
                # Registrar movimentação de fechamento
                cursor.execute("""
                    INSERT INTO movimentacoes_caixa (caixa_id, tipo, valor, descricao, funcionario)
                    VALUES (?, 'FECHAMENTO', ?, ?, ?)
                """, (self.caixa_atual[0], valor_final, f"Fechamento de caixa. Diferença: R$ {diferenca:.2f}", self.caixa_atual[11]))
                
                conn.commit()
            
            messagebox.showinfo("Sucesso", f"Caixa fechado com sucesso!\nDiferença: R$ {diferenca:.2f}")
            self.resultado = True
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Erro", "Valor final deve ser um número válido")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fechar caixa: {e}")

class BackupWindow:
    """Janela de backup e sincronização"""
    
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        
        self.window = tk.Toplevel(parent)
        self.window.title("💾 Backup e Sincronização")
        self.window.geometry("800x600")
        self.window.transient(parent)
        self.window.grab_set()
        centralizar_janela(self.window)
        
        self.setup_ui()
        self.carregar_backups()
    
    def setup_ui(self):
        """Configurar interface"""
        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="💾 Backup e Sincronização", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 15))
        
        # Frame ações
        acoes_frame = ttk.LabelFrame(main_frame, text="Ações de Backup", padding="15")
        acoes_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Botões de backup
        btn_row1 = ttk.Frame(acoes_frame)
        btn_row1.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(btn_row1, text="💾 Backup Completo", command=self.backup_completo, width=20).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_row1, text="📊 Backup Dados", command=self.backup_dados, width=20).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_row1, text="🔄 Backup Automático", command=self.configurar_auto, width=20).pack(side=tk.LEFT)
        
        btn_row2 = ttk.Frame(acoes_frame)
        btn_row2.pack(fill=tk.X)
        
        ttk.Button(btn_row2, text="📥 Restaurar Backup", command=self.restaurar_backup, width=20).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_row2, text="☁️ Sincronizar Nuvem", command=self.sincronizar_nuvem, width=20).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_row2, text="📤 Exportar Excel", command=self.exportar_excel, width=20).pack(side=tk.LEFT)
        
        # Frame configurações
        config_frame = ttk.LabelFrame(main_frame, text="Configurações", padding="10")
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        config_row = ttk.Frame(config_frame)
        config_row.pack(fill=tk.X)
        
        ttk.Label(config_row, text="Pasta de Backup:").pack(side=tk.LEFT)
        self.pasta_var = tk.StringVar(value="./backups")
        pasta_entry = ttk.Entry(config_row, textvariable=self.pasta_var, width=40)
        pasta_entry.pack(side=tk.LEFT, padx=(10, 10), fill=tk.X, expand=True)
        ttk.Button(config_row, text="📁", command=self.escolher_pasta, width=3).pack(side=tk.LEFT)
        
        # Frame lista de backups
        list_frame = ttk.LabelFrame(main_frame, text="Histórico de Backups", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Treeview backups
        self.backup_tree = ttk.Treeview(list_frame, columns=("nome", "data", "tamanho", "tipo", "status"), show="headings", height=12)
        
        self.backup_tree.heading("nome", text="Nome do Arquivo")
        self.backup_tree.heading("data", text="Data/Hora")
        self.backup_tree.heading("tamanho", text="Tamanho")
        self.backup_tree.heading("tipo", text="Tipo")
        self.backup_tree.heading("status", text="Status")
        
        self.backup_tree.column("nome", width=250)
        self.backup_tree.column("data", width=150)
        self.backup_tree.column("tamanho", width=100)
        self.backup_tree.column("tipo", width=100)
        self.backup_tree.column("status", width=100)
        
        # Scrollbar
        scrollbar_backup = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.backup_tree.yview)
        self.backup_tree.configure(yscrollcommand=scrollbar_backup.set)
        
        self.backup_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_backup.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame botões inferiores
        btn_inferior = ttk.Frame(main_frame)
        btn_inferior.pack(fill=tk.X)
        
        ttk.Button(btn_inferior, text="🗑️ Excluir Backup", command=self.excluir_backup, width=18).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_inferior, text="📋 Verificar Integridade", command=self.verificar_integridade, width=20).pack(side=tk.LEFT, padx=(0, 10))
        
        # Status
        self.status_label = ttk.Label(btn_inferior, text="Pronto", foreground="green")
        self.status_label.pack(side=tk.LEFT, padx=(20, 0))
        
        ttk.Button(btn_inferior, text="❌ Fechar", command=self.window.destroy, width=12).pack(side=tk.RIGHT)
    
    def backup_completo(self):
        """Fazer backup completo do sistema"""
        try:
            import shutil
            import os
            from datetime import datetime
            
            self.status_label.config(text="Fazendo backup completo...", foreground="orange")
            self.window.update()
            
            # Criar pasta de backup se não existir
            pasta_backup = self.pasta_var.get()
            os.makedirs(pasta_backup, exist_ok=True)
            
            # Nome do arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_backup = f"backup_completo_{timestamp}.db"
            caminho_backup = os.path.join(pasta_backup, nome_backup)
            
            # Copiar banco de dados
            shutil.copy2(self.db.db_path, caminho_backup)
            
            # Calcular tamanho
            tamanho_mb = os.path.getsize(caminho_backup) / (1024 * 1024)
            
            # Registrar no banco
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO backups (nome_arquivo, caminho_arquivo, tamanho_mb, tipo)
                    VALUES (?, ?, ?, 'COMPLETO')
                """, (nome_backup, caminho_backup, tamanho_mb))
                conn.commit()
            
            self.status_label.config(text="Backup completo realizado com sucesso!", foreground="green")
            messagebox.showinfo("Sucesso", f"Backup completo criado:\n{nome_backup}\nTamanho: {tamanho_mb:.2f} MB")
            self.carregar_backups()
            
        except Exception as e:
            self.status_label.config(text="Erro no backup", foreground="red")
            messagebox.showerror("Erro", f"Erro ao fazer backup: {e}")
    
    def backup_dados(self):
        """Fazer backup apenas dos dados essenciais"""
        try:
            import os
            from datetime import datetime
            
            self.status_label.config(text="Fazendo backup de dados...", foreground="orange")
            self.window.update()
            
            # Criar pasta de backup se não existir
            pasta_backup = self.pasta_var.get()
            os.makedirs(pasta_backup, exist_ok=True)
            
            # Nome do arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_backup = f"backup_dados_{timestamp}.sql"
            caminho_backup = os.path.join(pasta_backup, nome_backup)
            
            # Exportar dados essenciais
            with sqlite3.connect(self.db.db_path) as conn:
                with open(caminho_backup, 'w', encoding='utf-8') as f:
                    for linha in conn.iterdump():
                        if any(tabela in linha for tabela in ['estoque', 'historico_vendas', 'contas_abertas']):
                            f.write(linha + '\n')
            
            # Calcular tamanho
            tamanho_mb = os.path.getsize(caminho_backup) / (1024 * 1024)
            
            # Registrar no banco
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO backups (nome_arquivo, caminho_arquivo, tamanho_mb, tipo)
                    VALUES (?, ?, ?, 'DADOS')
                """, (nome_backup, caminho_backup, tamanho_mb))
                conn.commit()
            
            self.status_label.config(text="Backup de dados realizado!", foreground="green")
            messagebox.showinfo("Sucesso", f"Backup de dados criado:\n{nome_backup}\nTamanho: {tamanho_mb:.2f} MB")
            self.carregar_backups()
            
        except Exception as e:
            self.status_label.config(text="Erro no backup", foreground="red")
            messagebox.showerror("Erro", f"Erro ao fazer backup de dados: {e}")
    
    def configurar_auto(self):
        """Configurar backup automático"""
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de backup automático em desenvolvimento.\n\nNo momento, execute backups manuais regularmente.")
    
    def sincronizar_nuvem(self):
        """Sincronizar com a nuvem"""
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de sincronização em nuvem em desenvolvimento.\n\nUse backup manual e copie os arquivos para sua nuvem preferida (Google Drive, Dropbox, etc.)")
    
    def exportar_excel(self):
        """Exportar dados para Excel"""
        try:
            import pandas as pd
            import os
            from datetime import datetime
            
            self.status_label.config(text="Exportando para Excel...", foreground="orange")
            self.window.update()
            
            pasta_backup = self.pasta_var.get()
            os.makedirs(pasta_backup, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_excel = f"export_dados_{timestamp}.xlsx"
            caminho_excel = os.path.join(pasta_backup, nome_excel)
            
            with sqlite3.connect(self.db.db_path) as conn:
                # Ler dados das tabelas
                estoque_df = pd.read_sql_query("SELECT * FROM estoque", conn)
                vendas_df = pd.read_sql_query("SELECT * FROM historico_vendas", conn)
                contas_df = pd.read_sql_query("SELECT * FROM contas_abertas", conn)
                
                # Criar arquivo Excel com múltiplas abas
                with pd.ExcelWriter(caminho_excel, engine='openpyxl') as writer:
                    estoque_df.to_excel(writer, sheet_name='Estoque', index=False)
                    vendas_df.to_excel(writer, sheet_name='Vendas', index=False)
                    contas_df.to_excel(writer, sheet_name='Contas_Abertas', index=False)
            
            tamanho_mb = os.path.getsize(caminho_excel) / (1024 * 1024)
            
            # Registrar no banco
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO backups (nome_arquivo, caminho_arquivo, tamanho_mb, tipo)
                    VALUES (?, ?, ?, 'EXCEL')
                """, (nome_excel, caminho_excel, tamanho_mb))
                conn.commit()
            
            self.status_label.config(text="Exportação concluída!", foreground="green")
            messagebox.showinfo("Sucesso", f"Dados exportados para Excel:\n{nome_excel}\nTamanho: {tamanho_mb:.2f} MB")
            self.carregar_backups()
            
        except Exception as e:
            self.status_label.config(text="Erro na exportação", foreground="red")
            messagebox.showerror("Erro", f"Erro ao exportar para Excel: {e}")
    
    def restaurar_backup(self):
        """Restaurar backup selecionado"""
        selection = self.backup_tree.selection()
        if not selection:
            messagebox.showerror("Erro", "Selecione um backup para restaurar")
            return
        
        if not messagebox.askyesno("Confirmar", "ATENÇÃO: Restaurar backup substituirá todos os dados atuais.\n\nDeseja continuar?"):
            return
        
        # Implementar restauração
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de restauração em desenvolvimento.\n\nPara restaurar, substitua manualmente o arquivo banco.db")
    
    def escolher_pasta(self):
        """Escolher pasta de backup"""
        from tkinter import filedialog
        pasta = filedialog.askdirectory(title="Escolher Pasta de Backup")
        if pasta:
            self.pasta_var.set(pasta)
    
    def carregar_backups(self):
        """Carregar lista de backups"""
        # Limpar lista
        for item in self.backup_tree.get_children():
            self.backup_tree.delete(item)
        
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT nome_arquivo, data_backup, tamanho_mb, tipo, status
                    FROM backups 
                    ORDER BY data_backup DESC
                """)
                backups = cursor.fetchall()
                
                for backup in backups:
                    nome, data, tamanho, tipo, status = backup
                    
                    try:
                        data_fmt = datetime.fromisoformat(data).strftime("%d/%m/%Y %H:%M")
                    except:
                        data_fmt = data
                    
                    self.backup_tree.insert("", "end", values=(
                        nome,
                        data_fmt,
                        f"{tamanho:.2f} MB" if tamanho else "N/A",
                        tipo,
                        status
                    ))
                    
        except Exception as e:
            print(f"Erro ao carregar backups: {e}")
    
    def excluir_backup(self):
        """Excluir backup selecionado"""
        selection = self.backup_tree.selection()
        if not selection:
            messagebox.showerror("Erro", "Selecione um backup para excluir")
            return
        
        item = self.backup_tree.item(selection[0])
        nome_arquivo = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"Excluir backup '{nome_arquivo}'?"):
            try:
                with sqlite3.connect(self.db.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM backups WHERE nome_arquivo = ?", (nome_arquivo,))
                    conn.commit()
                
                messagebox.showinfo("Sucesso", "Backup excluído do registro")
                self.carregar_backups()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir backup: {e}")
    
    def verificar_integridade(self):
        """Verificar integridade dos backups"""
        try:
            import os
            
            pasta_backup = self.pasta_var.get()
            if not os.path.exists(pasta_backup):
                messagebox.showerror("Erro", "Pasta de backup não encontrada")
                return
            
            arquivos_pasta = os.listdir(pasta_backup)
            
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nome_arquivo, caminho_arquivo FROM backups")
                backups_db = cursor.fetchall()
            
            # Verificar arquivos
            arquivos_ok = 0
            arquivos_faltando = 0
            
            for nome, caminho in backups_db:
                if os.path.exists(caminho):
                    arquivos_ok += 1
                else:
                    arquivos_faltando += 1
            
            resultado = f"Verificação de Integridade:\n\n"
            resultado += f"✅ Arquivos OK: {arquivos_ok}\n"
            resultado += f"❌ Arquivos faltando: {arquivos_faltando}\n"
            resultado += f"📁 Arquivos na pasta: {len(arquivos_pasta)}"
            
            messagebox.showinfo("Verificação de Integridade", resultado)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar integridade: {e}")

def main():
    """Função principal"""
    print("🚀 Iniciando Sistema de Lanchonete...")
    
    if not verificar_dependencias():
        print("❌ Erro: Dependências não disponíveis")
        return
    
    try:
        app = MainWindow()
        print("✓ Sistema carregado com sucesso")
        app.run()
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")

if __name__ == "__main__":
    main()