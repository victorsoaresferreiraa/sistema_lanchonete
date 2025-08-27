#!/usr/bin/env python3
"""
Demonstração do Sistema de Licenciamento
Mostra como gerar e validar chaves de acesso
"""

import hashlib
import datetime
import base64

def gerar_chave_cliente(nome_cliente, dias_validade=365):
    """Gera chave única para um cliente específico"""
    
    # 1. Criar hash único do cliente
    cliente_hash = hashlib.sha256(nome_cliente.lower().encode()).hexdigest()[:8]
    
    # 2. Calcular data de expiração
    data_expiracao = datetime.datetime.now() + datetime.timedelta(days=dias_validade)
    data_str = data_expiracao.strftime("%Y%m%d")
    
    # 3. Combinar dados
    dados_licenca = f"{cliente_hash}-{data_str}"
    
    # 4. Codificar em base64
    dados_codificados = base64.b64encode(dados_licenca.encode()).decode()
    
    # 5. Criar chave final
    chave_final = f"LANCH-{dados_codificados}"
    
    return chave_final, data_expiracao

def validar_chave_cliente(chave_licenca, nome_cliente):
    """Valida se a chave pertence ao cliente e está válida"""
    
    try:
        # 1. Verificar formato
        if not chave_licenca.startswith("LANCH-"):
            return False, "Formato de chave inválido"
        
        # 2. Decodificar dados
        parte_codificada = chave_licenca.replace("LANCH-", "")
        dados_decodificados = base64.b64decode(parte_codificada).decode()
        
        # 3. Separar hash e data
        hash_cliente, data_str = dados_decodificados.split("-")
        
        # 4. Verificar se o hash bate com o cliente
        hash_esperado = hashlib.sha256(nome_cliente.lower().encode()).hexdigest()[:8]
        if hash_cliente != hash_esperado:
            return False, "Chave não pertence a este cliente"
        
        # 5. Verificar se não expirou
        data_expiracao = datetime.datetime.strptime(data_str, "%Y%m%d")
        if datetime.datetime.now() > data_expiracao:
            return False, "Licença expirada"
        
        # 6. Calcular dias restantes
        dias_restantes = (data_expiracao - datetime.datetime.now()).days
        
        return True, f"Licença válida por mais {dias_restantes} dias"
        
    except Exception as e:
        return False, f"Erro na validação: {e}"

def demonstracao_completa():
    """Demonstra todo o processo de licenciamento"""
    
    print("🔐 DEMONSTRAÇÃO DO SISTEMA DE LICENCIAMENTO")
    print("=" * 60)
    
    # Exemplos de clientes
    clientes = [
        ("Lanchonete do João", 365),
        ("Pizzaria Bella Vista", 180),
        ("Café Central", 90),
        ("Restaurante Sabor", 30)
    ]
    
    print("\n📋 GERANDO CHAVES PARA CLIENTES:")
    print("-" * 40)
    
    chaves_geradas = {}
    
    for nome_cliente, dias in clientes:
        chave, data_exp = gerar_chave_cliente(nome_cliente, dias)
        chaves_geradas[nome_cliente] = chave
        
        print(f"👤 Cliente: {nome_cliente}")
        print(f"🔑 Chave: {chave}")
        print(f"📅 Válida até: {data_exp.strftime('%d/%m/%Y')}")
        print(f"⏰ Dias: {dias}")
        print()
    
    print("\n🔍 TESTANDO VALIDAÇÕES:")
    print("-" * 40)
    
    # Testar chaves válidas
    for nome_cliente, chave in chaves_geradas.items():
        valida, mensagem = validar_chave_cliente(chave, nome_cliente)
        status = "✅" if valida else "❌"
        print(f"{status} {nome_cliente}: {mensagem}")
    
    # Testar chave em cliente errado
    print(f"\n🚫 TESTE DE SEGURANÇA:")
    chave_joao = chaves_geradas["Lanchonete do João"]
    valida, mensagem = validar_chave_cliente(chave_joao, "Pizzaria Bella Vista")
    print(f"❌ Usando chave do João na Pizzaria: {mensagem}")
    
    # Testar chave inválida
    valida, mensagem = validar_chave_cliente("CHAVE-FALSA-123", "Qualquer Cliente")
    print(f"❌ Chave falsa: {mensagem}")

def simular_uso_diario():
    """Simula como seria usado no dia a dia"""
    
    print("\n💼 SIMULAÇÃO DE USO COMERCIAL")
    print("=" * 40)
    
    # Cenário: Venda para novo cliente
    print("📞 CLIENTE LIGOU INTERESSADO:")
    cliente = "Hamburgeria Top Burger"
    
    # Gerar chave para 30 dias (período de teste)
    chave_teste, data_exp = gerar_chave_cliente(cliente, 30)
    
    print(f"👤 Cliente: {cliente}")
    print(f"🎯 Período: 30 dias (teste)")
    print(f"🔑 Chave gerada: {chave_teste}")
    print(f"📅 Válida até: {data_exp.strftime('%d/%m/%Y')}")
    
    # Simular validação no sistema do cliente
    print(f"\n🖥️  CLIENTE INSTALOU O SISTEMA:")
    valida, mensagem = validar_chave_cliente(chave_teste, cliente)
    print(f"✅ Status: {mensagem}")
    
    # Cliente decidiu comprar licença anual
    print(f"\n💰 CLIENTE COMPROU LICENÇA ANUAL:")
    chave_anual, data_exp_anual = gerar_chave_cliente(cliente, 365)
    print(f"🔑 Nova chave: {chave_anual}")
    print(f"📅 Válida até: {data_exp_anual.strftime('%d/%m/%Y')}")
    
    valida, mensagem = validar_chave_cliente(chave_anual, cliente)
    print(f"✅ Status: {mensagem}")

def calcular_potencial_comercial():
    """Calcula potencial de faturamento"""
    
    print("\n📊 POTENCIAL COMERCIAL")
    print("=" * 30)
    
    cenarios = {
        "Conservador": {"clientes": 50, "preco_medio": 300},
        "Realista": {"clientes": 200, "preco_medio": 450},
        "Otimista": {"clientes": 500, "preco_medio": 600}
    }
    
    for nome, dados in cenarios.items():
        faturamento_mensal = dados["clientes"] * dados["preco_medio"]
        faturamento_anual = faturamento_mensal * 12
        
        print(f"{nome}:")
        print(f"  👥 Clientes: {dados['clientes']}")
        print(f"  💰 Preço médio: R$ {dados['preco_medio']}")
        print(f"  📅 Mensal: R$ {faturamento_mensal:,}")
        print(f"  🎯 Anual: R$ {faturamento_anual:,}")
        print()

def main():
    """Função principal"""
    demonstracao_completa()
    simular_uso_diario()
    calcular_potencial_comercial()
    
    print("\n🎯 COMO IMPLEMENTAR:")
    print("1. Integrar validação no início do main_funcional.py")
    print("2. Criar site para gerar chaves automaticamente")
    print("3. Sistema de pagamento online")
    print("4. Suporte via WhatsApp/email")
    print("5. Renovação automática de licenças")

if __name__ == "__main__":
    main()