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
        
        ttk.Label(fields_frame, text="Produto:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.produto_var = tk.StringVar()
        self.produto_entry = ttk.Entry(fields_frame, textvariable=self.produto_var, width=30)
        self.produto_entry.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(fields_frame, text="Quantidade:").grid(row=0, column=2, sticky=tk.W, padx=(10, 10))
        self.quantidade_var = tk.StringVar()
        self.quantidade_entry = ttk.Entry(fields_frame, textvariable=self.quantidade_var, width=10)
        self.quantidade_entry.grid(row=0, column=3, padx=(0, 10))
        
        ttk.Button(
            fields_frame,
            text="Adicionar",
            command=self.adicionar_produto
        ).grid(row=0, column=4)
        
        # Frame para tabela de estoque
        table_frame = ttk.LabelFrame(main_frame, text="Estoque Atual", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para exibir estoque
        columns = ("Produto", "Quantidade")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configurar colunas
        self.tree.heading("Produto", text="Produto")
        self.tree.heading("Quantidade", text="Quantidade")
        
        self.tree.column("Produto", width=300)
        self.tree.column("Quantidade", width=100, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview e scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
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
            # Buscar dados do estoque
            estoque = self.estoque_controller.listar_estoque()
            
            if not estoque:
                # Inserir linha indicando estoque vazio
                self.tree.insert("", tk.END, values=("Nenhum produto cadastrado", "-"))
                return
                
            # Inserir dados na tabela
            for produto, quantidade in estoque:
                self.tree.insert("", tk.END, values=(produto, quantidade))
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar estoque: {str(e)}")
            
    def adicionar_produto(self):
        """Adiciona ou atualiza um produto no estoque"""
        try:
            produto = self.produto_var.get().strip()
            quantidade_str = self.quantidade_var.get().strip()
            
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
            
            # Verificar se produto já existe
            estoque_atual = self.estoque_controller.consultar_produto(produto)
            
            if estoque_atual is not None:
                # Produto existe, atualizar
                sucesso = self.estoque_controller.atualizar_produto(produto, quantidade)
                acao = "atualizado"
            else:
                # Produto novo, adicionar
                sucesso = self.estoque_controller.adicionar_produto(produto, quantidade)
                acao = "adicionado"
            
            if sucesso:
                # Limpar campos
                self.produto_var.set("")
                self.quantidade_var.set("")
                
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
