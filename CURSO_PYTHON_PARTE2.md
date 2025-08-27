# 📚 CURSO PYTHON - PARTE 2: MÓDULOS AVANÇADOS

**Continuação do Curso Completo de Python**

---

# 📚 MÓDULO 3: INTERFACE GRÁFICA COM TKINTER

## 🎯 Aula 11: Tkinter Básico

### **Introdução ao Tkinter**
Tkinter é a biblioteca padrão do Python para criar interfaces gráficas (GUI). É perfeita para aplicações desktop como nosso sistema de lanchonete.

#### **Primeira Janela**
```python
import tkinter as tk
from tkinter import ttk, messagebox

# Janela básica
def criar_janela_basica():
    janela = tk.Tk()
    janela.title("Minha Primeira Janela")
    janela.geometry("400x300")  # largura x altura
    janela.resizable(True, True)  # Pode redimensionar
    
    # Centralizar na tela
    janela.update_idletasks()
    x = (janela.winfo_screenwidth() // 2) - (400 // 2)
    y = (janela.winfo_screenheight() // 2) - (300 // 2)
    janela.geometry(f"400x300+{x}+{y}")
    
    # Label simples
    label = tk.Label(janela, text="Bem-vindo ao Sistema!", 
                     font=("Arial", 16))
    label.pack(pady=20)
    
    # Botão que mostra mensagem
    def mostrar_mensagem():
        messagebox.showinfo("Sucesso", "Botão funcionando!")
    
    botao = tk.Button(janela, text="Clique Aqui", 
                      command=mostrar_mensagem,
                      bg="lightblue", font=("Arial", 12))
    botao.pack(pady=10)
    
    janela.mainloop()

criar_janela_basica()
```

### **Widgets Essenciais**
```python
class JanelaCompleta:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Sistema de Lanchonete - Widgets")
        self.janela.geometry("600x500")
        
        self.criar_widgets()
    
    def criar_widgets(self):
        # Frame principal
        frame_principal = ttk.Frame(self.janela, padding="10")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = tk.Label(frame_principal, 
                         text="🍔 Sistema de Lanchonete",
                         font=("Arial", 20, "bold"),
                         fg="blue")
        titulo.pack(pady=(0, 20))
        
        # Frame para inputs
        frame_inputs = ttk.LabelFrame(frame_principal, 
                                     text="Dados do Produto", 
                                     padding="10")
        frame_inputs.pack(fill=tk.X, pady=(0, 20))
        
        # Entry (campo de texto)
        tk.Label(frame_inputs, text="Nome do Produto:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nome = tk.Entry(frame_inputs, width=30, font=("Arial", 11))
        self.entry_nome.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        # Spinbox (número)
        tk.Label(frame_inputs, text="Preço:").grid(row=1, column=0, sticky="w", pady=5)
        self.spinbox_preco = tk.Spinbox(frame_inputs, from_=0, to=999, 
                                       increment=0.5, width=28,
                                       font=("Arial", 11))
        self.spinbox_preco.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        # Combobox (lista suspensa)
        tk.Label(frame_inputs, text="Categoria:").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_categoria = ttk.Combobox(frame_inputs, 
                                           values=["Hambúrgueres", "Bebidas", "Acompanhamentos"],
                                           state="readonly", width=26)
        self.combo_categoria.grid(row=2, column=1, padx=(10, 0), pady=5)
        self.combo_categoria.set("Hambúrgueres")  # Valor padrão
        
        # Checkbutton (caixa de seleção)
        self.var_promocao = tk.BooleanVar()
        check_promocao = tk.Checkbutton(frame_inputs, 
                                       text="Produto em promoção",
                                       variable=self.var_promocao,
                                       font=("Arial", 10))
        check_promocao.grid(row=3, column=0, columnspan=2, sticky="w", pady=5)
        
        # Radiobuttons (opção única)
        tk.Label(frame_inputs, text="Tamanho:").grid(row=4, column=0, sticky="w", pady=5)
        
        frame_radio = tk.Frame(frame_inputs)
        frame_radio.grid(row=4, column=1, padx=(10, 0), pady=5, sticky="w")
        
        self.var_tamanho = tk.StringVar(value="Médio")
        
        for i, tamanho in enumerate(["Pequeno", "Médio", "Grande"]):
            radio = tk.Radiobutton(frame_radio, text=tamanho, 
                                  variable=self.var_tamanho, 
                                  value=tamanho,
                                  font=("Arial", 9))
            radio.pack(side=tk.LEFT, padx=(0, 10))
        
        # Text widget (texto multi-linha)
        tk.Label(frame_principal, text="Observações:", font=("Arial", 11)).pack(anchor="w")
        self.text_obs = tk.Text(frame_principal, height=4, width=60, 
                               font=("Arial", 10))
        self.text_obs.pack(pady=(5, 20))
        
        # Scrollbar para o Text
        scrollbar = tk.Scrollbar(self.text_obs)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_obs.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_obs.yview)
        
        # Frame para botões
        frame_botoes = tk.Frame(frame_principal)
        frame_botoes.pack(pady=20)
        
        # Botões com diferentes estilos
        botao_salvar = tk.Button(frame_botoes, text="💾 Salvar", 
                               command=self.salvar_produto,
                               bg="lightgreen", fg="black",
                               font=("Arial", 12, "bold"),
                               width=12)
        botao_salvar.pack(side=tk.LEFT, padx=5)
        
        botao_limpar = tk.Button(frame_botoes, text="🗑️ Limpar", 
                               command=self.limpar_campos,
                               bg="orange", fg="white",
                               font=("Arial", 12),
                               width=12)
        botao_limpar.pack(side=tk.LEFT, padx=5)
        
        botao_sair = tk.Button(frame_botoes, text="❌ Sair", 
                             command=self.janela.quit,
                             bg="red", fg="white",
                             font=("Arial", 12),
                             width=12)
        botao_sair.pack(side=tk.LEFT, padx=5)
    
    def salvar_produto(self):
        # Coletar dados dos widgets
        nome = self.entry_nome.get()
        preco = self.spinbox_preco.get()
        categoria = self.combo_categoria.get()
        promocao = self.var_promocao.get()
        tamanho = self.var_tamanho.get()
        observacoes = self.text_obs.get("1.0", tk.END).strip()
        
        # Validação básica
        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório!")
            self.entry_nome.focus()
            return
        
        try:
            preco_float = float(preco)
            if preco_float <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número positivo!")
            self.spinbox_preco.focus()
            return
        
        # Criar resumo
        resumo = f"""Produto Cadastrado:
        
Nome: {nome}
Preço: R$ {preco_float:.2f}
Categoria: {categoria}
Tamanho: {tamanho}
Promoção: {'Sim' if promocao else 'Não'}

Observações: {observacoes if observacoes else 'Nenhuma'}"""
        
        messagebox.showinfo("Sucesso", resumo)
    
    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.spinbox_preco.delete(0, tk.END)
        self.spinbox_preco.insert(0, "0")
        self.combo_categoria.set("Hambúrgueres")
        self.var_promocao.set(False)
        self.var_tamanho.set("Médio")
        self.text_obs.delete("1.0", tk.END)
        self.entry_nome.focus()
    
    def executar(self):
        self.janela.mainloop()

# Executar aplicação
app = JanelaCompleta()
app.executar()
```

## 🎯 Aula 12: Widgets e Layout

### **Sistema de Layout - Grid**
```python
class CalculadoraVendas:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Calculadora de Vendas")
        self.janela.geometry("500x400")
        
        # Variáveis para armazenar valores
        self.produtos = []
        self.total_geral = 0.0
        
        self.criar_interface()
    
    def criar_interface(self):
        # Configurar grid principal
        self.janela.columnconfigure(1, weight=1)  # Coluna 1 expande
        
        # Cabeçalho
        header = tk.Label(self.janela, text="🧮 Calculadora de Vendas",
                         font=("Arial", 18, "bold"), bg="lightblue", pady=10)
        header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
        # Seção de entrada de produtos
        frame_produto = ttk.LabelFrame(self.janela, text="Adicionar Produto", padding="10")
        frame_produto.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
        # Configurar grid do frame
        frame_produto.columnconfigure(1, weight=1)
        
        # Labels e Entries em grid
        tk.Label(frame_produto, text="Produto:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.entry_produto = tk.Entry(frame_produto, font=("Arial", 11))
        self.entry_produto.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        
        tk.Label(frame_produto, text="Qtd:").grid(row=0, column=2, sticky="w", padx=(10, 5))
        self.entry_quantidade = tk.Entry(frame_produto, width=8, font=("Arial", 11))
        self.entry_quantidade.grid(row=0, column=3, padx=(0, 10))
        
        tk.Label(frame_produto, text="Preço:").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        self.entry_preco = tk.Entry(frame_produto, font=("Arial", 11))
        self.entry_preco.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(10, 0))
        
        # Botão Adicionar
        btn_adicionar = tk.Button(frame_produto, text="➕ Adicionar",
                                 command=self.adicionar_produto,
                                 bg="lightgreen", font=("Arial", 10, "bold"))
        btn_adicionar.grid(row=1, column=2, columnspan=2, pady=(10, 0), padx=(10, 0))
        
        # Lista de produtos (usando Listbox)
        frame_lista = ttk.LabelFrame(self.janela, text="Produtos no Carrinho", padding="10")
        frame_lista.grid(row=2, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        frame_lista.columnconfigure(0, weight=1)
        
        # Listbox com scrollbar
        frame_listbox = tk.Frame(frame_lista)
        frame_listbox.grid(row=0, column=0, sticky="ew")
        frame_listbox.columnconfigure(0, weight=1)
        
        self.listbox_produtos = tk.Listbox(frame_listbox, height=6, font=("Courier", 10))
        self.listbox_produtos.grid(row=0, column=0, sticky="ew")
        
        scrollbar_list = tk.Scrollbar(frame_listbox, orient="vertical")
        scrollbar_list.grid(row=0, column=1, sticky="ns")
        
        self.listbox_produtos.config(yscrollcommand=scrollbar_list.set)
        scrollbar_list.config(command=self.listbox_produtos.yview)
        
        # Botão remover
        btn_remover = tk.Button(frame_lista, text="🗑️ Remover Selecionado",
                               command=self.remover_produto,
                               bg="orange", font=("Arial", 10))
        btn_remover.grid(row=1, column=0, pady=(10, 0))
        
        # Total
        frame_total = tk.Frame(self.janela, bg="yellow", relief="raised", bd=2)
        frame_total.grid(row=3, column=0, columnspan=3, sticky="ew", padx=5, pady=10)
        
        self.label_total = tk.Label(frame_total, text="TOTAL: R$ 0,00",
                                   font=("Arial", 16, "bold"), bg="yellow")
        self.label_total.pack(pady=10)
        
        # Botões finais
        frame_botoes = tk.Frame(self.janela)
        frame_botoes.grid(row=4, column=0, columnspan=3, pady=10)
        
        btn_finalizar = tk.Button(frame_botoes, text="✅ Finalizar Venda",
                                 command=self.finalizar_venda,
                                 bg="green", fg="white",
                                 font=("Arial", 12, "bold"), width=15)
        btn_finalizar.pack(side=tk.LEFT, padx=5)
        
        btn_limpar = tk.Button(frame_botoes, text="🗑️ Limpar Tudo",
                              command=self.limpar_tudo,
                              bg="red", fg="white",
                              font=("Arial", 12), width=15)
        btn_limpar.pack(side=tk.LEFT, padx=5)
        
        # Binds para Enter
        self.entry_produto.bind("<Return>", lambda e: self.entry_quantidade.focus())
        self.entry_quantidade.bind("<Return>", lambda e: self.entry_preco.focus())
        self.entry_preco.bind("<Return>", lambda e: self.adicionar_produto())
    
    def adicionar_produto(self):
        try:
            produto = self.entry_produto.get().strip()
            quantidade = int(self.entry_quantidade.get())
            preco = float(self.entry_preco.get())
            
            if not produto:
                messagebox.showerror("Erro", "Nome do produto é obrigatório!")
                return
            
            if quantidade <= 0 or preco <= 0:
                messagebox.showerror("Erro", "Quantidade e preço devem ser positivos!")
                return
            
            subtotal = quantidade * preco
            
            # Adicionar à lista
            item = {
                "produto": produto,
                "quantidade": quantidade,
                "preco": preco,
                "subtotal": subtotal
            }
            
            self.produtos.append(item)
            
            # Atualizar interface
            linha = f"{quantidade:2d}x {produto:<20} R$ {preco:6.2f} = R$ {subtotal:8.2f}"
            self.listbox_produtos.insert(tk.END, linha)
            
            # Atualizar total
            self.total_geral += subtotal
            self.label_total.config(text=f"TOTAL: R$ {self.total_geral:.2f}")
            
            # Limpar campos
            self.entry_produto.delete(0, tk.END)
            self.entry_quantidade.delete(0, tk.END)
            self.entry_preco.delete(0, tk.END)
            self.entry_produto.focus()
            
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser número inteiro e preço deve ser decimal!")
    
    def remover_produto(self):
        selecao = self.listbox_produtos.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um produto para remover!")
            return
        
        indice = selecao[0]
        produto_removido = self.produtos.pop(indice)
        
        # Atualizar total
        self.total_geral -= produto_removido["subtotal"]
        self.label_total.config(text=f"TOTAL: R$ {self.total_geral:.2f}")
        
        # Remover da listbox
        self.listbox_produtos.delete(indice)
    
    def finalizar_venda(self):
        if not self.produtos:
            messagebox.showwarning("Aviso", "Carrinho vazio!")
            return
        
        # Criar relatório da venda
        relatorio = "🧾 RELATÓRIO DA VENDA\n"
        relatorio += "=" * 40 + "\n\n"
        
        for item in self.produtos:
            relatorio += f"{item['quantidade']:2d}x {item['produto']:<20} "
            relatorio += f"R$ {item['preco']:6.2f} = R$ {item['subtotal']:8.2f}\n"
        
        relatorio += "\n" + "-" * 40 + "\n"
        relatorio += f"TOTAL GERAL: R$ {self.total_geral:.2f}\n"
        relatorio += "=" * 40
        
        messagebox.showinfo("Venda Finalizada", relatorio)
        
        # Limpar tudo após finalizar
        self.limpar_tudo()
    
    def limpar_tudo(self):
        self.produtos.clear()
        self.total_geral = 0.0
        self.listbox_produtos.delete(0, tk.END)
        self.label_total.config(text="TOTAL: R$ 0,00")
        self.entry_produto.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_produto.focus()
    
    def executar(self):
        self.janela.mainloop()

# Executar calculadora
calc = CalculadoraVendas()
calc.executar()
```

### **Sistema de Layout - Pack**
```python
class MenuLanchonete:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Menu da Lanchonete")
        self.janela.geometry("800x600")
        self.janela.configure(bg="white")
        
        self.criar_menu()
    
    def criar_menu(self):
        # Header com pack
        header_frame = tk.Frame(self.janela, bg="darkblue", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)  # Mantém altura fixa
        
        titulo = tk.Label(header_frame, text="🍔 MENU PYTHON BURGER 🍔",
                         font=("Arial", 24, "bold"), fg="white", bg="darkblue")
        titulo.pack(expand=True)
        
        # Subtítulo
        subtitulo = tk.Label(header_frame, text="Escolha seus produtos favoritos",
                           font=("Arial", 12), fg="lightblue", bg="darkblue")
        subtitulo.pack()
        
        # Área de conteúdo
        content_frame = tk.Frame(self.janela, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Menu de categorias (lado esquerdo)
        categorias_frame = tk.Frame(content_frame, bg="lightgray", width=200)
        categorias_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        categorias_frame.pack_propagate(False)
        
        tk.Label(categorias_frame, text="CATEGORIAS", 
                font=("Arial", 14, "bold"), bg="lightgray").pack(pady=10)
        
        categorias = ["🍔 Hambúrgueres", "🍟 Acompanhamentos", "🥤 Bebidas", "🍰 Sobremesas"]
        
        for categoria in categorias:
            btn = tk.Button(categorias_frame, text=categoria,
                           font=("Arial", 11), width=18,
                           command=lambda c=categoria: self.mostrar_categoria(c))
            btn.pack(pady=5, padx=10, fill=tk.X)
        
        # Área de produtos (centro)
        self.produtos_frame = tk.Frame(content_frame, bg="white")
        self.produtos_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Carrinho (lado direito)
        carrinho_frame = tk.Frame(content_frame, bg="lightyellow", width=250)
        carrinho_frame.pack(side=tk.RIGHT, fill=tk.Y)
        carrinho_frame.pack_propagate(False)
        
        tk.Label(carrinho_frame, text="🛒 SEU CARRINHO", 
                font=("Arial", 14, "bold"), bg="lightyellow").pack(pady=10)
        
        # Lista do carrinho
        self.carrinho_listbox = tk.Listbox(carrinho_frame, height=15, font=("Courier", 9))
        self.carrinho_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Total do carrinho
        self.total_label = tk.Label(carrinho_frame, text="TOTAL: R$ 0,00",
                                   font=("Arial", 12, "bold"), bg="lightyellow")
        self.total_label.pack(pady=10)
        
        # Botão finalizar
        btn_finalizar = tk.Button(carrinho_frame, text="✅ FINALIZAR PEDIDO",
                                 bg="green", fg="white", font=("Arial", 10, "bold"))
        btn_finalizar.pack(pady=10, padx=10, fill=tk.X)
        
        # Footer
        footer_frame = tk.Frame(self.janela, bg="darkblue", height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        footer_text = tk.Label(footer_frame, text="Python Burger © 2025 - Atendimento: (11) 99999-9999",
                              font=("Arial", 10), fg="white", bg="darkblue")
        footer_text.pack(expand=True)
        
        # Mostrar categoria inicial
        self.mostrar_categoria("🍔 Hambúrgueres")
    
    def mostrar_categoria(self, categoria):
        # Limpar área de produtos
        for widget in self.produtos_frame.winfo_children():
            widget.destroy()
        
        # Dados dos produtos por categoria
        produtos = {
            "🍔 Hambúrgueres": [
                ("X-Burguer", "Hambúrguer com queijo, alface e tomate", 15.90),
                ("X-Bacon", "Hambúrguer com bacon e queijo", 18.50),
                ("X-Tudo", "Hambúrguer completo", 22.00),
                ("X-Salada", "Hambúrguer com salada", 16.90)
            ],
            "🍟 Acompanhamentos": [
                ("Batata Frita", "Porção individual", 8.00),
                ("Batata Grande", "Porção para compartilhar", 12.00),
                ("Onion Rings", "Anéis de cebola", 9.50),
                ("Nuggets", "10 unidades", 11.00)
            ],
            "🥤 Bebidas": [
                ("Refrigerante", "Lata 350ml", 5.50),
                ("Suco Natural", "Copo 400ml", 7.00),
                ("Água", "Garrafa 500ml", 3.00),
                ("Milk Shake", "Copo 300ml", 9.50)
            ],
            "🍰 Sobremesas": [
                ("Sorvete", "2 bolas", 8.00),
                ("Torta", "Fatia", 12.00),
                ("Pudim", "Fatia", 7.50),
                ("Açaí", "Copo 300ml", 15.00)
            ]
        }
        
        # Título da categoria
        titulo_cat = tk.Label(self.produtos_frame, text=categoria,
                             font=("Arial", 16, "bold"))
        titulo_cat.pack(pady=(0, 20))
        
        # Lista de produtos
        produtos_lista = produtos.get(categoria, [])
        
        for nome, descricao, preco in produtos_lista:
            produto_frame = tk.Frame(self.produtos_frame, relief="raised", 
                                   bd=1, bg="white")
            produto_frame.pack(fill=tk.X, pady=5, padx=10)
            
            # Nome e preço
            header_produto = tk.Frame(produto_frame, bg="white")
            header_produto.pack(fill=tk.X, padx=10, pady=(10, 5))
            
            nome_label = tk.Label(header_produto, text=nome,
                                 font=("Arial", 12, "bold"), bg="white")
            nome_label.pack(side=tk.LEFT)
            
            preco_label = tk.Label(header_produto, text=f"R$ {preco:.2f}",
                                  font=("Arial", 12, "bold"), fg="green", bg="white")
            preco_label.pack(side=tk.RIGHT)
            
            # Descrição
            desc_label = tk.Label(produto_frame, text=descricao,
                                 font=("Arial", 10), fg="gray", bg="white")
            desc_label.pack(anchor="w", padx=10)
            
            # Botão adicionar
            btn_add = tk.Button(produto_frame, text="➕ Adicionar ao Carrinho",
                               bg="lightblue", font=("Arial", 10),
                               command=lambda n=nome, p=preco: self.adicionar_ao_carrinho(n, p))
            btn_add.pack(pady=(5, 10), padx=10, anchor="e")
    
    def adicionar_ao_carrinho(self, nome, preco):
        linha = f"{nome:<20} R$ {preco:6.2f}"
        self.carrinho_listbox.insert(tk.END, linha)
        
        # Atualizar total (simulado)
        total_atual = float(self.total_label.cget("text").split("R$ ")[1].replace(",", "."))
        novo_total = total_atual + preco
        self.total_label.config(text=f"TOTAL: R$ {novo_total:.2f}")
        
        messagebox.showinfo("Sucesso", f"{nome} adicionado ao carrinho!")
    
    def executar(self):
        self.janela.mainloop()

# Executar menu
menu = MenuLanchonete()
menu.executar()
```

## 🎯 Aula 13: Eventos e Callbacks

### **Sistema de Eventos Avançado**
```python
class SistemaEventos:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Sistema de Eventos - Lanchonete")
        self.janela.geometry("700x500")
        
        # Variáveis para demonstrar eventos
        self.contador_cliques = 0
        self.ultima_tecla = ""
        self.posicao_mouse = (0, 0)
        
        self.criar_interface()
        self.configurar_eventos()
    
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.janela, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = tk.Label(main_frame, text="🎮 Demonstração de Eventos",
                         font=("Arial", 18, "bold"))
        titulo.pack(pady=(0, 20))
        
        # Área de demonstração de cliques
        click_frame = ttk.LabelFrame(main_frame, text="Eventos de Mouse", padding="10")
        click_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.btn_clique = tk.Button(click_frame, text="Clique em mim!",
                                   font=("Arial", 14), width=20, height=2,
                                   bg="lightblue")
        self.btn_clique.pack(side=tk.LEFT, padx=(0, 20))
        
        self.label_cliques = tk.Label(click_frame, text="Cliques: 0",
                                     font=("Arial", 12))
        self.label_cliques.pack(side=tk.LEFT)
        
        # Área de demonstração de teclado
        key_frame = ttk.LabelFrame(main_frame, text="Eventos de Teclado", padding="10")
        key_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(key_frame, text="Digite aqui:").pack(anchor="w")
        self.entry_teclas = tk.Entry(key_frame, font=("Arial", 12), width=30)
        self.entry_teclas.pack(anchor="w", pady=(5, 10))
        
        self.label_tecla = tk.Label(key_frame, text="Última tecla: nenhuma",
                                   font=("Arial", 10), fg="blue")
        self.label_tecla.pack(anchor="w")
        
        # Área de movimento do mouse
        mouse_frame = ttk.LabelFrame(main_frame, text="Movimento do Mouse", padding="10")
        mouse_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.canvas_mouse = tk.Canvas(mouse_frame, height=100, bg="lightyellow")
        self.canvas_mouse.pack(fill=tk.X)
        
        self.label_posicao = tk.Label(mouse_frame, text="Posição: (0, 0)",
                                     font=("Arial", 10))
        self.label_posicao.pack(anchor="w")
        
        # Lista de eventos (log)
        log_frame = ttk.LabelFrame(main_frame, text="Log de Eventos", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Listbox com scrollbar
        list_frame = tk.Frame(log_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.listbox_eventos = tk.Listbox(list_frame, font=("Courier", 9))
        self.listbox_eventos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_eventos.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_eventos.yview)
        
        # Botão limpar log
        btn_limpar = tk.Button(log_frame, text="Limpar Log",
                              command=self.limpar_log)
        btn_limpar.pack(pady=(10, 0))
    
    def configurar_eventos(self):
        # Eventos de clique no botão
        self.btn_clique.bind("<Button-1>", self.clique_esquerdo)
        self.btn_clique.bind("<Button-3>", self.clique_direito)
        self.btn_clique.bind("<Double-Button-1>", self.duplo_clique)
        
        # Eventos de teclado
        self.entry_teclas.bind("<KeyPress>", self.tecla_pressionada)
        self.entry_teclas.bind("<KeyRelease>", self.tecla_solta)
        self.entry_teclas.bind("<Return>", self.enter_pressionado)
        
        # Eventos de mouse no canvas
        self.canvas_mouse.bind("<Motion>", self.movimento_mouse)
        self.canvas_mouse.bind("<Button-1>", self.clique_canvas)
        self.canvas_mouse.bind("<Enter>", self.mouse_entrou)
        self.canvas_mouse.bind("<Leave>", self.mouse_saiu)
        
        # Eventos da janela
        self.janela.bind("<Configure>", self.janela_redimensionada)
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        
        # Atalhos de teclado globais
        self.janela.bind("<Control-l>", lambda e: self.limpar_log())
        self.janela.bind("<F1>", self.mostrar_ajuda)
        self.janela.bind("<Escape>", lambda e: self.janela.quit())
    
    def clique_esquerdo(self, event):
        self.contador_cliques += 1
        self.label_cliques.config(text=f"Cliques: {self.contador_cliques}")
        self.log_evento(f"Clique esquerdo no botão - Total: {self.contador_cliques}")
        
        # Mudar cor do botão
        cores = ["lightblue", "lightgreen", "lightyellow", "lightcoral"]
        cor = cores[self.contador_cliques % len(cores)]
        self.btn_clique.config(bg=cor)
    
    def clique_direito(self, event):
        self.log_evento("Clique direito no botão")
        messagebox.showinfo("Clique Direito", "Você clicou com o botão direito!")
    
    def duplo_clique(self, event):
        self.log_evento("Duplo clique no botão")
        self.contador_cliques = 0
        self.label_cliques.config(text="Cliques: 0")
        self.btn_clique.config(bg="lightblue")
    
    def tecla_pressionada(self, event):
        self.ultima_tecla = event.keysym
        self.label_tecla.config(text=f"Última tecla: {self.ultima_tecla}")
        self.log_evento(f"Tecla pressionada: {event.keysym}")
    
    def tecla_solta(self, event):
        self.log_evento(f"Tecla solta: {event.keysym}")
    
    def enter_pressionado(self, event):
        texto = self.entry_teclas.get()
        self.log_evento(f"Enter pressionado - Texto: '{texto}'")
        
        if texto.lower() == "limpar":
            self.limpar_log()
            self.entry_teclas.delete(0, tk.END)
        elif texto.lower() == "sair":
            self.janela.quit()
    
    def movimento_mouse(self, event):
        self.posicao_mouse = (event.x, event.y)
        self.label_posicao.config(text=f"Posição: ({event.x}, {event.y})")
        
        # Desenhar ponto onde o mouse passou
        self.canvas_mouse.create_oval(event.x-2, event.y-2, event.x+2, event.y+2,
                                     fill="red", outline="red")
    
    def clique_canvas(self, event):
        self.log_evento(f"Clique no canvas em ({event.x}, {event.y})")
        
        # Desenhar círculo maior
        self.canvas_mouse.create_oval(event.x-10, event.y-10, event.x+10, event.y+10,
                                     fill="blue", outline="darkblue", width=2)
    
    def mouse_entrou(self, event):
        self.log_evento("Mouse entrou no canvas")
        self.canvas_mouse.config(bg="lightgreen")
    
    def mouse_saiu(self, event):
        self.log_evento("Mouse saiu do canvas")
        self.canvas_mouse.config(bg="lightyellow")
    
    def janela_redimensionada(self, event):
        if event.widget == self.janela:
            self.log_evento(f"Janela redimensionada: {event.width}x{event.height}")
    
    def fechar_janela(self):
        resposta = messagebox.askyesno("Confirmar", "Deseja realmente sair?")
        if resposta:
            self.log_evento("Aplicação fechada pelo usuário")
            self.janela.destroy()
    
    def mostrar_ajuda(self, event):
        ajuda = """🎮 ATALHOS DISPONÍVEIS:
        
F1 - Mostrar esta ajuda
Ctrl+L - Limpar log de eventos
ESC - Sair da aplicação

📝 COMANDOS NO CAMPO DE TEXTO:
'limpar' + Enter - Limpa o log
'sair' + Enter - Fecha aplicação

🖱️ INTERAÇÕES:
Clique esquerdo no botão - Contador
Clique direito no botão - Mensagem
Duplo clique no botão - Zerar contador
Movimento no canvas - Desenha pontos
Clique no canvas - Desenha círculos"""
        
        messagebox.showinfo("Ajuda - Eventos", ajuda)
    
    def log_evento(self, mensagem):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        linha = f"[{timestamp}] {mensagem}"
        
        self.listbox_eventos.insert(tk.END, linha)
        self.listbox_eventos.see(tk.END)  # Scroll automático para o fim
    
    def limpar_log(self):
        self.listbox_eventos.delete(0, tk.END)
        self.canvas_mouse.delete("all")
        self.log_evento("Log limpo")
    
    def executar(self):
        self.log_evento("Aplicação iniciada")
        self.janela.mainloop()

# Executar sistema de eventos
sistema = SistemaEventos()
sistema.executar()
```

### **Sistema de Pedidos com Eventos**
```python
class SistemaPedidosEventos:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Sistema de Pedidos - Eventos Avançados")
        self.janela.geometry("900x700")
        
        # Estado da aplicação
        self.pedido_atual = {"itens": [], "total": 0.0}
        self.modo_rapido = False
        
        self.criar_interface()
        self.configurar_eventos_avancados()
    
    def criar_interface(self):
        # Menu bar
        menubar = tk.Menu(self.janela)
        self.janela.config(menu=menubar)
        
        # Menu Arquivo
        arquivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label="Novo Pedido", command=self.novo_pedido)
        arquivo_menu.add_command(label="Salvar Pedido", command=self.salvar_pedido)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=self.janela.quit)
        
        # Menu Visualizar
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Visualizar", menu=view_menu)
        view_menu.add_command(label="Modo Rápido", command=self.toggle_modo_rapido)
        
        # Frame principal
        main_frame = ttk.Frame(self.janela, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Barra de status
        self.status_var = tk.StringVar(value="Pronto para novo pedido")
        status_bar = tk.Label(self.janela, textvariable=self.status_var,
                             relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Área de produtos (esquerda)
        produtos_frame = ttk.LabelFrame(main_frame, text="Produtos Disponíveis", padding="10")
        produtos_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Área de pedido (direita)
        pedido_frame = ttk.LabelFrame(main_frame, text="Pedido Atual", padding="10")
        pedido_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        self.criar_area_produtos(produtos_frame)
        self.criar_area_pedido(pedido_frame)
    
    def criar_area_produtos(self, parent):
        # Busca de produtos
        search_frame = tk.Frame(parent)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT)
        self.entry_busca = tk.Entry(search_frame, font=("Arial", 11))
        self.entry_busca.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Lista de produtos
        produtos_listframe = tk.Frame(parent)
        produtos_listframe.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para produtos
        colunas = ("Nome", "Preço", "Categoria")
        self.tree_produtos = ttk.Treeview(produtos_listframe, columns=colunas, show="headings", height=15)
        
        # Configurar colunas
        self.tree_produtos.heading("Nome", text="Nome do Produto")
        self.tree_produtos.heading("Preço", text="Preço")
        self.tree_produtos.heading("Categoria", text="Categoria")
        
        self.tree_produtos.column("Nome", width=200)
        self.tree_produtos.column("Preço", width=80)
        self.tree_produtos.column("Categoria", width=120)
        
        self.tree_produtos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar para produtos
        scrollbar_produtos = ttk.Scrollbar(produtos_listframe, orient="vertical", command=self.tree_produtos.yview)
        scrollbar_produtos.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_produtos.configure(yscrollcommand=scrollbar_produtos.set)
        
        # Carregar produtos
        self.carregar_produtos()
    
    def criar_area_pedido(self, parent):
        # Informações do cliente
        cliente_frame = ttk.LabelFrame(parent, text="Cliente", padding="5")
        cliente_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(cliente_frame, text="Nome:").grid(row=0, column=0, sticky="w")
        self.entry_cliente = tk.Entry(cliente_frame, width=25)
        self.entry_cliente.grid(row=0, column=1, padx=(5, 0))
        
        # Lista do pedido
        tk.Label(parent, text="Itens do Pedido:", font=("Arial", 11, "bold")).pack(anchor="w")
        
        # Frame para lista e scrollbar
        lista_frame = tk.Frame(parent)
        lista_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        self.listbox_pedido = tk.Listbox(lista_frame, font=("Courier", 10), width=35)
        self.listbox_pedido.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar_pedido = tk.Scrollbar(lista_frame)
        scrollbar_pedido.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_pedido.config(yscrollcommand=scrollbar_pedido.set)
        scrollbar_pedido.config(command=self.listbox_pedido.yview)
        
        # Total
        self.label_total = tk.Label(parent, text="TOTAL: R$ 0,00",
                                   font=("Arial", 14, "bold"), bg="yellow")
        self.label_total.pack(pady=10)
        
        # Botões
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill=tk.X)
        
        self.btn_remover = tk.Button(btn_frame, text="Remover Item",
                                    command=self.remover_item,
                                    state="disabled")
        self.btn_remover.pack(fill=tk.X, pady=2)
        
        self.btn_finalizar = tk.Button(btn_frame, text="Finalizar Pedido",
                                      command=self.finalizar_pedido,
                                      bg="green", fg="white", font=("Arial", 11, "bold"))
        self.btn_finalizar.pack(fill=tk.X, pady=2)
        
        btn_limpar = tk.Button(btn_frame, text="Limpar Pedido",
                              command=self.novo_pedido,
                              bg="orange")
        btn_limpar.pack(fill=tk.X, pady=2)
    
    def configurar_eventos_avancados(self):
        # Eventos de busca
        self.entry_busca.bind("<KeyRelease>", self.filtrar_produtos)
        self.entry_busca.bind("<Return>", self.focar_primeiro_produto)
        
        # Eventos da lista de produtos
        self.tree_produtos.bind("<Double-Button-1>", self.adicionar_produto_duplo_clique)
        self.tree_produtos.bind("<Return>", self.adicionar_produto_enter)
        
        # Eventos da lista de pedidos
        self.listbox_pedido.bind("<<ListboxSelect>>", self.item_pedido_selecionado)
        self.listbox_pedido.bind("<Delete>", self.remover_item_del)
        
        # Eventos do campo cliente
        self.entry_cliente.bind("<Return>", lambda e: self.entry_busca.focus())
        
        # Atalhos globais
        self.janela.bind("<Control-n>", lambda e: self.novo_pedido())
        self.janela.bind("<Control-f>", lambda e: self.entry_busca.focus())
        self.janela.bind("<Control-s>", lambda e: self.salvar_pedido())
        self.janela.bind("<F5>", lambda e: self.carregar_produtos())
        
        # Timer para auto-save
        self.janela.after(30000, self.auto_save)  # A cada 30 segundos
    
    def carregar_produtos(self):
        # Limpar produtos existentes
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        # Produtos de exemplo
        produtos = [
            ("X-Burguer", 15.90, "Hambúrgueres"),
            ("X-Bacon", 18.50, "Hambúrgueres"),
            ("X-Tudo", 22.00, "Hambúrgueres"),
            ("Batata Frita P", 8.00, "Acompanhamentos"),
            ("Batata Frita G", 12.00, "Acompanhamentos"),
            ("Nuggets", 11.00, "Acompanhamentos"),
            ("Refrigerante", 5.50, "Bebidas"),
            ("Suco Natural", 7.00, "Bebidas"),
            ("Água", 3.00, "Bebidas"),
            ("Sorvete", 8.00, "Sobremesas"),
            ("Torta", 12.00, "Sobremesas")
        ]
        
        for produto in produtos:
            self.tree_produtos.insert("", "end", values=produto)
        
        self.status_var.set(f"Carregados {len(produtos)} produtos")
    
    def filtrar_produtos(self, event):
        termo = self.entry_busca.get().lower()
        
        # Limpar visualização
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        # Recarregar produtos filtrados
        produtos = [
            ("X-Burguer", 15.90, "Hambúrgueres"),
            ("X-Bacon", 18.50, "Hambúrgueres"),
            ("X-Tudo", 22.00, "Hambúrgueres"),
            ("Batata Frita P", 8.00, "Acompanhamentos"),
            ("Batata Frita G", 12.00, "Acompanhamentos"),
            ("Nuggets", 11.00, "Acompanhamentos"),
            ("Refrigerante", 5.50, "Bebidas"),
            ("Suco Natural", 7.00, "Bebidas"),
            ("Água", 3.00, "Bebidas"),
            ("Sorvete", 8.00, "Sobremesas"),
            ("Torta", 12.00, "Sobremesas")
        ]
        
        produtos_filtrados = [p for p in produtos if termo in p[0].lower() or termo in p[2].lower()]
        
        for produto in produtos_filtrados:
            self.tree_produtos.insert("", "end", values=produto)
        
        self.status_var.set(f"Encontrados {len(produtos_filtrados)} produtos")
    
    def focar_primeiro_produto(self, event):
        children = self.tree_produtos.get_children()
        if children:
            self.tree_produtos.focus(children[0])
            self.tree_produtos.selection_set(children[0])
    
    def adicionar_produto_duplo_clique(self, event):
        self.adicionar_produto_selecionado()
    
    def adicionar_produto_enter(self, event):
        self.adicionar_produto_selecionado()
    
    def adicionar_produto_selecionado(self):
        selecionado = self.tree_produtos.selection()
        if not selecionado:
            return
        
        item = self.tree_produtos.item(selecionado[0])
        nome, preco_str, categoria = item["values"]
        preco = float(preco_str)
        
        # Adicionar ao pedido
        item_pedido = {
            "nome": nome,
            "preco": preco,
            "quantidade": 1
        }
        
        self.pedido_atual["itens"].append(item_pedido)
        self.pedido_atual["total"] += preco
        
        # Atualizar interface
        linha = f"1x {nome:<20} R$ {preco:6.2f}"
        self.listbox_pedido.insert(tk.END, linha)
        
        self.label_total.config(text=f"TOTAL: R$ {self.pedido_atual['total']:.2f}")
        
        self.status_var.set(f"Adicionado: {nome}")
        
        # Habilitar botões
        self.btn_finalizar.config(state="normal")
    
    def item_pedido_selecionado(self, event):
        selecionado = self.listbox_pedido.curselection()
        if selecionado:
            self.btn_remover.config(state="normal")
        else:
            self.btn_remover.config(state="disabled")
    
    def remover_item(self):
        selecionado = self.listbox_pedido.curselection()
        if not selecionado:
            return
        
        indice = selecionado[0]
        item_removido = self.pedido_atual["itens"].pop(indice)
        
        # Atualizar total
        self.pedido_atual["total"] -= item_removido["preco"]
        
        # Atualizar interface
        self.listbox_pedido.delete(indice)
        self.label_total.config(text=f"TOTAL: R$ {self.pedido_atual['total']:.2f}")
        
        self.status_var.set(f"Removido: {item_removido['nome']}")
        
        # Desabilitar botões se necessário
        if not self.pedido_atual["itens"]:
            self.btn_finalizar.config(state="disabled")
        
        self.btn_remover.config(state="disabled")
    
    def remover_item_del(self, event):
        self.remover_item()
    
    def novo_pedido(self):
        self.pedido_atual = {"itens": [], "total": 0.0}
        self.listbox_pedido.delete(0, tk.END)
        self.label_total.config(text="TOTAL: R$ 0,00")
        self.entry_cliente.delete(0, tk.END)
        self.btn_finalizar.config(state="disabled")
        self.btn_remover.config(state="disabled")
        self.status_var.set("Novo pedido iniciado")
        self.entry_cliente.focus()
    
    def finalizar_pedido(self):
        cliente = self.entry_cliente.get().strip()
        if not cliente:
            messagebox.showerror("Erro", "Nome do cliente é obrigatório!")
            self.entry_cliente.focus()
            return
        
        if not self.pedido_atual["itens"]:
            messagebox.showerror("Erro", "Adicione pelo menos um item!")
            return
        
        # Criar relatório
        relatorio = f"🧾 PEDIDO FINALIZADO\n"
        relatorio += f"Cliente: {cliente}\n"
        relatorio += f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        relatorio += "Itens:\n"
        
        for item in self.pedido_atual["itens"]:
            relatorio += f"• {item['nome']} - R$ {item['preco']:.2f}\n"
        
        relatorio += f"\nTOTAL: R$ {self.pedido_atual['total']:.2f}"
        
        messagebox.showinfo("Pedido Finalizado", relatorio)
        
        # Iniciar novo pedido
        self.novo_pedido()
    
    def salvar_pedido(self):
        if not self.pedido_atual["itens"]:
            messagebox.showwarning("Aviso", "Nenhum pedido para salvar!")
            return
        
        # Simulação de salvamento
        self.status_var.set("Pedido salvo automaticamente")
        messagebox.showinfo("Salvar", "Pedido salvo com sucesso!")
    
    def toggle_modo_rapido(self):
        self.modo_rapido = not self.modo_rapido
        
        if self.modo_rapido:
            self.status_var.set("Modo Rápido ATIVADO - Duplo clique para adicionar")
            # Configurar eventos de modo rápido
            self.tree_produtos.bind("<Button-1>", self.clique_rapido)
        else:
            self.status_var.set("Modo Rápido DESATIVADO")
            self.tree_produtos.unbind("<Button-1>")
    
    def clique_rapido(self, event):
        # No modo rápido, um clique já adiciona o produto
        self.adicionar_produto_selecionado()
    
    def auto_save(self):
        # Auto-save a cada 30 segundos
        if self.pedido_atual["itens"]:
            self.status_var.set("Auto-save realizado")
        
        # Reagendar
        self.janela.after(30000, self.auto_save)
    
    def executar(self):
        from datetime import datetime
        self.janela.mainloop()

# Executar sistema
sistema = SistemaPedidosEventos()
sistema.executar()
```

### **Continuação do curso...**

Ainda temos muitos módulos pela frente! Vou continuar criando as próximas aulas do curso completo. Já criamos uma base sólida e prática baseada no nosso sistema de lanchonete.