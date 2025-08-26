"""
Janela de consulta e gerenciamento de estoque
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.utils.helpers import centralizar_janela


class EstoqueWindow:
    def __init__(self, parent, estoque_controller):
        self.parent = parent
        self.estoque_controller = estoque_controller
        
        # Criar janela
        self.window = tk.Toplevel(parent)
        self.window.title("Consultar Estoque")
        self.window.geometry("600x400")
        self.window.resizable(True, True)
        
        # Configurar interface
        self.setup_ui()
        centralizar_janela(self.window)
        
        # Carregar dados
        self.carregar_estoque()
        
    def setup_ui(self):
        """Configura a interface da janela de estoque"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            main_frame,
            text="Gerenciamento de Estoque",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 10))
        
        # Frame para adicionar produto
        add_frame = ttk.LabelFrame(main_frame, text="Adicionar/Atualizar Produto", padding="10")
        add_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campos de produto
        fields_frame = ttk.Frame(add_frame)
        fields_frame.pack(fill=tk.X)
        
        # Primeira linha
        ttk.Label(fields_frame, text="Produto:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.produto_var = tk.StringVar()
        self.produto_entry = ttk.Entry(fields_frame, textvariable=self.produto_var, width=25)
        self.produto_entry.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(fields_frame, text="Quantidade:").grid(row=0, column=2, sticky=tk.W, padx=(10, 10))
        self.quantidade_var = tk.StringVar()
        self.quantidade_entry = ttk.Entry(fields_frame, textvariable=self.quantidade_var, width=10)
        self.quantidade_entry.grid(row=0, column=3, padx=(0, 10))
        
        # Segunda linha
        ttk.Label(fields_frame, text="Preço (R$):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.preco_var = tk.StringVar()
        self.preco_entry = ttk.Entry(fields_frame, textvariable=self.preco_var, width=10)
        self.preco_entry.grid(row=1, column=1, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        
        ttk.Label(fields_frame, text="Categoria:").grid(row=1, column=2, sticky=tk.W, padx=(10, 10), pady=(5, 0))
        self.categoria_var = tk.StringVar(value="Geral")
        self.categoria_combo = ttk.Combobox(fields_frame, textvariable=self.categoria_var, width=12)
        self.categoria_combo['values'] = ('Geral', 'Lanches', 'Bebidas', 'Doces', 'Salgados', 'Outros')
        self.categoria_combo.grid(row=1, column=3, padx=(0, 10), pady=(5, 0))
        
        # Terceira linha - botões
        button_row = ttk.Frame(fields_frame)
        button_row.grid(row=2, column=0, columnspan=4, pady=(10, 0), sticky=tk.W)
        
        ttk.Button(
            button_row,
            text="Adicionar/Atualizar",
            command=self.adicionar_produto
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_row,
            text="Limpar Campos",
            command=self.limpar_campos
        ).pack(side=tk.LEFT)
        
        # Frame para tabela de estoque
        table_frame = ttk.LabelFrame(main_frame, text="Estoque Atual", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para exibir estoque
        columns = ("Produto", "Quantidade", "Preço", "Categoria", "Valor Total")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configurar colunas
        self.tree.heading("Produto", text="Produto")
        self.tree.heading("Quantidade", text="Qtd")
        self.tree.heading("Preço", text="Preço (R$)")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Valor Total", text="Valor Total")
        
        self.tree.column("Produto", width=200)
        self.tree.column("Quantidade", width=60, anchor=tk.CENTER)
        self.tree.column("Preço", width=80, anchor=tk.CENTER)
        self.tree.column("Categoria", width=100, anchor=tk.CENTER)
        self.tree.column("Valor Total", width=100, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview e scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind duplo clique para editar
        self.tree.bind('<Double-1>', self.on_item_select)
        
        # Frame para botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text="Atualizar Lista",
            command=self.carregar_estoque
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Remover Produto",
            command=self.remover_produto
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Fechar",
            command=self.window.destroy
        ).pack(side=tk.RIGHT)
        
    def carregar_estoque(self):
        """Carrega dados do estoque na tabela"""
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            # Buscar dados do estoque completo
            estoque = self.estoque_controller.listar_estoque_completo()
            
            if not estoque:
                # Inserir linha indicando estoque vazio
                self.tree.insert("", tk.END, values=("Nenhum produto cadastrado", "-", "-", "-", "-"))
                return
                
            # Inserir dados na tabela
            for item in estoque:
                produto, quantidade, preco, categoria = item[0], item[1], item[2], item[3]
                valor_total = quantidade * preco
                self.tree.insert("", tk.END, values=(
                    produto, 
                    quantidade, 
                    f"{preco:.2f}", 
                    categoria, 
                    f"{valor_total:.2f}"
                ))
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar estoque: {str(e)}")
            
    def adicionar_produto(self):
        """Adiciona ou atualiza um produto no estoque"""
        try:
            produto = self.produto_var.get().strip()
            quantidade_str = self.quantidade_var.get().strip()
            preco_str = self.preco_var.get().strip()
            categoria = self.categoria_var.get().strip()
            
            if not produto:
                messagebox.showerror("Erro", "Nome do produto é obrigatório!")
                return
                
            if not quantidade_str:
                messagebox.showerror("Erro", "Quantidade é obrigatória!")
                return
                
            try:
                quantidade = int(quantidade_str)
                if quantidade < 0:
                    raise ValueError("Quantidade deve ser maior ou igual a zero")
            except ValueError:
                messagebox.showerror("Erro", "Quantidade deve ser um número inteiro não negativo!")
                return
                
            try:
                preco = float(preco_str.replace(',', '.')) if preco_str else 0.0
                if preco < 0:
                    raise ValueError("Preço deve ser maior ou igual a zero")
            except ValueError:
                messagebox.showerror("Erro", "Preço deve ser um número válido!")
                return
            
            if not categoria:
                categoria = "Geral"
            
            # Verificar se produto já existe
            produto_existente = self.estoque_controller.consultar_produto_completo(produto)
            
            if produto_existente is not None:
                # Produto existe, atualizar completamente
                sucesso = self.estoque_controller.atualizar_produto_completo(produto, quantidade, preco, categoria, '')
                acao = "atualizado"
            else:
                # Produto novo, adicionar
                sucesso = self.estoque_controller.adicionar_produto(produto, quantidade, preco, categoria, '')
                acao = "adicionado"
            
            if sucesso:
                # Limpar campos
                self.limpar_campos()
                
                # Recarregar tabela
                self.carregar_estoque()
                
                messagebox.showinfo("Sucesso", f"Produto {acao} com sucesso!")
            else:
                messagebox.showerror("Erro", f"Erro ao {acao.replace('do', 'r')} produto!")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            
    def remover_produto(self):
        """Remove um produto selecionado do estoque"""
        try:
            # Verificar se há item selecionado
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Aviso", "Selecione um produto para remover!")
                return
                
            # Obter dados do item selecionado
            item = self.tree.item(selected[0])
            produto = item['values'][0]
            
            if produto == "Nenhum produto cadastrado":
                return
                
            # Confirmar remoção
            resposta = messagebox.askyesno(
                "Confirmar Remoção",
                f"Deseja realmente remover o produto '{produto}' do estoque?"
            )
            
            if resposta:
                sucesso = self.estoque_controller.remover_produto(produto)
                if sucesso:
                    self.carregar_estoque()
                    messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
                else:
                    messagebox.showerror("Erro", "Erro ao remover produto!")
                    
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            
    def limpar_campos(self):
        """Limpa todos os campos de entrada"""
        self.produto_var.set("")
        self.quantidade_var.set("")
        self.preco_var.set("")
        self.categoria_var.set("Geral")
        
    def on_item_select(self, event):
        """Carrega dados do item selecionado nos campos para edição"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            
            if len(values) >= 4 and values[0] != "Nenhum produto cadastrado":
                self.produto_var.set(values[0])  # produto
                self.quantidade_var.set(str(values[1]))  # quantidade
                self.preco_var.set(str(values[2]).replace(',', '.'))  # preco
                self.categoria_var.set(values[3])  # categoria
