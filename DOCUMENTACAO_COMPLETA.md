# 📚 Documentação Completa - Sistema de Gerenciamento da Lanchonete

## 📖 Índice
1. [Visão Geral do Sistema](#visão-geral-do-sistema)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Como o Python Funciona Aqui](#como-o-python-funciona-aqui)
4. [Banco de Dados Explicado](#banco-de-dados-explicado)
5. [Interface Gráfica (Tkinter)](#interface-gráfica-tkinter)
6. [Fluxo de Funcionamento](#fluxo-de-funcionamento)
7. [Como Modificar Cada Parte](#como-modificar-cada-parte)
8. [Troubleshooting](#troubleshooting)
9. [Expansões Futuras](#expansões-futuras)

---

## 🎯 Visão Geral do Sistema

### O que o sistema faz?
Este é um sistema completo para gerenciar uma lanchonete. Ele controla:
- **Estoque**: produtos, quantidades, preços, categorias
- **Vendas**: registro de vendas com valores
- **Histórico**: todas as vendas realizadas com dados financeiros
- **Relatórios**: exportação para Excel
- **Gráficos**: análise visual das vendas

### Como funciona na prática?
1. **Funcionário abre o sistema** → Aparece a tela principal
2. **Cliente pede um hambúrguer** → Funcionário digita "Hambúrguer", quantidade "1"
3. **Sistema busca o preço automaticamente** → Mostra R$ 15,50
4. **Funcionário pode ajustar o preço** se necessário
5. **Clica "Registrar Venda"** → Sistema salva tudo no banco de dados
6. **Atualiza o estoque automaticamente** → Diminui 1 hambúrguer do estoque

---

## 📁 Estrutura do Projeto

```
📁 sistema_lanchonete/
├── 📄 main.py                    ← Arquivo principal (inicia tudo)
├── 📄 executar_lanchonete.bat    ← Executa o sistema (clique duplo)
├── 📄 build_pyinstaller.py      ← Cria o executável .exe
├── 📄 INSTRUCOES_INSTALACAO.md  ← Como instalar
├── 📄 DOCUMENTACAO_COMPLETA.md  ← Este arquivo
├── 📄 replit.md                 ← Configurações do projeto
├── 📄 pyproject.toml            ← Dependências do Python
│
├── 📁 src/                      ← Código fonte principal
│   ├── 📁 estoque/              ← Gerenciamento de estoque
│   │   ├── 📄 database.py       ← Conecta com banco de dados
│   │   └── 📄 controller.py     ← Lógica de estoque
│   │
│   ├── 📁 interface/            ← Telas do sistema
│   │   ├── 📄 main_window.py    ← Tela principal
│   │   ├── 📄 estoque_window.py ← Tela de consulta estoque
│   │   └── 📄 historico_window.py ← Tela de histórico
│   │
│   ├── 📁 pedidos/              ← Vendas e relatórios
│   │   ├── 📄 controller.py     ← Lógica de vendas
│   │   ├── 📄 export.py         ← Exportar para Excel
│   │   └── 📄 graficos.py       ← Criar gráficos
│   │
│   ├── 📁 utils/                ← Ferramentas auxiliares
│   │   └── 📄 helpers.py        ← Funções úteis
│   │
│   └── 📁 versioning/           ← Controle de versão
│       └── 📄 version_manager.py ← Gerencia atualizações
│
├── 📁 data/                     ← Dados do sistema
│   └── 📄 banco.db              ← Banco de dados SQLite
│
├── 📁 assets/                   ← Recursos visuais
│   └── 📄 icon.ico              ← Ícone do sistema
│
└── 📁 tests/                    ← Testes do sistema
    └── 📄 test_database.py      ← Testa o banco de dados
```

---

## 🐍 Como o Python Funciona Aqui

### Conceitos Básicos que Você Precisa Saber:

#### 1. **Módulos e Imports**
```python
from src.estoque.database import DatabaseManager
```
**O que significa:** "Pegue a classe `DatabaseManager` que está no arquivo `database.py` dentro da pasta `src/estoque/`"

**Como modificar:** Se você quiser usar uma função de outro arquivo, use `from pasta.arquivo import funcao`

#### 2. **Classes (Como Receitas)**
```python
class EstoqueController:
    def __init__(self):
        self.db = DatabaseManager()
    
    def adicionar_produto(self, nome, quantidade):
        # código aqui
```

**O que significa:** 
- `class` = Uma receita para criar objetos
- `__init__` = O que acontece quando você cria o objeto
- `self` = Se refere ao próprio objeto
- `def` = Define uma função (método)

**Como usar:**
```python
estoque = EstoqueController()  # Cria um objeto
estoque.adicionar_produto("Coca-Cola", 10)  # Usa o método
```

#### 3. **Parâmetros e Retornos**
```python
def calcular_total(quantidade, preco):
    total = quantidade * preco
    return total

# Uso:
resultado = calcular_total(2, 15.50)  # resultado = 31.0
```

#### 4. **Try/Except (Tratamento de Erros)**
```python
try:
    # Tenta fazer algo
    preco = float(texto_preco)
except ValueError:
    # Se der erro, faz isso
    print("Preço inválido!")
```

---

## 🗄️ Banco de Dados Explicado

### O que é o SQLite?
É um banco de dados que fica em um arquivo (`banco.db`). Como uma planilha Excel, mas mais poderosa.

### Estrutura das Tabelas:

#### Tabela `estoque`:
```sql
CREATE TABLE estoque (
    produto TEXT PRIMARY KEY,        -- Nome do produto (único)
    quantidade INTEGER,              -- Quantos tem no estoque
    preco REAL,                     -- Preço unitário
    categoria TEXT,                 -- Categoria (ex: "Bebidas")
    codigo_barras TEXT,             -- Código de barras
    data_cadastro TEXT,             -- Quando foi cadastrado
    data_atualizacao TEXT           -- Última atualização
)
```

#### Tabela `historico_vendas`:
```sql
CREATE TABLE historico_vendas (
    id INTEGER PRIMARY KEY,         -- Número único da venda
    produto TEXT,                   -- Produto vendido
    quantidade INTEGER,             -- Quantidade vendida
    preco_unitario REAL,           -- Preço na hora da venda
    valor_total REAL,              -- Total da venda
    data_hora TEXT,                -- Quando foi vendido
    vendedor TEXT,                 -- Quem vendeu
    observacoes TEXT               -- Observações extras
)
```

### Como o Sistema Usa o Banco:

#### Inserir um produto:
```python
def inserir_produto(self, produto, quantidade, preco):
    query = "INSERT INTO estoque (produto, quantidade, preco) VALUES (?, ?, ?)"
    cursor.execute(query, (produto, quantidade, preco))
```

#### Buscar um produto:
```python
def consultar_produto(self, produto):
    query = "SELECT quantidade, preco FROM estoque WHERE produto = ?"
    result = cursor.execute(query, (produto,)).fetchone()
    return result
```

### Como Modificar Consultas:

**Para adicionar uma nova coluna:**
1. Modifique a tabela: `ALTER TABLE estoque ADD COLUMN nova_coluna TEXT`
2. Atualize as consultas para incluir a nova coluna
3. Modifique a interface para mostrar/editar a nova coluna

---

## 🖼️ Interface Gráfica (Tkinter)

### Como Funciona o Tkinter:

#### Estrutura Básica:
```python
import tkinter as tk
from tkinter import ttk

# Criar janela principal
root = tk.Tk()
root.title("Minha Janela")
root.geometry("800x600")

# Criar widgets (botões, labels, etc.)
label = ttk.Label(root, text="Olá Mundo")
label.pack()

button = ttk.Button(root, text="Clique Aqui", command=minha_funcao)
button.pack()

# Iniciar o loop da interface
root.mainloop()
```

#### Principais Widgets Usados:

1. **Label** - Mostra texto
```python
ttk.Label(parent, text="Produto:")
```

2. **Entry** - Campo de entrada de texto
```python
self.produto_var = tk.StringVar()
ttk.Entry(parent, textvariable=self.produto_var)
```

3. **Button** - Botão clicável
```python
ttk.Button(parent, text="Salvar", command=self.salvar)
```

4. **Treeview** - Tabela para mostrar dados
```python
tree = ttk.Treeview(parent, columns=("Nome", "Preço"))
tree.heading("Nome", text="Produto")
tree.insert("", tk.END, values=("Coca-Cola", "R$ 5,00"))
```

#### Layout Managers:

1. **Pack** - Empilha widgets
```python
widget.pack(side=tk.TOP, fill=tk.X)
```

2. **Grid** - Organiza em grade
```python
widget.grid(row=0, column=1, padx=10, pady=5)
```

### Como Modificar a Interface:

#### Para adicionar um novo campo:
1. Crie a variável: `self.novo_campo_var = tk.StringVar()`
2. Crie o label: `ttk.Label(parent, text="Novo Campo:")`
3. Crie o entry: `ttk.Entry(parent, textvariable=self.novo_campo_var)`
4. Posicione com grid ou pack

#### Para adicionar um novo botão:
```python
ttk.Button(
    parent, 
    text="Nova Ação", 
    command=self.nova_funcao
).pack()

def nova_funcao(self):
    # Código da nova funcionalidade
    pass
```

---

## ⚙️ Fluxo de Funcionamento

### 1. Inicialização do Sistema:

```
main.py
  ↓
Carrega configurações
  ↓
Inicializa banco de dados (database.py)
  ↓
Cria controladores (controller.py)
  ↓
Abre tela principal (main_window.py)
```

### 2. Registro de uma Venda:

```
Usuário digita produto → produto_entry
  ↓
Sistema busca no banco → consultar_produto_completo()
  ↓
Carrega preço automaticamente → carregar_preco_produto()
  ↓
Usuário digita quantidade → quantidade_entry
  ↓
Sistema calcula total → calcular_total()
  ↓
Usuário clica "Registrar" → registrar_venda()
  ↓
Valida dados → verificar se estoque tem
  ↓
Salva no histórico → db.registrar_venda()
  ↓
Atualiza estoque → db.atualizar_quantidade()
  ↓
Mostra confirmação → messagebox.showinfo()
```

### 3. Consulta de Estoque:

```
Usuário clica "Consultar Estoque" → abrir_estoque()
  ↓
Abre nova janela → EstoqueWindow()
  ↓
Carrega dados do banco → db.listar_estoque_completo()
  ↓
Mostra na tabela → tree.insert()
  ↓
Usuário pode filtrar → filtrar_estoque()
```

---

## 🔧 Como Modificar Cada Parte

### Para Adicionar um Novo Campo no Produto:

#### 1. Modificar o Banco de Dados:
```python
# Em database.py, no método init_database():
cursor.execute('''
    ALTER TABLE estoque ADD COLUMN fornecedor TEXT DEFAULT ''
''')
```

#### 2. Atualizar as Consultas:
```python
# Em database.py:
def inserir_produto(self, produto, quantidade, preco, categoria, fornecedor):
    query = """INSERT INTO estoque 
               (produto, quantidade, preco, categoria, fornecedor) 
               VALUES (?, ?, ?, ?, ?)"""
    # ...
```

#### 3. Modificar a Interface:
```python
# Em estoque_window.py:
ttk.Label(frame, text="Fornecedor:")
self.fornecedor_var = tk.StringVar()
ttk.Entry(frame, textvariable=self.fornecedor_var)
```

#### 4. Atualizar o Controlador:
```python
# Em controller.py:
def adicionar_produto(self, produto, quantidade, preco, categoria, fornecedor):
    return self.db.inserir_produto(produto, quantidade, preco, categoria, fornecedor)
```

### Para Adicionar uma Nova Tela:

#### 1. Criar o Arquivo:
```python
# src/interface/nova_tela.py
import tkinter as tk
from tkinter import ttk

class NovaTela:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Nova Funcionalidade")
        self.setup_ui()
    
    def setup_ui(self):
        # Criar interface aqui
        pass
```

#### 2. Adicionar Botão na Tela Principal:
```python
# Em main_window.py:
ttk.Button(
    buttons_frame,
    text="Nova Tela",
    command=self.abrir_nova_tela
).grid(row=2, column=0)

def abrir_nova_tela(self):
    from src.interface.nova_tela import NovaTela
    NovaTela(self.root)
```

### Para Modificar Cálculos:

#### Exemplo: Adicionar Desconto
```python
# Em main_window.py:
def calcular_total(self, event=None):
    try:
        quantidade = float(self.quantidade_var.get())
        preco = float(self.preco_venda_var.get().replace(',', '.'))
        desconto = float(self.desconto_var.get() or 0)  # Novo campo
        
        subtotal = quantidade * preco
        total = subtotal - (subtotal * desconto / 100)
        
        self.total_venda_var.set(f"R$ {total:.2f}".replace('.', ','))
    except ValueError:
        self.total_venda_var.set("R$ 0,00")
```

---

## 🚨 Troubleshooting

### Problemas Comuns e Soluções:

#### 1. **Erro: "No such column 'preco'"**
**Causa:** Banco de dados antigo sem as novas colunas
**Solução:**
```bash
# Apagar banco antigo
rm data/banco.db
# Executar sistema novamente para recriar
python main.py
```

#### 2. **Erro: "ModuleNotFoundError"**
**Causa:** Biblioteca não instalada
**Solução:**
```bash
pip install pandas matplotlib openpyxl pillow
```

#### 3. **Interface não responde**
**Causa:** Loop infinito ou operação pesada na thread principal
**Solução:** Usar threading para operações longas:
```python
import threading

def operacao_pesada():
    # código pesado aqui
    pass

# Executar em thread separada
thread = threading.Thread(target=operacao_pesada)
thread.start()
```

#### 4. **Erro ao salvar dados**
**Causa:** Permissões ou arquivo corrompido
**Solução:**
1. Verificar permissões da pasta `data/`
2. Fazer backup do banco: `cp data/banco.db data/banco_backup.db`
3. Verificar integridade: `sqlite3 data/banco.db ".schema"`

### Debug e Logs:

#### Adicionar logs para debug:
```python
import logging

# Configurar logging
logging.basicConfig(
    filename='sistema.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Usar nos métodos
def registrar_venda(self):
    logging.info(f"Tentando registrar venda: {produto}")
    try:
        # código
        logging.info("Venda registrada com sucesso")
    except Exception as e:
        logging.error(f"Erro ao registrar venda: {e}")
```

---

## 🚀 Expansões Futuras

### Funcionalidades Prontas para Implementar:

#### 1. **Sistema de Usuários**
```python
# Nova tabela
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    login TEXT UNIQUE,
    senha_hash TEXT,
    nivel TEXT  -- 'admin', 'vendedor'
)
```

#### 2. **Controle de Caixa**
```python
# Nova tabela
CREATE TABLE movimentacao_caixa (
    id INTEGER PRIMARY KEY,
    tipo TEXT,  -- 'entrada', 'saida'
    valor REAL,
    descricao TEXT,
    data_hora TEXT
)
```

#### 3. **Alertas de Estoque Baixo**
```python
def verificar_estoque_baixo(self):
    produtos = self.db.execute_query(
        "SELECT produto FROM estoque WHERE quantidade < 5"
    )
    if produtos:
        self.mostrar_alerta(f"Estoque baixo: {', '.join(produtos)}")
```

#### 4. **Backup Automático**
```python
import shutil
from datetime import datetime

def fazer_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2('data/banco.db', f'data/backup_{timestamp}.db')
```

#### 5. **Integração com API de Preços**
```python
import requests

def atualizar_precos_online(self):
    # Conectar com API de fornecedor
    response = requests.get('https://api.fornecedor.com/precos')
    precos = response.json()
    
    for produto, preco in precos.items():
        self.db.atualizar_preco(produto, preco)
```

### Como Implementar Novas Funcionalidades:

#### Processo Recomendado:
1. **Planejar** - Definir exatamente o que a funcionalidade deve fazer
2. **Banco de Dados** - Criar/modificar tabelas necessárias
3. **Backend** - Implementar a lógica no controller
4. **Interface** - Criar/modificar telas
5. **Testes** - Testar todas as situações possíveis
6. **Documentar** - Atualizar esta documentação

---

## 📝 Manutenção e Boas Práticas

### Para Manter o Sistema Funcionando:

#### 1. **Backup Regular**
- Copie `data/banco.db` semanalmente
- Mantenha pelo menos 3 backups
- Teste a restauração periodicamente

#### 2. **Atualizações de Dependências**
```bash
# Verificar versões atuais
pip list

# Atualizar todas
pip install --upgrade pandas matplotlib openpyxl pillow

# Ou específica
pip install --upgrade pandas==2.0.0
```

#### 3. **Monitoramento de Performance**
```python
import time

def cronometrar(func):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fim = time.time()
        print(f"{func.__name__} executou em {fim-inicio:.2f} segundos")
        return resultado
    return wrapper

@cronometrar
def operacao_pesada(self):
    # código
    pass
```

#### 4. **Validação de Dados**
```python
def validar_produto(self, nome):
    if not nome or len(nome.strip()) == 0:
        raise ValueError("Nome do produto é obrigatório")
    
    if len(nome) > 100:
        raise ValueError("Nome muito longo (máximo 100 caracteres)")
    
    caracteres_proibidos = ['<', '>', '"', "'"]
    if any(char in nome for char in caracteres_proibidos):
        raise ValueError("Nome contém caracteres inválidos")
```

---

## 📚 Recursos para Aprender Mais

### Documentação Oficial:
- **Python:** https://docs.python.org/pt-br/
- **Tkinter:** https://docs.python.org/3/library/tkinter.html
- **SQLite:** https://sqlite.org/docs.html
- **Pandas:** https://pandas.pydata.org/docs/
- **Matplotlib:** https://matplotlib.org/stable/contents.html

### Tutoriais Recomendados:
- Python para iniciantes: https://python.org.br/introducao/
- Tkinter básico: https://realpython.com/python-gui-tkinter/
- SQLite com Python: https://docs.python.org/3/library/sqlite3.html

---

## 🎯 Resumo Final

Este sistema foi construído com uma arquitetura modular onde cada parte tem uma responsabilidade específica:

- **`main.py`** - Ponto de entrada
- **`database.py`** - Gerencia dados
- **`controller.py`** - Lógica de negócio
- **`*_window.py`** - Interface com usuário
- **`helpers.py`** - Funções auxiliares

Para fazer qualquer modificação:
1. Identifique qual parte precisa ser alterada
2. Modifique o banco se necessário
3. Atualize a lógica no controller
4. Ajuste a interface
5. Teste tudo

O sistema está preparado para crescer e se adaptar às necessidades da lanchonete!