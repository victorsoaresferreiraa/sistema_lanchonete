"""
Janela principal do sistema de lanchonete
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.estoque.controller import EstoqueController
from src.pedidos.historico import HistoricoController
from src.pedidos.export import ExportController
from src.pedidos.graficos import GraficoController
from src.utils.helpers import centralizar_janela
from src.config.versioning import VersionManager, UpdateChecker
from .estoque_window import EstoqueWindow
from .historico_window import HistoricoWindow


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Lanchonete - v1.0.0")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Inicializar controladores
        self.estoque_controller = EstoqueController()
        self.historico_controller = HistoricoController()
        self.export_controller = ExportController()
        self.grafico_controller = GraficoController()
        self.version_manager = VersionManager()
        self.update_checker = UpdateChecker()
        
        # Configurar interface
        self.setup_ui()
        centralizar_janela(self.root)
        
    def setup_ui(self):
        """Configura a interface gráfica principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título com versão
        versao = self.version_manager.obter_versao_atual()
        title_label = ttk.Label(
            main_frame, 
            text=f"Sistema de Gerenciamento de Lanchonete v{versao}",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para informações rápidas
        info_frame = ttk.LabelFrame(main_frame, text="Resumo Rápido", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Exibir informações básicas
        self.info_label = ttk.Label(info_frame, text="Carregando informações...", font=("Arial", 10))
        self.info_label.pack()
        
        # Carregar informações iniciais
        self.atualizar_informacoes_rapidas()
        
        # Frame para registrar venda
        venda_frame = ttk.LabelFrame(main_frame, text="Registrar Venda", padding="10")
        venda_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Primeira linha - Produto e Quantidade
        ttk.Label(venda_frame, text="Produto:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.produto_var = tk.StringVar()
        self.produto_entry = ttk.Entry(venda_frame, textvariable=self.produto_var, width=25)
        self.produto_entry.grid(row=0, column=1, padx=(0, 10))
        self.produto_entry.bind('<FocusOut>', self.carregar_preco_produto)
        
        ttk.Label(venda_frame, text="Quantidade:").grid(row=0, column=2, sticky=tk.W, padx=(10, 10))
        self.quantidade_var = tk.StringVar()
        self.quantidade_entry = ttk.Entry(venda_frame, textvariable=self.quantidade_var, width=8)
        self.quantidade_entry.grid(row=0, column=3)
        self.quantidade_entry.bind('<KeyRelease>', self.calcular_total)
        
        # Segunda linha - Preço e Total
        ttk.Label(venda_frame, text="Preço Unit. (R$):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.preco_venda_var = tk.StringVar(value="0,00")
        self.preco_venda_entry = ttk.Entry(venda_frame, textvariable=self.preco_venda_var, width=10)
        self.preco_venda_entry.grid(row=1, column=1, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.preco_venda_entry.bind('<KeyRelease>', self.calcular_total)
        
        ttk.Label(venda_frame, text="Total (R$):").grid(row=1, column=2, sticky=tk.W, padx=(10, 10), pady=(5, 0))
        self.total_venda_var = tk.StringVar(value="R$ 0,00")
        self.total_label = ttk.Label(venda_frame, textvariable=self.total_venda_var, 
                                    font=("Arial", 11, "bold"), foreground="green")
        self.total_label.grid(row=1, column=3, sticky=tk.W, pady=(5, 0))
        
        # Terceira linha - Botões
        button_frame = ttk.Frame(venda_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=(10, 0), sticky=tk.W)
        
        ttk.Button(
            button_frame,
            text="Registrar Venda",
            command=self.registrar_venda
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Limpar",
            command=self.limpar_campos_venda
        ).pack(side=tk.LEFT)
        
        # Frame para botões principais
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        # Botões principais em grid 2x2
        ttk.Button(
            buttons_frame,
            text="Consultar Estoque",
            command=self.abrir_estoque,
            width=20
        ).grid(row=0, column=0, padx=(0, 10), pady=(0, 10))
        
        ttk.Button(
            buttons_frame,
            text="Exportar Dados",
            command=self.exportar_dados,
            width=20
        ).grid(row=0, column=1, pady=(0, 10))
        
        ttk.Button(
            buttons_frame,
            text="Visualizar Histórico",
            command=self.abrir_historico,
            width=20
        ).grid(row=1, column=0, padx=(0, 10))
        
        ttk.Button(
            buttons_frame,
            text="Gerar Gráfico",
            command=self.gerar_grafico,
            width=20
        ).grid(row=1, column=1)
        
        # Configurar grid do frame de botões
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        
        # Frame de status
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.status_label = ttk.Label(
            status_frame,
            text="Sistema pronto para uso",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X)
        
    def carregar_preco_produto(self, event=None):
        """Carrega o preço do produto quando selecionado"""
        try:
            produto = self.produto_var.get().strip()
            if produto:
                produto_info = self.estoque_controller.consultar_produto_completo(produto)
                if produto_info:
                    preco = produto_info[2]  # preço
                    self.preco_venda_var.set(f"{preco:.2f}".replace('.', ','))
                else:
                    self.preco_venda_var.set("0,00")
                self.calcular_total()
        except Exception:
            self.preco_venda_var.set("0,00")
            
    def calcular_total(self, event=None):
        """Calcula o total da venda"""
        try:
            quantidade_str = self.quantidade_var.get().strip()
            preco_str = self.preco_venda_var.get().strip().replace(',', '.')
            
            if quantidade_str and preco_str:
                quantidade = float(quantidade_str)
                preco = float(preco_str)
                total = quantidade * preco
                self.total_venda_var.set(f"R$ {total:.2f}".replace('.', ','))
            else:
                self.total_venda_var.set("R$ 0,00")
        except ValueError:
            self.total_venda_var.set("R$ 0,00")
            
    def limpar_campos_venda(self):
        """Limpa todos os campos de venda"""
        self.produto_var.set("")
        self.quantidade_var.set("")
        self.preco_venda_var.set("0,00")
        self.total_venda_var.set("R$ 0,00")

    def registrar_venda(self):
        """Registra uma nova venda"""
        try:
            produto = self.produto_var.get().strip()
            quantidade_str = self.quantidade_var.get().strip()
            preco_str = self.preco_venda_var.get().strip().replace(',', '.')
            
            if not produto:
                messagebox.showerror("Erro", "Nome do produto é obrigatório!")
                return
                
            if not quantidade_str:
                messagebox.showerror("Erro", "Quantidade é obrigatória!")
                return
                
            if not preco_str or preco_str == "0":
                messagebox.showerror("Erro", "Preço é obrigatório e deve ser maior que zero!")
                return
                
            try:
                quantidade = int(quantidade_str)
                if quantidade <= 0:
                    raise ValueError("Quantidade deve ser maior que zero")
            except ValueError:
                messagebox.showerror("Erro", "Quantidade deve ser um número inteiro positivo!")
                return
                
            try:
                preco_unitario = float(preco_str)
                if preco_unitario <= 0:
                    raise ValueError("Preço deve ser maior que zero")
            except ValueError:
                messagebox.showerror("Erro", "Preço deve ser um número válido e maior que zero!")
                return
            
            # Verificar se há estoque suficiente
            produto_info = self.estoque_controller.consultar_produto_completo(produto)
            if produto_info is None:
                # Produto não existe, perguntar se quer criar
                resposta = messagebox.askyesno(
                    "Produto não encontrado", 
                    f"O produto '{produto}' não existe no estoque.\nDeseja criar este produto?"
                )
                if resposta:
                    self.estoque_controller.adicionar_produto(produto, 0, preco_unitario)
                    estoque_atual = 0
                else:
                    return
            else:
                estoque_atual = produto_info[1]  # quantidade
                
            if estoque_atual < quantidade:
                resposta = messagebox.askyesno(
                    "Estoque insuficiente",
                    f"Estoque insuficiente!\nDisponível: {estoque_atual}\nSolicitado: {quantidade}\n\nDeseja continuar mesmo assim?"
                )
                if not resposta:
                    return
            
            # Registrar venda
            sucesso = self.historico_controller.registrar_venda(produto, quantidade, preco_unitario)
            if sucesso:
                # Atualizar estoque apenas se havia estoque suficiente
                if estoque_atual >= quantidade:
                    novo_estoque = estoque_atual - quantidade
                    self.estoque_controller.atualizar_produto(produto, novo_estoque)
                
                # Limpar campos
                self.limpar_campos_venda()
                
                # Atualizar status
                valor_total = quantidade * preco_unitario
                self.status_label.config(text=f"Venda registrada: {produto} (Qtd: {quantidade}, Total: R$ {valor_total:.2f})")
                
                # Atualizar informações rápidas
                self.atualizar_informacoes_rapidas()
                
                messagebox.showinfo("Sucesso", f"Venda registrada com sucesso!\n\nProduto: {produto}\nQuantidade: {quantidade}\nPreço unitário: R$ {preco_unitario:.2f}\nTotal: R$ {valor_total:.2f}")
            else:
                messagebox.showerror("Erro", "Erro ao registrar venda!")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            
    def abrir_estoque(self):
        """Abre a janela de consulta de estoque"""
        EstoqueWindow(self.root, self.estoque_controller)
        
    def abrir_historico(self):
        """Abre a janela de histórico de vendas"""
        HistoricoWindow(self.root, self.historico_controller)
        
    def exportar_dados(self):
        """Exporta dados do estoque para Excel"""
        try:
            arquivo = self.export_controller.exportar_estoque()
            if arquivo:
                self.status_label.config(text=f"Dados exportados para: {arquivo}")
                messagebox.showinfo("Sucesso", f"Dados exportados para:\n{arquivo}")
            else:
                messagebox.showerror("Erro", "Erro ao exportar dados!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
            
    def gerar_grafico(self):
        """Gera gráfico de vendas por produto"""
        try:
            self.grafico_controller.gerar_grafico_vendas()
            self.status_label.config(text="Gráfico gerado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico: {str(e)}")
            
    def atualizar_informacoes_rapidas(self):
        """Atualiza as informações rápidas exibidas"""
        try:
            # Obter estatísticas básicas
            estoque = self.estoque_controller.listar_estoque()
            total_produtos = len(estoque)
            
            receita_total = self.historico_controller.obter_receita_total()
            valor_estoque = self.estoque_controller.obter_valor_total_estoque()
            
            info_text = f"Produtos cadastrados: {total_produtos} | "
            info_text += f"Receita total: R$ {receita_total:.2f} | "
            info_text += f"Valor do estoque: R$ {valor_estoque:.2f}"
            
            self.info_label.config(text=info_text)
            
        except Exception as e:
            self.info_label.config(text="Erro ao carregar informações")
            
    def verificar_atualizacoes_menu(self):
        """Menu para verificar atualizações manualmente"""
        try:
            tem_atualizacao, info = self.update_checker.verificar_ao_iniciar()
            
            if tem_atualizacao:
                mensagem = f"Nova versão disponível: {info['versao']}\n\n"
                mensagem += f"Descrição: {info['descricao']}\n\n"
                mensagem += "Deseja baixar a atualização?"
                
                resposta = messagebox.askyesno("Atualização Disponível", mensagem)
                if resposta and info.get('url_download'):
                    import webbrowser
                    webbrowser.open(info['url_download'])
            else:
                messagebox.showinfo("Atualizações", "Sistema está atualizado!")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar atualizações: {str(e)}")
            
    def run(self):
        """Inicia a aplicação"""
        # Verificar atualizações na inicialização (se configurado)
        try:
            tem_atualizacao, info = self.update_checker.verificar_ao_iniciar()
            if tem_atualizacao and isinstance(info, dict) and info.get('obrigatoria'):
                messagebox.showwarning(
                    "Atualização Obrigatória", 
                    f"É necessário atualizar para a versão {info['versao']} para continuar usando o sistema."
                )
        except:
            pass  # Ignorar erros de verificação de atualização
            
        self.root.mainloop()
