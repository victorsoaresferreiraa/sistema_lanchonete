"""
Janela de visualização do histórico de vendas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.utils.helpers import centralizar_janela


class HistoricoWindow:
    def __init__(self, parent, historico_controller):
        self.parent = parent
        self.historico_controller = historico_controller
        
        # Criar janela
        self.window = tk.Toplevel(parent)
        self.window.title("Histórico de Vendas")
        self.window.geometry("700x500")
        self.window.resizable(True, True)
        
        # Configurar interface
        self.setup_ui()
        centralizar_janela(self.window)
        
        # Carregar dados
        self.carregar_historico()
        
    def setup_ui(self):
        """Configura a interface da janela de histórico"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            main_frame,
            text="Histórico de Vendas",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 10))
        
        # Frame para filtros
        filter_frame = ttk.LabelFrame(main_frame, text="Filtros", padding="10")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campo de busca por produto
        ttk.Label(filter_frame, text="Buscar produto:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.filtro_var = tk.StringVar()
        self.filtro_entry = ttk.Entry(filter_frame, textvariable=self.filtro_var, width=30)
        self.filtro_entry.grid(row=0, column=1, padx=(0, 10))
        self.filtro_entry.bind('<KeyRelease>', self.filtrar_historico)
        
        ttk.Button(
            filter_frame,
            text="Limpar",
            command=self.limpar_filtro
        ).grid(row=0, column=2)
        
        # Frame para tabela de histórico
        table_frame = ttk.LabelFrame(main_frame, text="Vendas Realizadas", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para exibir histórico
        columns = ("ID", "Produto", "Quantidade", "Data/Hora")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Produto", text="Produto")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Data/Hora", text="Data/Hora")
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Produto", width=200)
        self.tree.column("Quantidade", width=100, anchor=tk.CENTER)
        self.tree.column("Data/Hora", width=150, anchor=tk.CENTER)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid treeview e scrollbars
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        v_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        h_scrollbar.grid(row=1, column=0, sticky=tk.EW)
        
        # Configurar grid
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # Frame para estatísticas
        stats_frame = ttk.LabelFrame(main_frame, text="Estatísticas", padding="10")
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.stats_label = ttk.Label(stats_frame, text="", font=("Arial", 10))
        self.stats_label.pack()
        
        # Frame para botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text="Atualizar Lista",
            command=self.carregar_historico
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Exportar Histórico",
            command=self.exportar_historico
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Fechar",
            command=self.window.destroy
        ).pack(side=tk.RIGHT)
        
    def carregar_historico(self):
        """Carrega dados do histórico na tabela"""
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            # Buscar dados do histórico
            historico = self.historico_controller.listar_historico()
            
            if not historico:
                # Inserir linha indicando histórico vazio
                self.tree.insert("", tk.END, values=("-", "Nenhuma venda registrada", "-", "-"))
                self.stats_label.config(text="Nenhuma venda registrada")
                return
                
            # Inserir dados na tabela
            total_vendas = 0
            total_itens = 0
            
            for venda in historico:
                venda_id, produto, quantidade, data_hora = venda
                self.tree.insert("", tk.END, values=(venda_id, produto, quantidade, data_hora))
                total_vendas += 1
                total_itens += quantidade
                
            # Atualizar estatísticas
            self.stats_label.config(
                text=f"Total de vendas: {total_vendas} | Total de itens vendidos: {total_itens}"
            )
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar histórico: {str(e)}")
            
    def filtrar_historico(self, event=None):
        """Filtra o histórico por produto"""
        filtro = self.filtro_var.get().strip().lower()
        
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            # Buscar dados do histórico
            historico = self.historico_controller.listar_historico()
            
            if not historico:
                self.tree.insert("", tk.END, values=("-", "Nenhuma venda registrada", "-", "-"))
                return
                
            # Filtrar e inserir dados
            vendas_filtradas = 0
            total_itens_filtrados = 0
            
            for venda in historico:
                venda_id, produto, quantidade, data_hora = venda
                
                # Aplicar filtro se especificado
                if not filtro or filtro in produto.lower():
                    self.tree.insert("", tk.END, values=(venda_id, produto, quantidade, data_hora))
                    vendas_filtradas += 1
                    total_itens_filtrados += quantidade
                    
            # Atualizar estatísticas
            if filtro:
                self.stats_label.config(
                    text=f"Vendas filtradas: {vendas_filtradas} | Itens filtrados: {total_itens_filtrados}"
                )
            else:
                self.stats_label.config(
                    text=f"Total de vendas: {vendas_filtradas} | Total de itens vendidos: {total_itens_filtrados}"
                )
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao filtrar histórico: {str(e)}")
            
    def limpar_filtro(self):
        """Limpa o filtro e recarrega todo o histórico"""
        self.filtro_var.set("")
        self.carregar_historico()
        
    def exportar_historico(self):
        """Exporta o histórico para Excel"""
        try:
            from src.pedidos.export import ExportController
            export_controller = ExportController()
            
            arquivo = export_controller.exportar_historico()
            if arquivo:
                messagebox.showinfo("Sucesso", f"Histórico exportado para:\n{arquivo}")
            else:
                messagebox.showerror("Erro", "Erro ao exportar histórico!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
