# 🐍 CURSO COMPLETO DE PYTHON - Do Básico ao Avançado

**Baseado no Sistema de Lanchonete Real**

---

## 📋 ÍNDICE DO CURSO

### **MÓDULO 1: FUNDAMENTOS** (Semana 1-2)
- Aula 1: Introdução e Ambiente
- Aula 2: Variáveis e Tipos de Dados
- Aula 3: Estruturas de Controle
- Aula 4: Funções Básicas
- Aula 5: Estruturas de Dados

### **MÓDULO 2: PROGRAMAÇÃO ORIENTADA A OBJETOS** (Semana 3-4)
- Aula 6: Classes e Objetos
- Aula 7: Herança e Polimorfismo
- Aula 8: Encapsulamento e Propriedades
- Aula 9: Métodos Especiais
- Aula 10: Composição vs Herança

### **MÓDULO 3: INTERFACE GRÁFICA COM TKINTER** (Semana 5-6)
- Aula 11: Tkinter Básico
- Aula 12: Widgets e Layout
- Aula 13: Eventos e Callbacks
- Aula 14: Janelas Modais
- Aula 15: Temas e Estilos

### **MÓDULO 4: BANCO DE DADOS E SQLITE** (Semana 7-8)
- Aula 16: SQLite Básico
- Aula 17: CRUD Operations
- Aula 18: Relacionamentos
- Aula 19: Transações
- Aula 20: Otimização de Queries

### **MÓDULO 5: ARQUITETURA E PADRÕES** (Semana 9-10)
- Aula 21: MVC Pattern
- Aula 22: Repository Pattern
- Aula 23: Observer Pattern
- Aula 24: Strategy Pattern
- Aula 25: SOLID Principles

### **MÓDULO 6: TESTES E QUALIDADE** (Semana 11-12)
- Aula 26: Testes Unitários
- Aula 27: Mocking e Fixtures
- Aula 28: Testes de Integração
- Aula 29: Coverage e Qualidade
- Aula 30: Debugging Avançado

### **MÓDULO 7: MANIPULAÇÃO DE DADOS** (Semana 13-14)
- Aula 31: Pandas Básico
- Aula 32: Análise de Dados
- Aula 33: Excel com OpenPyXL
- Aula 34: Gráficos com Matplotlib
- Aula 35: Relatórios Automáticos

### **MÓDULO 8: DEPLOY E DISTRIBUIÇÃO** (Semana 15-16)
- Aula 36: Packaging com PyInstaller
- Aula 37: Executáveis e Instaladores
- Aula 38: Logs e Monitoramento
- Aula 39: Configuração e Ambientes
- Aula 40: Projeto Final

---

# 📚 MÓDULO 1: FUNDAMENTOS DE PYTHON

## 🎯 Aula 1: Introdução e Ambiente

### **Por que Python?**
Python é uma linguagem poderosa e versátil, perfeita para:
- **Desktop Applications** (como nosso sistema de lanchonete)
- **Web Development** (Django, Flask)
- **Data Science** (Pandas, NumPy)
- **Automation** (Scripts, bots)
- **AI/ML** (TensorFlow, PyTorch)

### **Configurando o Ambiente**

#### **1. Instalação do Python**
```bash
# Windows: Baixar do site oficial
# https://www.python.org/downloads/

# Verificar instalação
python --version
pip --version

# Linux/Mac
sudo apt install python3 python3-pip  # Ubuntu
brew install python3                   # Mac
```

#### **2. Editor Recomendado**
- **VS Code** com extensão Python
- **PyCharm** (IDE completa)
- **Sublime Text** (leve)

#### **3. Primeiro Programa**
```python
# hello_world.py
print("Bem-vindo ao Curso de Python!")
print("Vamos criar um sistema de lanchonete!")

# Executar
python hello_world.py
```

### **Exercício Prático:**
Crie um programa que mostra informações da sua lanchonete:
```python
# minha_lanchonete.py
nome_lanchonete = "Python Burger"
endereco = "Rua dos Programadores, 123"
telefone = "(11) 99999-9999"

print(f"🍔 {nome_lanchonete}")
print(f"📍 {endereco}")
print(f"📞 {telefone}")
print("Aberto de Segunda a Sábado!")
```

---

## 🎯 Aula 2: Variáveis e Tipos de Dados

### **Tipos Básicos em Python**

#### **1. Números**
```python
# Inteiros
quantidade_produtos = 50
idade_cliente = 25

# Decimais
preco_hamburger = 15.90
desconto = 0.10

# Operações matemáticas
total = preco_hamburger * quantidade_produtos
preco_com_desconto = preco_hamburger * (1 - desconto)

print(f"Total: R$ {total:.2f}")
print(f"Com desconto: R$ {preco_com_desconto:.2f}")
```

#### **2. Strings (Texto)**
```python
# Diferentes formas de criar strings
produto = "X-Burguer"
descricao = 'Hambúrguer com queijo e bacon'
observacoes = """
Cliente solicitou:
- Sem cebola
- Bacon extra
- Batata à parte
"""

# Manipulação de strings
produto_maiusculo = produto.upper()
produto_minusculo = produto.lower()
produto_formatado = produto.title()

# F-strings (formatação moderna)
cliente = "João Silva"
valor = 28.50
mensagem = f"Olá {cliente}, seu pedido de R$ {valor:.2f} está pronto!"

print(mensagem)
```

#### **3. Booleanos (Verdadeiro/Falso)**
```python
# Estados do sistema
lanchonete_aberta = True
tem_estoque = False
cliente_vip = True

# Operações lógicas
pode_vender = lanchonete_aberta and tem_estoque
precisa_reposicao = not tem_estoque
desconto_especial = cliente_vip or valor > 50

if pode_vender:
    print("Pode processar a venda!")
else:
    print("Não é possível vender no momento")
```

### **Exemplo Prático: Calculadora de Pedidos**
```python
# calculadora_pedido.py

# Dados do produto
produto = "X-Bacon"
preco_unitario = 18.50
quantidade = 2

# Dados do cliente
cliente = "Maria Santos"
eh_cliente_vip = True

# Cálculos
subtotal = preco_unitario * quantidade
desconto_vip = 0.10 if eh_cliente_vip else 0.0
valor_desconto = subtotal * desconto_vip
total_final = subtotal - valor_desconto

# Exibir resultado
print("=" * 40)
print("🍔 PEDIDO - PYTHON BURGER")
print("=" * 40)
print(f"Cliente: {cliente}")
print(f"Produto: {produto}")
print(f"Quantidade: {quantidade}")
print(f"Preço unitário: R$ {preco_unitario:.2f}")
print("-" * 40)
print(f"Subtotal: R$ {subtotal:.2f}")

if eh_cliente_vip:
    print(f"Desconto VIP (10%): -R$ {valor_desconto:.2f}")

print(f"TOTAL: R$ {total_final:.2f}")
print("=" * 40)
```

### **Exercícios:**
1. Crie um programa que calcula o troco de uma venda
2. Faça um sistema que verifica se um produto está em promoção
3. Desenvolva uma calculadora de comissão para vendedores

---

## 🎯 Aula 3: Estruturas de Controle

### **1. Condicionais (if, elif, else)**

#### **Sistema de Descontos**
```python
# sistema_desconto.py

valor_compra = float(input("Digite o valor da compra: R$ "))
eh_cliente_vip = input("Cliente VIP? (s/n): ").lower() == 's'
quantidade_itens = int(input("Quantos itens no pedido? "))

# Lógica de desconto
desconto = 0

if eh_cliente_vip:
    desconto = 0.15  # 15% para VIP
elif valor_compra >= 100:
    desconto = 0.10  # 10% para compras acima de R$ 100
elif quantidade_itens >= 5:
    desconto = 0.05  # 5% para pedidos com 5+ itens
else:
    desconto = 0     # Sem desconto

# Aplicar desconto
valor_desconto = valor_compra * desconto
valor_final = valor_compra - valor_desconto

# Mostrar resultado
print("\n" + "="*40)
print("🍔 RESUMO DO PEDIDO")
print("="*40)
print(f"Valor original: R$ {valor_compra:.2f}")

if desconto > 0:
    percentual = desconto * 100
    print(f"Desconto ({percentual:.0f}%): -R$ {valor_desconto:.2f}")
    print(f"Valor final: R$ {valor_final:.2f}")
    print(f"Você economizou: R$ {valor_desconto:.2f}")
else:
    print("Nenhum desconto aplicado")
    print(f"Valor final: R$ {valor_final:.2f}")
```

### **2. Loops (for e while)**

#### **Sistema de Cardápio**
```python
# cardapio_interativo.py

cardapio = {
    1: {"nome": "X-Burguer", "preco": 15.90},
    2: {"nome": "X-Bacon", "preco": 18.50},
    3: {"nome": "X-Tudo", "preco": 22.00},
    4: {"nome": "Batata Frita", "preco": 8.00},
    5: {"nome": "Refrigerante", "preco": 5.50}
}

carrinho = []
total_pedido = 0

print("🍔 BEM-VINDO À PYTHON BURGER!")
print("="*40)

while True:
    print("\n📋 CARDÁPIO:")
    print("-"*40)
    
    # Loop for para mostrar cardápio
    for codigo, item in cardapio.items():
        nome = item["nome"]
        preco = item["preco"]
        print(f"{codigo}. {nome} - R$ {preco:.2f}")
    
    print("0. Finalizar pedido")
    print("-"*40)
    
    # Input do usuário
    try:
        opcao = int(input("Digite o código do produto: "))
        
        if opcao == 0:
            break
        elif opcao in cardapio:
            produto = cardapio[opcao]
            quantidade = int(input(f"Quantos {produto['nome']}? "))
            
            # Adicionar ao carrinho
            item_carrinho = {
                "produto": produto["nome"],
                "preco_unitario": produto["preco"],
                "quantidade": quantidade,
                "subtotal": produto["preco"] * quantidade
            }
            
            carrinho.append(item_carrinho)
            total_pedido += item_carrinho["subtotal"]
            
            print(f"✅ {quantidade}x {produto['nome']} adicionado(s)!")
            
        else:
            print("❌ Código inválido!")
            
    except ValueError:
        print("❌ Digite apenas números!")

# Mostrar resumo do pedido
print("\n" + "="*50)
print("🧾 RESUMO DO PEDIDO")
print("="*50)

if carrinho:
    for item in carrinho:
        nome = item["produto"]
        qtd = item["quantidade"]
        preco = item["preco_unitario"]
        subtotal = item["subtotal"]
        print(f"{qtd}x {nome} - R$ {preco:.2f} = R$ {subtotal:.2f}")
    
    print("-"*50)
    print(f"TOTAL: R$ {total_pedido:.2f}")
else:
    print("Carrinho vazio!")

print("="*50)
print("Obrigado pela preferência! 🍔")
```

### **3. List Comprehensions (Avançado)**
```python
# Análise rápida de vendas
vendas_semana = [120.50, 89.30, 156.80, 200.00, 175.90, 134.20, 98.70]

# Filtrar vendas acima de R$ 150
vendas_altas = [venda for venda in vendas_semana if venda > 150]

# Calcular comissão (5% sobre cada venda)
comissoes = [venda * 0.05 for venda in vendas_semana]

# Classificar dias
classificacao = [
    "Excelente" if venda > 180 else
    "Bom" if venda > 120 else
    "Regular"
    for venda in vendas_semana
]

print("Vendas altas:", vendas_altas)
print("Comissões:", comissoes)
print("Classificação:", classificacao)
```

### **Exercícios:**
1. Crie um sistema de login com 3 tentativas
2. Faça um programa que lista produtos em estoque baixo
3. Desenvolva um menu interativo para gerenciar produtos

---

## 🎯 Aula 4: Funções Básicas

### **Por que usar Funções?**
Funções organizam código, evitam repetição e facilitam manutenção.

#### **Exemplo sem Funções (Ruim):**
```python
# Código repetitivo e desorganizado
preco1 = 15.90
quantidade1 = 2
desconto1 = 0.10
total1 = preco1 * quantidade1 * (1 - desconto1)

preco2 = 18.50
quantidade2 = 1
desconto2 = 0.15
total2 = preco2 * quantidade2 * (1 - desconto2)

preco3 = 22.00
quantidade3 = 3
desconto3 = 0.05
total3 = preco3 * quantidade3 * (1 - desconto3)
```

#### **Exemplo com Funções (Bom):**
```python
def calcular_total_item(preco, quantidade, desconto=0):
    """
    Calcula o total de um item com desconto opcional
    
    Args:
        preco (float): Preço unitário do produto
        quantidade (int): Quantidade do produto
        desconto (float): Percentual de desconto (0 a 1)
    
    Returns:
        float: Total calculado
    """
    subtotal = preco * quantidade
    valor_desconto = subtotal * desconto
    total = subtotal - valor_desconto
    return total

# Uso limpo e reutilizável
total1 = calcular_total_item(15.90, 2, 0.10)
total2 = calcular_total_item(18.50, 1, 0.15)
total3 = calcular_total_item(22.00, 3, 0.05)

print(f"Totais: R$ {total1:.2f}, R$ {total2:.2f}, R$ {total3:.2f}")
```

### **Tipos de Funções**

#### **1. Funções Básicas**
```python
def saudar_cliente(nome):
    """Função simples que retorna saudação"""
    return f"Olá {nome}, bem-vindo à Python Burger!"

def verificar_estoque(produto, quantidade_necessaria, estoque_atual):
    """Verifica se há estoque suficiente"""
    if estoque_atual >= quantidade_necessaria:
        return True, f"Estoque OK. Disponível: {estoque_atual}"
    else:
        falta = quantidade_necessaria - estoque_atual
        return False, f"Estoque insuficiente. Faltam: {falta}"

# Uso
mensagem = saudar_cliente("João")
print(mensagem)

tem_estoque, status = verificar_estoque("X-Burguer", 3, 5)
print(f"Tem estoque: {tem_estoque} - {status}")
```

#### **2. Funções com Parâmetros Opcionais**
```python
def processar_venda(cliente, produtos, metodo_pagamento="dinheiro", aplicar_desconto=False):
    """
    Processa uma venda com parâmetros opcionais
    """
    total = sum(item["preco"] * item["quantidade"] for item in produtos)
    
    # Aplicar desconto se solicitado
    if aplicar_desconto:
        if metodo_pagamento == "cartao":
            desconto = 0.05  # 5% no cartão
        else:
            desconto = 0.10  # 10% no dinheiro
        
        total = total * (1 - desconto)
    
    # Acréscimo para cartão
    if metodo_pagamento == "cartao" and not aplicar_desconto:
        total = total * 1.03  # 3% acréscimo
    
    return {
        "cliente": cliente,
        "total": total,
        "metodo": metodo_pagamento,
        "desconto_aplicado": aplicar_desconto
    }

# Diferentes formas de usar
produtos = [
    {"nome": "X-Burguer", "preco": 15.90, "quantidade": 2},
    {"nome": "Batata", "preco": 8.00, "quantidade": 1}
]

# Venda básica
venda1 = processar_venda("João", produtos)

# Venda com cartão e desconto
venda2 = processar_venda("Maria", produtos, "cartao", True)

# Venda com dinheiro e desconto
venda3 = processar_venda("Pedro", produtos, aplicar_desconto=True)

print(f"Venda 1: R$ {venda1['total']:.2f}")
print(f"Venda 2: R$ {venda2['total']:.2f}")
print(f"Venda 3: R$ {venda3['total']:.2f}")
```

#### **3. Funções que Retornam Múltiplos Valores**
```python
def analisar_vendas_dia(vendas):
    """
    Analisa vendas do dia e retorna estatísticas
    """
    if not vendas:
        return 0, 0, 0, 0
    
    total_vendas = len(vendas)
    total_faturamento = sum(venda["valor"] for venda in vendas)
    ticket_medio = total_faturamento / total_vendas
    maior_venda = max(venda["valor"] for venda in vendas)
    
    return total_vendas, total_faturamento, ticket_medio, maior_venda

# Dados de exemplo
vendas_hoje = [
    {"cliente": "João", "valor": 28.50},
    {"cliente": "Maria", "valor": 15.90},
    {"cliente": "Pedro", "valor": 42.00},
    {"cliente": "Ana", "valor": 18.50}
]

# Análise
qtd, faturamento, media, maior = analisar_vendas_dia(vendas_hoje)

print(f"Vendas hoje: {qtd}")
print(f"Faturamento: R$ {faturamento:.2f}")
print(f"Ticket médio: R$ {media:.2f}")
print(f"Maior venda: R$ {maior:.2f}")
```

### **Sistema Completo com Funções**
```python
# sistema_lanchonete_funcoes.py

def mostrar_menu():
    """Exibe o menu de opções"""
    print("\n🍔 SISTEMA PYTHON BURGER")
    print("="*30)
    print("1. Registrar venda")
    print("2. Consultar estoque")
    print("3. Relatório de vendas")
    print("4. Sair")
    print("="*30)

def obter_opcao():
    """Obtém opção do usuário com validação"""
    while True:
        try:
            opcao = int(input("Digite sua opção: "))
            if 1 <= opcao <= 4:
                return opcao
            else:
                print("❌ Opção inválida! Digite 1-4")
        except ValueError:
            print("❌ Digite apenas números!")

def registrar_venda():
    """Registra uma nova venda"""
    print("\n📝 REGISTRAR VENDA")
    cliente = input("Nome do cliente: ")
    produto = input("Produto: ")
    preco = float(input("Preço: R$ "))
    quantidade = int(input("Quantidade: "))
    
    total = preco * quantidade
    
    # Simular salvamento (em aulas futuras usaremos banco de dados)
    venda = {
        "cliente": cliente,
        "produto": produto,
        "quantidade": quantidade,
        "preco_unitario": preco,
        "total": total
    }
    
    print(f"✅ Venda registrada: {cliente} - R$ {total:.2f}")
    return venda

def consultar_estoque():
    """Simula consulta ao estoque"""
    print("\n📦 ESTOQUE ATUAL")
    estoque = {
        "X-Burguer": 15,
        "X-Bacon": 10,
        "Batata Frita": 25,
        "Refrigerante": 30
    }
    
    for produto, quantidade in estoque.items():
        status = "🟢 OK" if quantidade > 10 else "🟡 Baixo" if quantidade > 5 else "🔴 Crítico"
        print(f"{produto}: {quantidade} unidades {status}")

def relatorio_vendas():
    """Exibe relatório de vendas simulado"""
    print("\n📊 RELATÓRIO DE VENDAS")
    print("Funcionalidade será implementada com banco de dados!")

def main():
    """Função principal do sistema"""
    print("🚀 Sistema iniciado!")
    
    while True:
        mostrar_menu()
        opcao = obter_opcao()
        
        if opcao == 1:
            registrar_venda()
        elif opcao == 2:
            consultar_estoque()
        elif opcao == 3:
            relatorio_vendas()
        elif opcao == 4:
            print("👋 Até logo!")
            break

# Execução do programa
if __name__ == "__main__":
    main()
```

### **Exercícios:**
1. Crie uma função que calcula o tempo de preparo baseado nos produtos
2. Desenvolva uma função que gera códigos únicos para pedidos
3. Faça uma função que converte preços entre moedas

---

## 🎯 Aula 5: Estruturas de Dados

### **1. Listas - Coleções Ordenadas**

#### **Gerenciando Pedidos**
```python
# Lista de pedidos em andamento
pedidos_pendentes = []

def adicionar_pedido(cliente, produtos):
    """Adiciona novo pedido à fila"""
    pedido = {
        "id": len(pedidos_pendentes) + 1,
        "cliente": cliente,
        "produtos": produtos,
        "status": "pendente",
        "timestamp": "2025-08-27 10:30:00"
    }
    pedidos_pendentes.append(pedido)
    return pedido["id"]

def listar_pedidos():
    """Lista todos os pedidos pendentes"""
    print("\n📋 PEDIDOS PENDENTES:")
    for i, pedido in enumerate(pedidos_pendentes):
        print(f"{i+1}. {pedido['cliente']} - {len(pedido['produtos'])} itens")

def concluir_pedido(indice):
    """Marca pedido como concluído"""
    if 0 <= indice < len(pedidos_pendentes):
        pedido = pedidos_pendentes.pop(indice)  # Remove da lista
        pedido["status"] = "concluído"
        print(f"✅ Pedido de {pedido['cliente']} concluído!")
        return pedido
    else:
        print("❌ Pedido não encontrado!")

# Uso prático
id1 = adicionar_pedido("João", ["X-Burguer", "Batata"])
id2 = adicionar_pedido("Maria", ["X-Bacon", "Refrigerante"])

listar_pedidos()
concluir_pedido(0)  # Conclui primeiro pedido
listar_pedidos()
```

### **2. Dicionários - Dados Estruturados**

#### **Sistema de Produtos**
```python
# Base de dados de produtos
produtos_db = {
    "hamburgers": {
        "x_burguer": {
            "nome": "X-Burguer",
            "preco": 15.90,
            "ingredientes": ["pão", "carne", "queijo", "alface", "tomate"],
            "tempo_preparo": 8,
            "categoria": "hamburgers"
        },
        "x_bacon": {
            "nome": "X-Bacon",
            "preco": 18.50,
            "ingredientes": ["pão", "carne", "queijo", "bacon", "alface"],
            "tempo_preparo": 10,
            "categoria": "hamburgers"
        }
    },
    "acompanhamentos": {
        "batata_frita": {
            "nome": "Batata Frita",
            "preco": 8.00,
            "ingredientes": ["batata", "óleo", "sal"],
            "tempo_preparo": 5,
            "categoria": "acompanhamentos"
        }
    },
    "bebidas": {
        "refrigerante": {
            "nome": "Refrigerante",
            "preco": 5.50,
            "ingredientes": [],
            "tempo_preparo": 1,
            "categoria": "bebidas"
        }
    }
}

def buscar_produto(codigo):
    """Busca produto por código"""
    for categoria, produtos in produtos_db.items():
        if codigo in produtos:
            return produtos[codigo]
    return None

def listar_categoria(categoria):
    """Lista produtos de uma categoria"""
    if categoria in produtos_db:
        print(f"\n📋 {categoria.upper()}:")
        for codigo, produto in produtos_db[categoria].items():
            nome = produto["nome"]
            preco = produto["preco"]
            tempo = produto["tempo_preparo"]
            print(f"{codigo}: {nome} - R$ {preco:.2f} ({tempo}min)")
    else:
        print("❌ Categoria não encontrada!")

def calcular_tempo_total(codigos_produtos):
    """Calcula tempo total de preparo"""
    tempo_total = 0
    for codigo in codigos_produtos:
        produto = buscar_produto(codigo)
        if produto:
            tempo_total += produto["tempo_preparo"]
    return tempo_total

# Uso prático
listar_categoria("hamburgers")
produto = buscar_produto("x_bacon")
print(f"\nProduto encontrado: {produto['nome']}")

pedido = ["x_burguer", "batata_frita", "refrigerante"]
tempo = calcular_tempo_total(pedido)
print(f"Tempo total de preparo: {tempo} minutos")
```

### **3. Sets - Coleções Únicas**

#### **Controle de Ingredientes**
```python
def verificar_alergias(produto, alergias_cliente):
    """Verifica se produto contém alérgenos"""
    ingredientes = set(produto["ingredientes"])
    alergenos = set(alergias_cliente)
    
    conflitos = ingredientes.intersection(alergenos)
    
    if conflitos:
        return False, f"⚠️ Contém: {', '.join(conflitos)}"
    else:
        return True, "✅ Produto seguro"

def sugerir_substitutos(produto_original, alergia):
    """Sugere produtos sem determinado alérgeno"""
    substitutos = []
    
    for categoria, produtos in produtos_db.items():
        for codigo, produto in produtos.items():
            if alergia not in produto["ingredientes"]:
                substitutos.append(produto["nome"])
    
    return substitutos

# Uso prático
cliente_alergico = ["queijo", "bacon"]
produto_desejado = buscar_produto("x_bacon")

pode_comer, mensagem = verificar_alergias(produto_desejado, cliente_alergico)
print(f"X-Bacon para cliente alérgico: {mensagem}")

if not pode_comer:
    alternativas = sugerir_substitutos(produto_desejado, "queijo")
    print(f"Sugestões sem queijo: {alternativas}")
```

### **4. Tuplas - Dados Imutáveis**

#### **Coordenadas e Configurações**
```python
# Configurações fixas do sistema
CONFIG_SISTEMA = (
    ("MOEDA", "BRL"),
    ("TAXA_CARTAO", 0.03),
    ("DESCONTO_VIP", 0.15),
    ("LIMITE_DESCONTO", 100.00),
    ("HORARIO_FUNCIONAMENTO", (8, 22))  # 8h às 22h
)

def obter_config(chave):
    """Obtém configuração por chave"""
    for config_chave, valor in CONFIG_SISTEMA:
        if config_chave == chave:
            return valor
    return None

def esta_aberto(hora_atual):
    """Verifica se lanchonete está aberta"""
    abertura, fechamento = obter_config("HORARIO_FUNCIONAMENTO")
    return abertura <= hora_atual <= fechamento

# Coordenadas de entrega
enderecos_entrega = {
    "centro": (23.5505, -46.6333),
    "vila_madalena": (23.5364, -46.6881),
    "pinheiros": (23.5629, -46.7006)
}

def calcular_distancia(origem, destino):
    """Calcula distância simples entre dois pontos"""
    lat1, lon1 = origem
    lat2, lon2 = destino
    
    # Fórmula simplificada (para exemplo)
    distancia = ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5
    return round(distancia * 100, 2)  # Convertido para km

# Uso
print(f"Taxa do cartão: {obter_config('TAXA_CARTAO') * 100}%")
print(f"Aberto às 15h? {esta_aberto(15)}")

loja = (23.5505, -46.6333)
cliente = enderecos_entrega["vila_madalena"]
distancia = calcular_distancia(loja, cliente)
print(f"Distância para entrega: {distancia} km")
```

### **Sistema Integrado com Todas as Estruturas**
```python
# sistema_completo_estruturas.py

class SistemaLanchonete:
    def __init__(self):
        # Lista de vendas (histórico)
        self.vendas = []
        
        # Dicionário de estoque
        self.estoque = {
            "x_burguer": {"nome": "X-Burguer", "preco": 15.90, "quantidade": 20},
            "x_bacon": {"nome": "X-Bacon", "preco": 18.50, "quantidade": 15},
            "batata": {"nome": "Batata Frita", "preco": 8.00, "quantidade": 30},
            "refrigerante": {"nome": "Refrigerante", "preco": 5.50, "quantidade": 50}
        }
        
        # Set de clientes VIP
        self.clientes_vip = {"João Silva", "Maria Santos", "Pedro Costa"}
        
        # Tupla de configurações
        self.config = (
            ("desconto_vip", 0.15),
            ("taxa_entrega", 5.00),
            ("valor_minimo_entrega", 30.00)
        )
    
    def processar_venda(self, cliente, itens):
        """Processa uma venda completa"""
        # Verificar estoque
        for codigo, quantidade in itens.items():
            if codigo not in self.estoque:
                return False, f"Produto {codigo} não encontrado"
            
            if self.estoque[codigo]["quantidade"] < quantidade:
                return False, f"Estoque insuficiente para {codigo}"
        
        # Calcular total
        total = 0
        produtos_vendidos = []
        
        for codigo, quantidade in itens.items():
            produto = self.estoque[codigo]
            subtotal = produto["preco"] * quantidade
            total += subtotal
            
            produtos_vendidos.append({
                "produto": produto["nome"],
                "quantidade": quantidade,
                "preco_unitario": produto["preco"],
                "subtotal": subtotal
            })
            
            # Reduzir estoque
            self.estoque[codigo]["quantidade"] -= quantidade
        
        # Aplicar desconto VIP
        if cliente in self.clientes_vip:
            desconto = self.obter_config("desconto_vip")
            total = total * (1 - desconto)
        
        # Registrar venda
        venda = {
            "id": len(self.vendas) + 1,
            "cliente": cliente,
            "produtos": produtos_vendidos,
            "total": total,
            "timestamp": "2025-08-27 14:30:00"
        }
        
        self.vendas.append(venda)
        
        return True, venda
    
    def obter_config(self, chave):
        """Obtém configuração do sistema"""
        for config_chave, valor in self.config:
            if config_chave == chave:
                return valor
        return None
    
    def relatorio_estoque_baixo(self, limite=10):
        """Lista produtos com estoque baixo"""
        produtos_baixo = []
        
        for codigo, produto in self.estoque.items():
            if produto["quantidade"] <= limite:
                produtos_baixo.append({
                    "codigo": codigo,
                    "nome": produto["nome"],
                    "quantidade": produto["quantidade"]
                })
        
        return produtos_baixo
    
    def top_clientes(self, limite=3):
        """Top clientes por quantidade de compras"""
        contador_clientes = {}
        
        for venda in self.vendas:
            cliente = venda["cliente"]
            if cliente in contador_clientes:
                contador_clientes[cliente] += 1
            else:
                contador_clientes[cliente] = 1
        
        # Ordenar por quantidade de compras
        top = sorted(contador_clientes.items(), 
                    key=lambda x: x[1], 
                    reverse=True)[:limite]
        
        return top

# Exemplo de uso
sistema = SistemaLanchonete()

# Processar algumas vendas
pedido1 = {"x_burguer": 2, "batata": 1, "refrigerante": 2}
sucesso, resultado = sistema.processar_venda("João Silva", pedido1)

if sucesso:
    print(f"✅ Venda processada: R$ {resultado['total']:.2f}")
else:
    print(f"❌ Erro: {resultado}")

# Relatórios
estoque_baixo = sistema.relatorio_estoque_baixo()
print(f"\n📦 Produtos com estoque baixo: {len(estoque_baixo)}")

for produto in estoque_baixo:
    nome = produto["nome"]
    qtd = produto["quantidade"]
    print(f"- {nome}: {qtd} unidades")
```

### **Exercícios:**
1. Crie um sistema de fila de pedidos com prioridade
2. Desenvolva um sistema de combos usando dicionários aninhados
3. Implemente um sistema de pontos de fidelidade usando sets

---

# 📚 MÓDULO 2: PROGRAMAÇÃO ORIENTADA A OBJETOS

## 🎯 Aula 6: Classes e Objetos

### **Por que usar POO?**
Programação Orientada a Objetos organiza código em "objetos" que representam entidades do mundo real.

#### **Problema sem POO:**
```python
# Dados espalhados em variáveis globais
produto1_nome = "X-Burguer"
produto1_preco = 15.90
produto1_estoque = 20

produto2_nome = "X-Bacon"
produto2_preco = 18.50
produto2_estoque = 15

# Funções separadas
def calcular_total_produto1(quantidade):
    return produto1_preco * quantidade

def reduzir_estoque_produto1(quantidade):
    global produto1_estoque
    produto1_estoque -= quantidade
```

#### **Solução com POO:**
```python
class Produto:
    """Representa um produto da lanchonete"""
    
    def __init__(self, nome, preco, estoque_inicial=0):
        """Construtor - inicializa o objeto"""
        self.nome = nome
        self.preco = preco
        self.estoque = estoque_inicial
    
    def calcular_total(self, quantidade):
        """Calcula total para uma quantidade"""
        return self.preco * quantidade
    
    def reduzir_estoque(self, quantidade):
        """Reduz estoque se possível"""
        if self.estoque >= quantidade:
            self.estoque -= quantidade
            return True
        return False
    
    def adicionar_estoque(self, quantidade):
        """Adiciona itens ao estoque"""
        self.estoque += quantidade
    
    def tem_estoque(self, quantidade):
        """Verifica se há estoque suficiente"""
        return self.estoque >= quantidade
    
    def __str__(self):
        """Representação em string do produto"""
        return f"{self.nome} - R$ {self.preco:.2f} (Estoque: {self.estoque})"

# Criando objetos (instâncias)
x_burguer = Produto("X-Burguer", 15.90, 20)
x_bacon = Produto("X-Bacon", 18.50, 15)
batata = Produto("Batata Frita", 8.00, 30)

# Usando os objetos
print(x_burguer)  # Chama __str__
print(f"Total 3 X-Burguer: R$ {x_burguer.calcular_total(3):.2f}")

if x_burguer.tem_estoque(2):
    x_burguer.reduzir_estoque(2)
    print(f"Venda realizada! Estoque atual: {x_burguer.estoque}")
```

### **Classe Cliente**
```python
class Cliente:
    """Representa um cliente da lanchonete"""
    
    def __init__(self, nome, telefone, eh_vip=False):
        self.nome = nome
        self.telefone = telefone
        self.eh_vip = eh_vip
        self.historico_compras = []
        self.total_gasto = 0
    
    def adicionar_compra(self, valor):
        """Registra uma nova compra"""
        from datetime import datetime
        
        compra = {
            "valor": valor,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.historico_compras.append(compra)
        self.total_gasto += valor
        
        # Promover para VIP se gastou mais de R$ 500
        if self.total_gasto >= 500 and not self.eh_vip:
            self.eh_vip = True
            print(f"🎉 {self.nome} promovido para VIP!")
    
    def obter_desconto(self):
        """Retorna desconto baseado no status"""
        if self.eh_vip:
            return 0.15  # 15% para VIP
        elif self.total_gasto > 200:
            return 0.05  # 5% para clientes frequentes
        else:
            return 0     # Sem desconto
    
    def __str__(self):
        status = "VIP" if self.eh_vip else "Regular"
        return f"{self.nome} ({status}) - Total gasto: R$ {self.total_gasto:.2f}"

# Exemplo de uso
cliente1 = Cliente("João Silva", "(11) 99999-9999")
cliente2 = Cliente("Maria Santos", "(11) 88888-8888", True)

print(cliente1)
print(cliente2)

# Simular compras
cliente1.adicionar_compra(25.50)
cliente1.adicionar_compra(42.80)
print(f"Desconto para {cliente1.nome}: {cliente1.obter_desconto()*100}%")
```

### **Classe Venda (Relacionando Objetos)**
```python
class Venda:
    """Representa uma venda realizada"""
    
    contador_vendas = 0  # Variável de classe (compartilhada)
    
    def __init__(self, cliente):
        Venda.contador_vendas += 1
        self.id = Venda.contador_vendas
        self.cliente = cliente
        self.itens = []
        self.total = 0
        self.finalizada = False
        
        from datetime import datetime
        self.data_hora = datetime.now()
    
    def adicionar_item(self, produto, quantidade):
        """Adiciona item à venda"""
        if self.finalizada:
            print("❌ Venda já finalizada!")
            return False
        
        if not produto.tem_estoque(quantidade):
            print(f"❌ Estoque insuficiente para {produto.nome}")
            return False
        
        item = {
            "produto": produto,
            "quantidade": quantidade,
            "preco_unitario": produto.preco,
            "subtotal": produto.calcular_total(quantidade)
        }
        
        self.itens.append(item)
        self.total += item["subtotal"]
        
        print(f"✅ {quantidade}x {produto.nome} adicionado")
        return True
    
    def remover_item(self, indice):
        """Remove item da venda"""
        if 0 <= indice < len(self.itens):
            item = self.itens.pop(indice)
            self.total -= item["subtotal"]
            print(f"❌ {item['produto'].nome} removido")
        else:
            print("❌ Item não encontrado!")
    
    def aplicar_desconto(self):
        """Aplica desconto baseado no cliente"""
        desconto = self.cliente.obter_desconto()
        if desconto > 0:
            valor_desconto = self.total * desconto
            self.total -= valor_desconto
            print(f"💰 Desconto aplicado: R$ {valor_desconto:.2f}")
    
    def finalizar(self):
        """Finaliza a venda"""
        if not self.itens:
            print("❌ Venda sem itens!")
            return False
        
        # Aplicar desconto
        self.aplicar_desconto()
        
        # Reduzir estoque
        for item in self.itens:
            produto = item["produto"]
            quantidade = item["quantidade"]
            produto.reduzir_estoque(quantidade)
        
        # Registrar no histórico do cliente
        self.cliente.adicionar_compra(self.total)
        
        self.finalizada = True
        print(f"✅ Venda #{self.id} finalizada: R$ {self.total:.2f}")
        return True
    
    def __str__(self):
        status = "Finalizada" if self.finalizada else "Em andamento"
        return f"Venda #{self.id} - {self.cliente.nome} - {status} - R$ {self.total:.2f}"

# Sistema completo em ação
def demonstracao_poo():
    print("🍔 DEMONSTRAÇÃO DO SISTEMA POO")
    print("="*40)
    
    # Criar produtos
    x_burguer = Produto("X-Burguer", 15.90, 10)
    batata = Produto("Batata Frita", 8.00, 20)
    refrigerante = Produto("Refrigerante", 5.50, 30)
    
    # Criar cliente
    cliente = Cliente("João Silva", "(11) 99999-9999")
    
    # Criar venda
    venda = Venda(cliente)
    
    print(f"\n📝 Nova venda para: {cliente.nome}")
    print(f"Status inicial do X-Burguer: {x_burguer}")
    
    # Adicionar itens
    venda.adicionar_item(x_burguer, 2)
    venda.adicionar_item(batata, 1)
    venda.adicionar_item(refrigerante, 2)
    
    print(f"\n🛒 Carrinho atual:")
    for i, item in enumerate(venda.itens):
        produto = item["produto"]
        qtd = item["quantidade"]
        subtotal = item["subtotal"]
        print(f"{i+1}. {qtd}x {produto.nome} - R$ {subtotal:.2f}")
    
    print(f"\n💰 Total antes do desconto: R$ {venda.total:.2f}")
    
    # Finalizar venda
    venda.finalizar()
    
    print(f"\n📊 Status após a venda:")
    print(f"Cliente: {cliente}")
    print(f"X-Burguer: {x_burguer}")
    print(f"Total de vendas realizadas: {Venda.contador_vendas}")

# Executar demonstração
demonstracao_poo()
```

### **Exercícios:**
1. Crie uma classe `Funcionario` com salário e comissão
2. Desenvolva uma classe `Mesa` para controle de mesas do restaurante
3. Implemente uma classe `Combo` que agrupa produtos

---

## 🎯 Aula 7: Herança e Polimorfismo

### **Herança - Reutilizando Código**

#### **Classe Base (Pai)**
```python
class Pessoa:
    """Classe base para pessoas do sistema"""
    
    def __init__(self, nome, telefone, email):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        
        from datetime import datetime
        self.data_cadastro = datetime.now()
    
    def obter_contato(self):
        """Retorna informações de contato"""
        return f"{self.nome} - {self.telefone} - {self.email}"
    
    def atualizar_telefone(self, novo_telefone):
        """Atualiza telefone"""
        self.telefone = novo_telefone
        print(f"📞 Telefone atualizado para: {novo_telefone}")
    
    def __str__(self):
        return f"{self.nome} (Cadastro: {self.data_cadastro.strftime('%d/%m/%Y')})"
```

#### **Classes Filhas (Herdam de Pessoa)**
```python
class Cliente(Pessoa):
    """Cliente herda de Pessoa e adiciona funcionalidades específicas"""
    
    def __init__(self, nome, telefone, email):
        super().__init__(nome, telefone, email)  # Chama construtor do pai
        self.eh_vip = False
        self.total_gasto = 0
        self.pontos_fidelidade = 0
        self.historico_pedidos = []
    
    def adicionar_pontos(self, valor_compra):
        """Adiciona pontos baseado na compra"""
        pontos = int(valor_compra / 10)  # 1 ponto a cada R$ 10
        self.pontos_fidelidade += pontos
        print(f"⭐ +{pontos} pontos! Total: {self.pontos_fidelidade}")
    
    def promover_vip(self):
        """Promove cliente para VIP"""
        if self.total_gasto >= 500:
            self.eh_vip = True
            print(f"🎉 {self.nome} promovido para VIP!")
            return True
        return False
    
    def usar_pontos(self, pontos):
        """Usa pontos para desconto (100 pontos = R$ 10)"""
        if self.pontos_fidelidade >= pontos:
            self.pontos_fidelidade -= pontos
            desconto = pontos / 10  # 100 pontos = R$ 10
            return desconto
        return 0

class Funcionario(Pessoa):
    """Funcionário herda de Pessoa"""
    
    def __init__(self, nome, telefone, email, cargo, salario):
        super().__init__(nome, telefone, email)
        self.cargo = cargo
        self.salario = salario
        self.vendas_realizadas = []
        self.comissao_total = 0
    
    def registrar_venda(self, valor_venda):
        """Registra venda e calcula comissão"""
        from datetime import datetime
        
        venda = {
            "valor": valor_venda,
            "data": datetime.now(),
            "comissao": valor_venda * 0.02  # 2% de comissão
        }
        
        self.vendas_realizadas.append(venda)
        self.comissao_total += venda["comissao"]
        
        print(f"💰 Venda registrada: R$ {valor_venda:.2f} (Comissão: R$ {venda['comissao']:.2f})")
    
    def calcular_salario_total(self):
        """Calcula salário total com comissão"""
        return self.salario + self.comissao_total
    
    def relatorio_vendas_mes(self):
        """Relatório de vendas do mês atual"""
        from datetime import datetime
        
        mes_atual = datetime.now().month
        vendas_mes = [v for v in self.vendas_realizadas 
                     if v["data"].month == mes_atual]
        
        total_vendas = sum(v["valor"] for v in vendas_mes)
        total_comissao = sum(v["comissao"] for v in vendas_mes)
        
        return {
            "quantidade": len(vendas_mes),
            "total_vendas": total_vendas,
            "total_comissao": total_comissao
        }

class Fornecedor(Pessoa):
    """Fornecedor herda de Pessoa"""
    
    def __init__(self, nome, telefone, email, empresa, cnpj):
        super().__init__(nome, telefone, email)
        self.empresa = empresa
        self.cnpj = cnpj
        self.produtos_fornecidos = []
        self.pedidos_pendentes = []
    
    def adicionar_produto(self, produto, preco_fornecimento):
        """Adiciona produto ao catálogo do fornecedor"""
        item = {
            "produto": produto,
            "preco": preco_fornecimento,
            "disponivel": True
        }
        self.produtos_fornecidos.append(item)
    
    def criar_pedido(self, produtos_quantidades):
        """Cria pedido para o fornecedor"""
        from datetime import datetime, timedelta
        
        pedido = {
            "id": len(self.pedidos_pendentes) + 1,
            "produtos": produtos_quantidades,
            "data_pedido": datetime.now(),
            "data_entrega_prevista": datetime.now() + timedelta(days=3),
            "status": "pendente"
        }
        
        self.pedidos_pendentes.append(pedido)
        return pedido["id"]
```

### **Polimorfismo - Mesmo Método, Comportamentos Diferentes**

```python
class Produto:
    """Classe base para produtos"""
    
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco
    
    def calcular_preco_final(self, quantidade):
        """Método base - será sobrescrito pelas classes filhas"""
        return self.preco * quantidade
    
    def obter_informacoes(self):
        """Informações básicas do produto"""
        return f"{self.nome} - R$ {self.preco:.2f}"

class ProdutoSimples(Produto):
    """Produto sem variações"""
    
    def calcular_preco_final(self, quantidade):
        # Preço simples sem modificações
        return super().calcular_preco_final(quantidade)

class ProdutoComDesconto(Produto):
    """Produto com desconto em quantidade"""
    
    def __init__(self, nome, preco, quantidade_minima=5, desconto=0.1):
        super().__init__(nome, preco)
        self.quantidade_minima = quantidade_minima
        self.desconto = desconto
    
    def calcular_preco_final(self, quantidade):
        """Aplica desconto se quantidade >= mínima"""
        preco_base = super().calcular_preco_final(quantidade)
        
        if quantidade >= self.quantidade_minima:
            preco_com_desconto = preco_base * (1 - self.desconto)
            print(f"💰 Desconto de {self.desconto*100}% aplicado!")
            return preco_com_desconto
        
        return preco_base

class ProdutoPersonalizavel(Produto):
    """Produto com opcionais que afetam o preço"""
    
    def __init__(self, nome, preco_base):
        super().__init__(nome, preco_base)
        self.opcionais = []
    
    def adicionar_opcional(self, nome_opcional, preco_adicional):
        """Adiciona opcional ao produto"""
        self.opcionais.append({
            "nome": nome_opcional,
            "preco": preco_adicional
        })
    
    def calcular_preco_final(self, quantidade):
        """Calcula preço com opcionais"""
        preco_base = self.preco
        preco_opcionais = sum(opcional["preco"] for opcional in self.opcionais)
        preco_unitario = preco_base + preco_opcionais
        
        return preco_unitario * quantidade
    
    def obter_informacoes(self):
        """Informações incluindo opcionais"""
        info = super().obter_informacoes()
        
        if self.opcionais:
            opcionais_str = ", ".join(opt["nome"] for opt in self.opcionais)
            info += f" + {opcionais_str}"
        
        return info

# Demonstração do Polimorfismo
def demonstrar_polimorfismo():
    print("🔄 DEMONSTRAÇÃO DE POLIMORFISMO")
    print("="*40)
    
    # Criar diferentes tipos de produtos
    produtos = [
        ProdutoSimples("Refrigerante", 5.50),
        ProdutoComDesconto("Batata Frita", 8.00, quantidade_minima=3, desconto=0.15),
        ProdutoPersonalizavel("X-Burguer", 15.90)
    ]
    
    # Adicionar opcionais ao produto personalizável
    produtos[2].adicionar_opcional("Bacon Extra", 3.00)
    produtos[2].adicionar_opcional("Queijo Extra", 2.50)
    
    # Testar polimorfismo - mesmo método, comportamentos diferentes
    quantidade = 4
    
    print(f"\n🛒 Calculando preços para {quantidade} unidades:")
    print("-" * 40)
    
    for produto in produtos:
        # Polimorfismo: calcular_preco_final() tem comportamento diferente
        # dependendo do tipo do objeto
        preco = produto.calcular_preco_final(quantidade)
        info = produto.obter_informacoes()
        
        print(f"{info}")
        print(f"   {quantidade}x = R$ {preco:.2f}")
        print()

demonstrar_polimorfismo()
```

### **Sistema Avançado com Herança e Polimorfismo**

```python
class SistemaLanchonete:
    """Sistema principal usando herança e polimorfismo"""
    
    def __init__(self):
        self.pessoas = []  # Lista que pode conter Clientes, Funcionários, etc.
        self.produtos = []
        self.vendas = []
    
    def cadastrar_pessoa(self, pessoa):
        """Cadastra qualquer tipo de pessoa (polimorfismo)"""
        self.pessoas.append(pessoa)
        
        # Polimorfismo: __str__ funciona diferente para cada tipo
        print(f"✅ Cadastrado: {pessoa}")
    
    def buscar_pessoa_por_nome(self, nome):
        """Busca pessoa independente do tipo"""
        for pessoa in self.pessoas:
            if pessoa.nome.lower() == nome.lower():
                return pessoa
        return None
    
    def processar_venda(self, cliente_nome, itens_pedido):
        """Processa venda usando polimorfismo"""
        cliente = self.buscar_pessoa_por_nome(cliente_nome)
        
        if not cliente or not isinstance(cliente, Cliente):
            print("❌ Cliente não encontrado!")
            return False
        
        total = 0
        detalhes_venda = []
        
        print(f"\n🛒 Processando pedido para: {cliente.nome}")
        print("-" * 30)
        
        for item in itens_pedido:
            produto_nome = item["produto"]
            quantidade = item["quantidade"]
            
            # Buscar produto
            produto = self.buscar_produto_por_nome(produto_nome)
            if not produto:
                print(f"❌ Produto '{produto_nome}' não encontrado!")
                continue
            
            # Polimorfismo: calcular_preco_final funciona diferente
            # para cada tipo de produto
            preco_item = produto.calcular_preco_final(quantidade)
            total += preco_item
            
            detalhes_venda.append({
                "produto": produto,
                "quantidade": quantidade,
                "preco": preco_item
            })
            
            print(f"{quantidade}x {produto.obter_informacoes()} = R$ {preco_item:.2f}")
        
        # Aplicar desconto do cliente (se VIP)
        if hasattr(cliente, 'eh_vip') and cliente.eh_vip:
            desconto = total * 0.15
            total -= desconto
            print(f"💰 Desconto VIP: -R$ {desconto:.2f}")
        
        print(f"\n💰 TOTAL: R$ {total:.2f}")
        
        # Registrar venda
        cliente.total_gasto += total
        if hasattr(cliente, 'adicionar_pontos'):
            cliente.adicionar_pontos(total)
        
        return True
    
    def buscar_produto_por_nome(self, nome):
        """Busca produto por nome"""
        for produto in self.produtos:
            if produto.nome.lower() == nome.lower():
                return produto
        return None
    
    def relatorio_pessoas(self):
        """Relatório usando polimorfismo"""
        print("\n👥 RELATÓRIO DE PESSOAS CADASTRADAS")
        print("="*40)
        
        clientes = []
        funcionarios = []
        fornecedores = []
        
        # Separar por tipo
        for pessoa in self.pessoas:
            if isinstance(pessoa, Cliente):
                clientes.append(pessoa)
            elif isinstance(pessoa, Funcionario):
                funcionarios.append(pessoa)
            elif isinstance(pessoa, Fornecedor):
                fornecedores.append(pessoa)
        
        print(f"👤 Clientes: {len(clientes)}")
        for cliente in clientes:
            status = "VIP" if cliente.eh_vip else "Regular"
            print(f"   {cliente.nome} ({status}) - R$ {cliente.total_gasto:.2f}")
        
        print(f"\n👔 Funcionários: {len(funcionarios)}")
        for funcionario in funcionarios:
            salario_total = funcionario.calcular_salario_total()
            print(f"   {funcionario.nome} ({funcionario.cargo}) - R$ {salario_total:.2f}")
        
        print(f"\n🏢 Fornecedores: {len(fornecedores)}")
        for fornecedor in fornecedores:
            print(f"   {fornecedor.nome} ({fornecedor.empresa})")

# Exemplo completo
def exemplo_sistema_completo():
    sistema = SistemaLanchonete()
    
    # Cadastrar pessoas de diferentes tipos
    sistema.cadastrar_pessoa(Cliente("João Silva", "(11) 99999-9999", "joao@email.com"))
    sistema.cadastrar_pessoa(Funcionario("Maria Santos", "(11) 88888-8888", "maria@lanchonete.com", 
                                        "Atendente", 2000.00))
    sistema.cadastrar_pessoa(Fornecedor("Pedro Costa", "(11) 77777-7777", "pedro@fornecedor.com",
                                       "Carnes Premium", "12.345.678/0001-90"))
    
    # Cadastrar produtos de diferentes tipos
    sistema.produtos.append(ProdutoSimples("Refrigerante", 5.50))
    sistema.produtos.append(ProdutoComDesconto("Batata Frita", 8.00, 3, 0.15))
    
    produto_personalizado = ProdutoPersonalizavel("X-Burguer", 15.90)
    produto_personalizado.adicionar_opcional("Bacon Extra", 3.00)
    sistema.produtos.append(produto_personalizado)
    
    # Processar venda
    pedido = [
        {"produto": "X-Burguer", "quantidade": 1},
        {"produto": "Batata Frita", "quantidade": 3},
        {"produto": "Refrigerante", "quantidade": 2}
    ]
    
    sistema.processar_venda("João Silva", pedido)
    
    # Relatório
    sistema.relatorio_pessoas()

exemplo_sistema_completo()
```

### **Exercícios:**
1. Crie uma hierarquia de classes para diferentes tipos de pagamento
2. Implemente herança para diferentes tipos de promoções
3. Desenvolva um sistema de relatórios usando polimorfismo

---

Continuo com as próximas aulas? O curso está bem detalhado e prático!

## 🎯 Aula 8: Encapsulamento e Propriedades

### **Encapsulamento - Controlando Acesso aos Dados**

#### **Problema sem Encapsulamento:**
```python
class ContaBancaria:
    def __init__(self, titular, saldo_inicial):
        self.titular = titular
        self.saldo = saldo_inicial  # Público - qualquer um pode modificar

# Problema: acesso direto permite modificações indevidas
conta = ContaBancaria("João", 1000)
conta.saldo = -500  # ❌ Isso não deveria ser permitido!
```

#### **Solução com Encapsulamento:**
```python
class Produto:
    """Produto com controle de acesso aos dados"""
    
    def __init__(self, nome, preco, estoque_inicial=0):
        self._nome = nome           # Protegido (convenção Python)
        self._preco = preco
        self._estoque = estoque_inicial
        self.__codigo_interno = self._gerar_codigo()  # Privado
    
    def _gerar_codigo(self):
        """Método protegido - uso interno"""
        import random
        return f"PRD{random.randint(1000, 9999)}"
    
    # Propriedades (getters/setters)
    @property
    def nome(self):
        """Getter para nome"""
        return self._nome
    
    @nome.setter
    def nome(self, novo_nome):
        """Setter com validação"""
        if not novo_nome or len(novo_nome.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        self._nome = novo_nome.strip().title()
    
    @property
    def preco(self):
        """Getter para preço"""
        return self._preco
    
    @preco.setter
    def preco(self, novo_preco):
        """Setter com validação"""
        if novo_preco <= 0:
            raise ValueError("Preço deve ser positivo")
        
        # Log da mudança
        preco_antigo = self._preco
        self._preco = novo_preco
        print(f"💰 Preço alterado: R$ {preco_antigo:.2f} → R$ {novo_preco:.2f}")
    
    @property
    def estoque(self):
        """Getter para estoque"""
        return self._estoque
    
    @property
    def codigo_interno(self):
        """Código interno - somente leitura"""
        return self.__codigo_interno
    
    def adicionar_estoque(self, quantidade):
        """Método público para adicionar estoque"""
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        
        self._estoque += quantidade
        print(f"📦 Estoque atualizado: +{quantidade} = {self._estoque}")
    
    def reduzir_estoque(self, quantidade):
        """Método público para reduzir estoque"""
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        
        if quantidade > self._estoque:
            raise ValueError(f"Estoque insuficiente. Disponível: {self._estoque}")
        
        self._estoque -= quantidade
        print(f"📦 Estoque reduzido: -{quantidade} = {self._estoque}")
        
        # Alerta de estoque baixo
        if self._estoque <= 5:
            print(f"⚠️ ALERTA: Estoque baixo para {self._nome}!")
    
    def __str__(self):
        return f"{self._nome} (Código: {self.__codigo_interno}) - R$ {self._preco:.2f} - Estoque: {self._estoque}"

# Exemplo de uso
produto = Produto("X-Burguer", 15.90, 20)

# Acessar propriedades (getters)
print(f"Nome: {produto.nome}")
print(f"Preço: R$ {produto.preco:.2f}")
print(f"Estoque: {produto.estoque}")
print(f"Código: {produto.codigo_interno}")

# Modificar com validação (setters)
produto.nome = "X-Burguer Premium"
produto.preco = 18.90

# Métodos seguros para estoque
produto.adicionar_estoque(10)
produto.reduzir_estoque(25)  # Vai gerar alerta de estoque baixo

# Tentar acesso indevido - vai gerar erro
try:
    produto.nome = ""  # ❌ Nome muito curto
except ValueError as e:
    print(f"Erro: {e}")
```

### **Classe Cliente com Encapsulamento Avançado**
```python
class Cliente:
    """Cliente com controle de acesso e validações"""
    
    def __init__(self, nome, cpf, telefone, email):
        self._nome = nome
        self._cpf = self._validar_cpf(cpf)
        self._telefone = telefone
        self._email = email
        self._total_gasto = 0.0
        self._pontos_fidelidade = 0
        self._eh_vip = False
        self._historico_compras = []
        
        # Dados privados do sistema
        self.__limite_credito = 500.0
        self.__divida_atual = 0.0
    
    def _validar_cpf(self, cpf):
        """Validação básica de CPF"""
        # Remove caracteres não numéricos
        cpf_limpo = ''.join(c for c in cpf if c.isdigit())
        
        if len(cpf_limpo) != 11:
            raise ValueError("CPF deve ter 11 dígitos")
        
        return cpf_limpo
    
    def _validar_email(self, email):
        """Validação básica de email"""
        if '@' not in email or '.' not in email:
            raise ValueError("Email inválido")
        return email.lower()
    
    # Propriedades com validação
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, novo_nome):
        if not novo_nome or len(novo_nome.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        self._nome = novo_nome.strip().title()
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, novo_email):
        self._email = self._validar_email(novo_email)
    
    @property
    def telefone(self):
        return self._telefone
    
    @telefone.setter
    def telefone(self, novo_telefone):
        # Remove caracteres não numéricos
        telefone_limpo = ''.join(c for c in novo_telefone if c.isdigit())
        
        if len(telefone_limpo) < 10:
            raise ValueError("Telefone deve ter pelo menos 10 dígitos")
        
        self._telefone = novo_telefone
    
    # Propriedades somente leitura
    @property
    def cpf(self):
        """CPF mascarado para exibição"""
        return f"{self._cpf[:3]}.{self._cpf[3:6]}.{self._cpf[6:9]}-{self._cpf[9:]}"
    
    @property
    def total_gasto(self):
        return self._total_gasto
    
    @property
    def pontos_fidelidade(self):
        return self._pontos_fidelidade
    
    @property
    def eh_vip(self):
        return self._eh_vip
    
    @property
    def limite_credito_disponivel(self):
        """Limite disponível para compras fiado"""
        return self.__limite_credito - self.__divida_atual
    
    # Métodos públicos para operações controladas
    def registrar_compra(self, valor):
        """Registra uma compra no histórico"""
        if valor <= 0:
            raise ValueError("Valor da compra deve ser positivo")
        
        from datetime import datetime
        
        compra = {
            "valor": valor,
            "data": datetime.now(),
            "pontos_ganhos": int(valor / 10)
        }
        
        self._historico_compras.append(compra)
        self._total_gasto += valor
        self._pontos_fidelidade += compra["pontos_ganhos"]
        
        # Verificar promoção para VIP
        self._verificar_promocao_vip()
        
        print(f"✅ Compra registrada: R$ {valor:.2f}")
        print(f"   Pontos ganhos: {compra['pontos_ganhos']}")
        print(f"   Total gasto: R$ {self._total_gasto:.2f}")
    
    def usar_pontos(self, pontos):
        """Usa pontos para desconto"""
        if pontos <= 0:
            raise ValueError("Quantidade de pontos deve ser positiva")
        
        if pontos > self._pontos_fidelidade:
            raise ValueError(f"Pontos insuficientes. Disponível: {self._pontos_fidelidade}")
        
        self._pontos_fidelidade -= pontos
        desconto = pontos / 10  # 10 pontos = R$ 1
        
        print(f"💰 {pontos} pontos usados. Desconto: R$ {desconto:.2f}")
        return desconto
    
    def comprar_fiado(self, valor):
        """Permite compra fiado dentro do limite"""
        if valor > self.limite_credito_disponivel:
            raise ValueError(f"Limite insuficiente. Disponível: R$ {self.limite_credito_disponivel:.2f}")
        
        self.__divida_atual += valor
        self.registrar_compra(valor)
        
        print(f"🏪 Compra fiado: R$ {valor:.2f}")
        print(f"   Dívida atual: R$ {self.__divida_atual:.2f}")
    
    def pagar_divida(self, valor):
        """Paga parte ou total da dívida"""
        if valor <= 0:
            raise ValueError("Valor do pagamento deve ser positivo")
        
        if valor > self.__divida_atual:
            valor = self.__divida_atual
        
        self.__divida_atual -= valor
        print(f"💳 Pagamento efetuado: R$ {valor:.2f}")
        print(f"   Dívida restante: R$ {self.__divida_atual:.2f}")
    
    def _verificar_promocao_vip(self):
        """Método privado para verificar promoção VIP"""
        if not self._eh_vip and self._total_gasto >= 500:
            self._eh_vip = True
            self.__limite_credito = 1000.0  # Aumenta limite para VIP
            print(f"🎉 {self._nome} promovido para VIP!")
            print(f"   Novo limite de crédito: R$ {self.__limite_credito:.2f}")
    
    def obter_relatorio_completo(self):
        """Relatório completo do cliente"""
        return {
            "nome": self._nome,
            "cpf": self.cpf,
            "telefone": self._telefone,
            "email": self._email,
            "total_gasto": self._total_gasto,
            "pontos_fidelidade": self._pontos_fidelidade,
            "eh_vip": self._eh_vip,
            "limite_disponivel": self.limite_credito_disponivel,
            "divida_atual": self.__divida_atual,
            "total_compras": len(self._historico_compras)
        }
    
    def __str__(self):
        status = "VIP" if self._eh_vip else "Regular"
        return f"{self._nome} ({status}) - CPF: {self.cpf} - Total: R$ {self._total_gasto:.2f}"

# Demonstração completa
def demonstrar_encapsulamento():
    print("🔒 DEMONSTRAÇÃO DE ENCAPSULAMENTO")
    print("="*50)
    
    # Criar cliente com validações
    try:
        cliente = Cliente("João Silva", "12345678901", "(11) 99999-9999", "joao@email.com")
        print(f"✅ Cliente criado: {cliente}")
        
        # Modificações controladas
        cliente.nome = "joão da silva"  # Será formatado
        cliente.email = "JOAO.NOVO@EMAIL.COM"  # Será normalizado
        
        print(f"📝 Dados atualizados:")
        print(f"   Nome: {cliente.nome}")
        print(f"   Email: {cliente.email}")
        
        # Operações seguras
        cliente.registrar_compra(150.00)
        cliente.registrar_compra(200.00)
        cliente.registrar_compra(180.00)  # Total > 500, vira VIP
        
        # Usar pontos
        desconto = cliente.usar_pontos(50)
        
        # Compra fiado
        cliente.comprar_fiado(100.00)
        cliente.pagar_divida(50.00)
        
        # Relatório final
        relatorio = cliente.obter_relatorio_completo()
        print(f"\n📊 RELATÓRIO FINAL:")
        for chave, valor in relatorio.items():
            print(f"   {chave}: {valor}")
        
    except ValueError as e:
        print(f"❌ Erro de validação: {e}")

demonstrar_encapsulamento()
```

## 🎯 Aula 9: Métodos Especiais (Magic Methods)

### **Métodos Especiais Essenciais**

```python
class Produto:
    """Produto com métodos especiais para operações naturais"""
    
    def __init__(self, nome, preco, estoque=0):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque
    
    def __str__(self):
        """Representação amigável para usuários"""
        return f"{self.nome} - R$ {self.preco:.2f}"
    
    def __repr__(self):
        """Representação técnica para desenvolvedores"""
        return f"Produto('{self.nome}', {self.preco}, {self.estoque})"
    
    def __eq__(self, other):
        """Igualdade baseada no nome do produto"""
        if isinstance(other, Produto):
            return self.nome.lower() == other.nome.lower()
        return False
    
    def __lt__(self, other):
        """Comparação por preço (menor que)"""
        if isinstance(other, Produto):
            return self.preco < other.preco
        return NotImplemented
    
    def __le__(self, other):
        """Menor ou igual"""
        return self < other or self == other
    
    def __gt__(self, other):
        """Maior que"""
        if isinstance(other, Produto):
            return self.preco > other.preco
        return NotImplemented
    
    def __ge__(self, other):
        """Maior ou igual"""
        return self > other or self == other
    
    def __add__(self, other):
        """Soma de preços ou adição de estoque"""
        if isinstance(other, Produto):
            # Soma preços para criar combo
            return Produto(f"{self.nome} + {other.nome}", 
                          self.preco + other.preco)
        elif isinstance(other, (int, float)):
            # Adiciona valor ao preço
            return Produto(self.nome, self.preco + other, self.estoque)
        return NotImplemented
    
    def __mul__(self, other):
        """Multiplicação para calcular totais"""
        if isinstance(other, (int, float)):
            return self.preco * other
        return NotImplemented
    
    def __rmul__(self, other):
        """Multiplicação reversa (3 * produto)"""
        return self.__mul__(other)
    
    def __len__(self):
        """Tamanho = estoque disponível"""
        return self.estoque
    
    def __bool__(self):
        """Verdadeiro se tem estoque"""
        return self.estoque > 0
    
    def __contains__(self, item):
        """Verifica se palavra está no nome do produto"""
        return item.lower() in self.nome.lower()
    
    def __getitem__(self, key):
        """Acesso por índice ou chave"""
        if key == 0 or key == "nome":
            return self.nome
        elif key == 1 or key == "preco":
            return self.preco
        elif key == 2 or key == "estoque":
            return self.estoque
        else:
            raise KeyError(f"Chave '{key}' não encontrada")
    
    def __setitem__(self, key, value):
        """Modificação por índice ou chave"""
        if key == 0 or key == "nome":
            self.nome = value
        elif key == 1 or key == "preco":
            self.preco = value
        elif key == 2 or key == "estoque":
            self.estoque = value
        else:
            raise KeyError(f"Chave '{key}' não encontrada")

class Carrinho:
    """Carrinho de compras com métodos especiais"""
    
    def __init__(self):
        self.itens = []
    
    def __len__(self):
        """Quantidade de tipos de produtos no carrinho"""
        return len(self.itens)
    
    def __bool__(self):
        """Verdadeiro se tem itens"""
        return len(self.itens) > 0
    
    def __iter__(self):
        """Permite iterar sobre os itens"""
        return iter(self.itens)
    
    def __contains__(self, produto):
        """Verifica se produto está no carrinho"""
        for item in self.itens:
            if item["produto"] == produto:
                return True
        return False
    
    def __add__(self, item):
        """Adiciona item ao carrinho"""
        if isinstance(item, tuple) and len(item) == 2:
            produto, quantidade = item
            self.adicionar_item(produto, quantidade)
        return self
    
    def __iadd__(self, item):
        """Operador += para adicionar item"""
        return self.__add__(item)
    
    def __getitem__(self, index):
        """Acesso por índice"""
        return self.itens[index]
    
    def __delitem__(self, index):
        """Remove item por índice"""
        del self.itens[index]
    
    def adicionar_item(self, produto, quantidade):
        """Adiciona item ao carrinho"""
        # Verificar se produto já está no carrinho
        for item in self.itens:
            if item["produto"] == produto:
                item["quantidade"] += quantidade
                return
        
        # Adicionar novo item
        self.itens.append({
            "produto": produto,
            "quantidade": quantidade,
            "subtotal": produto.preco * quantidade
        })
    
    def calcular_total(self):
        """Calcula total do carrinho"""
        return sum(item["subtotal"] for item in self.itens)
    
    def __str__(self):
        """Representação do carrinho"""
        if not self.itens:
            return "Carrinho vazio"
        
        linhas = ["🛒 CARRINHO:"]
        for i, item in enumerate(self.itens, 1):
            produto = item["produto"]
            qtd = item["quantidade"]
            subtotal = item["subtotal"]
            linhas.append(f"{i}. {qtd}x {produto.nome} = R$ {subtotal:.2f}")
        
        total = self.calcular_total()
        linhas.append(f"TOTAL: R$ {total:.2f}")
        
        return "\n".join(linhas)

# Demonstração dos métodos especiais
def demonstrar_metodos_especiais():
    print("✨ DEMONSTRAÇÃO DE MÉTODOS ESPECIAIS")
    print("="*50)
    
    # Criar produtos
    x_burguer = Produto("X-Burguer", 15.90, 10)
    x_bacon = Produto("X-Bacon", 18.50, 8)
    batata = Produto("Batata Frita", 8.00, 15)
    
    print("📦 PRODUTOS CRIADOS:")
    print(f"str(x_burguer): {x_burguer}")  # __str__
    print(f"repr(x_burguer): {repr(x_burguer)}")  # __repr__
    
    # Comparações
    print(f"\n🔍 COMPARAÇÕES:")
    print(f"X-Burguer == X-Bacon: {x_burguer == x_bacon}")  # __eq__
    print(f"X-Burguer < X-Bacon: {x_burguer < x_bacon}")    # __lt__
    print(f"X-Burguer > Batata: {x_burguer > batata}")      # __gt__
    
    # Operações matemáticas
    print(f"\n🧮 OPERAÇÕES MATEMÁTICAS:")
    combo = x_burguer + batata  # __add__
    print(f"Combo criado: {combo}")
    
    total_2_burguers = 2 * x_burguer  # __rmul__
    print(f"2 X-Burguers: R$ {total_2_burguers:.2f}")
    
    # Propriedades especiais
    print(f"\n🔧 PROPRIEDADES ESPECIAIS:")
    print(f"Estoque X-Burguer (len): {len(x_burguer)}")     # __len__
    print(f"Tem estoque (bool): {bool(x_burguer)}")         # __bool__
    print(f"'Burguer' in X-Burguer: {'Burguer' in x_burguer}")  # __contains__
    
    # Acesso por índice/chave
    print(f"\n🔑 ACESSO POR ÍNDICE/CHAVE:")
    print(f"x_burguer[0] (nome): {x_burguer[0]}")           # __getitem__
    print(f"x_burguer['preco']: {x_burguer['preco']}")
    
    x_burguer["preco"] = 16.90  # __setitem__
    print(f"Preço alterado: {x_burguer}")
    
    # Carrinho com métodos especiais
    print(f"\n🛒 CARRINHO COM MÉTODOS ESPECIAIS:")
    carrinho = Carrinho()
    
    # Adicionar itens com +=
    carrinho += (x_burguer, 2)  # __iadd__
    carrinho += (batata, 1)
    
    print(f"Itens no carrinho (len): {len(carrinho)}")      # __len__
    print(f"Carrinho tem itens (bool): {bool(carrinho)}")   # __bool__
    print(f"X-Burguer in carrinho: {x_burguer in carrinho}")  # __contains__
    
    # Iterar sobre carrinho
    print(f"\n🔄 ITERAÇÃO SOBRE CARRINHO:")
    for item in carrinho:  # __iter__
        produto = item["produto"]
        qtd = item["quantidade"]
        print(f"- {qtd}x {produto.nome}")
    
    # Acesso por índice
    primeiro_item = carrinho[0]  # __getitem__
    print(f"\nPrimeiro item: {primeiro_item['produto'].nome}")
    
    print(f"\n{carrinho}")  # __str__

demonstrar_metodos_especiais()
```

## 🎯 Aula 10: Composição vs Herança

### **Composição - "Tem um" vs Herança - "É um"**

#### **Problema com Herança Excessiva:**
```python
# ❌ Hierarquia complexa e rígida
class Veiculo:
    pass

class VeiculoTerrestre(Veiculo):
    pass

class VeiculoAquatico(Veiculo):
    pass

class Carro(VeiculoTerrestre):
    pass

class CarroEletrico(Carro):
    pass

class CarroHibrido(Carro):
    pass

class CarroEsportivo(Carro):
    pass

class CarroEletricoEsportivo(CarroEletrico, CarroEsportivo):  # ❌ Herança múltipla complexa
    pass
```

#### **Solução com Composição:**
```python
# ✅ Componentes reutilizáveis
class Motor:
    """Componente: Motor"""
    def __init__(self, tipo, potencia):
        self.tipo = tipo
        self.potencia = potencia
    
    def ligar(self):
        return f"Motor {self.tipo} ligado ({self.potencia}CV)"

class Sistema Pagamento:
    """Componente: Sistema de pagamento"""
    def __init__(self, tipo):
        self.tipo = tipo
        self.taxa = {"dinheiro": 0, "cartao": 0.03, "pix": 0.01}[tipo]
    
    def processar(self, valor):
        valor_final = valor * (1 + self.taxa)
        return valor_final, self.taxa * valor

class SistemaEntrega:
    """Componente: Sistema de entrega"""
    def __init__(self, raio_km=10):
        self.raio_km = raio_km
        self.taxa_por_km = 2.00
    
    def calcular_taxa(self, distancia_km):
        if distancia_km > self.raio_km:
            return None  # Fora da área de entrega
        return distancia_km * self.taxa_por_km

class SistemaFidelidade:
    """Componente: Sistema de fidelidade"""
    def __init__(self):
        self.pontos_por_real = 1
        self.pontos_para_desconto = 100
    
    def calcular_pontos(self, valor_compra):
        return int(valor_compra * self.pontos_por_real)
    
    def calcular_desconto(self, pontos_usados):
        return pontos_usados / self.pontos_para_desconto

# Classe principal usando composição
class Lanchonete:
    """Lanchonete composta por vários sistemas"""
    
    def __init__(self, nome):
        self.nome = nome
        
        # Composição: "Tem um" sistema de pagamento
        self.sistema_pagamento = SistemaPagamento("cartao")
        
        # Composição: "Tem um" sistema de entrega
        self.sistema_entrega = SistemaEntrega(raio_km=15)
        
        # Composição: "Tem um" sistema de fidelidade
        self.sistema_fidelidade = SistemaFidelidade()
        
        # Estado interno
        self.pedidos = []
        self.clientes = {}
    
    def alterar_tipo_pagamento(self, novo_tipo):
        """Flexibilidade: pode trocar sistema de pagamento"""
        self.sistema_pagamento = SistemaPagamento(novo_tipo)
        print(f"💳 Sistema de pagamento alterado para: {novo_tipo}")
    
    def processar_pedido(self, cliente_id, valor, distancia_entrega=0):
        """Usa composição para processar pedido completo"""
        
        # Sistema de pagamento
        valor_final, taxa = self.sistema_pagamento.processar(valor)
        
        # Sistema de entrega
        taxa_entrega = 0
        if distancia_entrega > 0:
            taxa_entrega = self.sistema_entrega.calcular_taxa(distancia_entrega)
            if taxa_entrega is None:
                return {"erro": "Fora da área de entrega"}
            valor_final += taxa_entrega
        
        # Sistema de fidelidade
        pontos_ganhos = self.sistema_fidelidade.calcular_pontos(valor)
        
        # Registrar pedido
        pedido = {
            "cliente_id": cliente_id,
            "valor_original": valor,
            "taxa_pagamento": taxa,
            "taxa_entrega": taxa_entrega,
            "valor_final": valor_final,
            "pontos_ganhos": pontos_ganhos
        }
        
        self.pedidos.append(pedido)
        
        return pedido
    
    def usar_pontos_cliente(self, cliente_id, pontos):
        """Integração entre sistemas"""
        desconto = self.sistema_fidelidade.calcular_desconto(pontos)
        return desconto

# Exemplo de flexibilidade da composição
def demonstrar_composicao():
    print("🔧 DEMONSTRAÇÃO DE COMPOSIÇÃO")
    print("="*40)
    
    # Criar lanchonete
    lanchonete = Lanchonete("Python Burger")
    
    # Processar pedido com cartão
    print("💳 PEDIDO COM CARTÃO:")
    pedido1 = lanchonete.processar_pedido("cliente001", 50.00, distancia_entrega=5)
    
    print(f"   Valor original: R$ {pedido1['valor_original']:.2f}")
    print(f"   Taxa cartão: R$ {pedido1['taxa_pagamento']:.2f}")
    print(f"   Taxa entrega: R$ {pedido1['taxa_entrega']:.2f}")
    print(f"   Valor final: R$ {pedido1['valor_final']:.2f}")
    print(f"   Pontos ganhos: {pedido1['pontos_ganhos']}")
    
    # Mudar para PIX (flexibilidade da composição)
    lanchonete.alterar_tipo_pagamento("pix")
    
    print("\n📱 MESMO PEDIDO COM PIX:")
    pedido2 = lanchonete.processar_pedido("cliente002", 50.00, distancia_entrega=5)
    print(f"   Taxa PIX: R$ {pedido2['taxa_pagamento']:.2f}")
    print(f"   Valor final: R$ {pedido2['valor_final']:.2f}")
    
    # Testar fora da área
    print("\n🚫 PEDIDO FORA DA ÁREA:")
    pedido3 = lanchonete.processar_pedido("cliente003", 30.00, distancia_entrega=20)
    print(f"   Resultado: {pedido3}")

demonstrar_composicao()
```

### **Sistema Completo: Lanchonete com Composição**

```python
class ControladorEstoque:
    """Componente para controle de estoque"""
    
    def __init__(self):
        self.produtos = {}
        self.alertas_ativados = True
    
    def adicionar_produto(self, codigo, nome, preco, quantidade_inicial=0):
        self.produtos[codigo] = {
            "nome": nome,
            "preco": preco,
            "quantidade": quantidade_inicial,
            "reservado": 0
        }
    
    def verificar_disponibilidade(self, codigo, quantidade):
        if codigo not in self.produtos:
            return False, "Produto não encontrado"
        
        produto = self.produtos[codigo]
        disponivel = produto["quantidade"] - produto["reservado"]
        
        if disponivel >= quantidade:
            return True, f"Disponível: {disponivel}"
        else:
            return False, f"Insuficiente. Disponível: {disponivel}"
    
    def reservar_produto(self, codigo, quantidade):
        """Reserva produto para venda"""
        disponivel, msg = self.verificar_disponibilidade(codigo, quantidade)
        if disponivel:
            self.produtos[codigo]["reservado"] += quantidade
            return True
        return False
    
    def confirmar_venda(self, codigo, quantidade):
        """Confirma venda e reduz estoque"""
        produto = self.produtos[codigo]
        produto["quantidade"] -= quantidade
        produto["reservado"] -= quantidade
        
        if self.alertas_ativados and produto["quantidade"] <= 5:
            print(f"⚠️ ALERTA: Estoque baixo para {produto['nome']}")

class ProcessadorPedidos:
    """Componente para processar pedidos"""
    
    def __init__(self, controlador_estoque):
        self.estoque = controlador_estoque
        self.pedidos_pendentes = []
        self.proximo_id = 1
    
    def criar_pedido(self, cliente, itens):
        """Cria novo pedido"""
        pedido = {
            "id": self.proximo_id,
            "cliente": cliente,
            "itens": [],
            "status": "criando",
            "total": 0
        }
        
        self.proximo_id += 1
        
        # Validar e reservar itens
        for item in itens:
            codigo = item["codigo"]
            quantidade = item["quantidade"]
            
            disponivel, msg = self.estoque.verificar_disponibilidade(codigo, quantidade)
            if not disponivel:
                return False, f"Erro no item {codigo}: {msg}"
            
            # Reservar produto
            self.estoque.reservar_produto(codigo, quantidade)
            
            # Adicionar ao pedido
            produto = self.estoque.produtos[codigo]
            item_pedido = {
                "codigo": codigo,
                "nome": produto["nome"],
                "preco_unitario": produto["preco"],
                "quantidade": quantidade,
                "subtotal": produto["preco"] * quantidade
            }
            
            pedido["itens"].append(item_pedido)
            pedido["total"] += item_pedido["subtotal"]
        
        pedido["status"] = "pendente"
        self.pedidos_pendentes.append(pedido)
        
        return True, pedido
    
    def finalizar_pedido(self, pedido_id):
        """Finaliza pedido e confirma vendas"""
        pedido = self.buscar_pedido(pedido_id)
        if not pedido:
            return False, "Pedido não encontrado"
        
        # Confirmar vendas no estoque
        for item in pedido["itens"]:
            self.estoque.confirmar_venda(item["codigo"], item["quantidade"])
        
        pedido["status"] = "finalizado"
        self.pedidos_pendentes.remove(pedido)
        
        return True, pedido
    
    def buscar_pedido(self, pedido_id):
        for pedido in self.pedidos_pendentes:
            if pedido["id"] == pedido_id:
                return pedido
        return None

class GeradorRelatorios:
    """Componente para gerar relatórios"""
    
    def __init__(self, controlador_estoque, processador_pedidos):
        self.estoque = controlador_estoque
        self.pedidos = processador_pedidos
        self.vendas_finalizadas = []
    
    def relatorio_estoque(self):
        """Relatório de estoque atual"""
        print("\n📦 RELATÓRIO DE ESTOQUE")
        print("-" * 40)
        
        for codigo, produto in self.estoque.produtos.items():
            nome = produto["nome"]
            quantidade = produto["quantidade"]
            reservado = produto["reservado"]
            disponivel = quantidade - reservado
            
            status = "🟢" if disponivel > 10 else "🟡" if disponivel > 5 else "🔴"
            
            print(f"{codigo}: {nome}")
            print(f"   Total: {quantidade} | Reservado: {reservado} | Disponível: {disponivel} {status}")
    
    def relatorio_pedidos_pendentes(self):
        """Relatório de pedidos pendentes"""
        print("\n📋 PEDIDOS PENDENTES")
        print("-" * 40)
        
        if not self.pedidos.pedidos_pendentes:
            print("Nenhum pedido pendente")
            return
        
        for pedido in self.pedidos.pedidos_pendentes:
            print(f"Pedido #{pedido['id']} - {pedido['cliente']}")
            print(f"   Status: {pedido['status']} | Total: R$ {pedido['total']:.2f}")
            print(f"   Itens: {len(pedido['itens'])}")

# Sistema integrado usando composição
class SistemaLanchoneteCompleto:
    """Sistema principal que compõe todos os componentes"""
    
    def __init__(self, nome):
        self.nome = nome
        
        # Composição: integrar todos os componentes
        self.estoque = ControladorEstoque()
        self.processador = ProcessadorPedidos(self.estoque)
        self.relatorios = GeradorRelatorios(self.estoque, self.processador)
        
        # Inicializar dados de exemplo
        self._inicializar_produtos()
    
    def _inicializar_produtos(self):
        """Inicializa produtos de exemplo"""
        produtos_iniciais = [
            ("XB001", "X-Burguer", 15.90, 20),
            ("XB002", "X-Bacon", 18.50, 15),
            ("AC001", "Batata Frita", 8.00, 30),
            ("BE001", "Refrigerante", 5.50, 50),
            ("BE002", "Suco Natural", 7.00, 25)
        ]
        
        for codigo, nome, preco, quantidade in produtos_iniciais:
            self.estoque.adicionar_produto(codigo, nome, preco, quantidade)
    
    def processar_venda_completa(self, cliente, itens_pedido):
        """Fluxo completo de venda usando todos os componentes"""
        print(f"\n🔄 PROCESSANDO VENDA PARA: {cliente}")
        print("-" * 50)
        
        # 1. Criar pedido
        sucesso, resultado = self.processador.criar_pedido(cliente, itens_pedido)
        
        if not sucesso:
            print(f"❌ Erro ao criar pedido: {resultado}")
            return False
        
        pedido = resultado
        print(f"✅ Pedido #{pedido['id']} criado com sucesso!")
        
        # 2. Mostrar detalhes
        print(f"\n📋 DETALHES DO PEDIDO:")
        for item in pedido["itens"]:
            nome = item["nome"]
            qtd = item["quantidade"]
            preco = item["preco_unitario"]
            subtotal = item["subtotal"]
            print(f"   {qtd}x {nome} - R$ {preco:.2f} = R$ {subtotal:.2f}")
        
        print(f"\n💰 TOTAL: R$ {pedido['total']:.2f}")
        
        # 3. Confirmar venda
        sucesso, pedido_finalizado = self.processador.finalizar_pedido(pedido["id"])
        
        if sucesso:
            print(f"✅ Pedido #{pedido['id']} finalizado!")
            return True
        else:
            print(f"❌ Erro ao finalizar pedido!")
            return False
    
    def menu_principal(self):
        """Menu interativo do sistema"""
        while True:
            print(f"\n🍔 {self.nome.upper()}")
            print("=" * 40)
            print("1. Processar venda")
            print("2. Relatório de estoque")
            print("3. Pedidos pendentes")
            print("4. Sair")
            print("-" * 40)
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1":
                self._menu_venda()
            elif opcao == "2":
                self.relatorios.relatorio_estoque()
            elif opcao == "3":
                self.relatorios.relatorio_pedidos_pendentes()
            elif opcao == "4":
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida!")
    
    def _menu_venda(self):
        """Menu para processar venda"""
        cliente = input("Nome do cliente: ")
        
        itens = []
        print("\nAdicione itens (digite 'fim' para terminar):")
        
        while True:
            codigo = input("Código do produto (ou 'fim'): ")
            if codigo.lower() == 'fim':
                break
            
            try:
                quantidade = int(input("Quantidade: "))
                itens.append({"codigo": codigo, "quantidade": quantidade})
            except ValueError:
                print("❌ Quantidade inválida!")
        
        if itens:
            self.processar_venda_completa(cliente, itens)

# Demonstração final
def demonstracao_sistema_completo():
    print("🎯 SISTEMA COMPLETO COM COMPOSIÇÃO")
    print("=" * 50)
    
    # Criar sistema
    sistema = SistemaLanchoneteCompleto("Python Burger Premium")
    
    # Simular algumas vendas
    vendas_exemplo = [
        {
            "cliente": "João Silva",
            "itens": [
                {"codigo": "XB001", "quantidade": 2},
                {"codigo": "AC001", "quantidade": 1},
                {"codigo": "BE001", "quantidade": 2}
            ]
        },
        {
            "cliente": "Maria Santos",
            "itens": [
                {"codigo": "XB002", "quantidade": 1},
                {"codigo": "BE002", "quantidade": 1}
            ]
        }
    ]
    
    # Processar vendas
    for venda in vendas_exemplo:
        sistema.processar_venda_completa(venda["cliente"], venda["itens"])
    
    # Mostrar relatórios
    sistema.relatorios.relatorio_estoque()
    sistema.relatorios.relatorio_pedidos_pendentes()

demonstracao_sistema_completo()
```

### **Continuando o curso completo...**