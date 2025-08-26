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
        
        # Campos de venda
        ttk.Label(venda_frame, text="Produto:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.produto_var = tk.StringVar()
        self.produto_entry = ttk.Entry(venda_frame, textvariable=self.produto_var, width=25)
        self.produto_entry.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(venda_frame, text="Quantidade:").grid(row=0, column=2, sticky=tk.W, padx=(10, 10))
        self.quantidade_var = tk.StringVar()
        self.quantidade_entry = ttk.Entry(venda_frame, textvariable=self.quantidade_var, width=10)
        self.quantidade_entry.grid(row=0, column=3)
        
        # Botão registrar venda
        ttk.Button(
            venda_frame,
            text="Registrar Venda",
            command=self.registrar_venda
        ).grid(row=1, column=0, columnspan=4, pady=(10, 0))
        
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
        
    def registrar_venda(self):
        """Registra uma nova venda"""
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
                if quantidade <= 0:
                    raise ValueError("Quantidade deve ser maior que zero")
            except ValueError:
                messagebox.showerror("Erro", "Quantidade deve ser um número inteiro positivo!")
                return
            
            # Verificar se há estoque suficiente
            produto_info = self.estoque_controller.consultar_produto_completo(produto)
            if produto_info is None:
                # Produto não existe, criar com estoque zero
                self.estoque_controller.adicionar_produto(produto, 0, 0.0)
                estoque_atual = 0
                preco_unitario = 0.0
            else:
                estoque_atual = produto_info[1]  # quantidade
                preco_unitario = produto_info[2]  # preco
                
            if estoque_atual < quantidade:
                messagebox.showerror(
                    "Erro",
                    f"Estoque insuficiente! Disponível: {estoque_atual}, Solicitado: {quantidade}"
                )
                return
            
            # Registrar venda
            sucesso = self.historico_controller.registrar_venda(produto, quantidade, preco_unitario)
            if sucesso:
                # Atualizar estoque
                novo_estoque = estoque_atual - quantidade
                self.estoque_controller.atualizar_produto(produto, novo_estoque)
                
                # Limpar campos
                self.produto_var.set("")
                self.quantidade_var.set("")
                
                # Atualizar status
                valor_total = quantidade * preco_unitario
                self.status_label.config(text=f"Venda registrada: {produto} (Qtd: {quantidade}, Total: R$ {valor_total:.2f})")
                
                # Atualizar informações rápidas
                self.atualizar_informacoes_rapidas()
                
                messagebox.showinfo("Sucesso", f"Venda registrada com sucesso!\nTotal: R$ {valor_total:.2f}")
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
