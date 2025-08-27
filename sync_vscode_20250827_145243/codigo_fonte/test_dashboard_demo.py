#!/usr/bin/env python3
"""
Demonstração do Dashboard Financeiro
Gera dados de exemplo e cria relatório Excel demonstrativo
"""

import os
import sys
from datetime import datetime, timedelta
import pandas as pd

# Configurar path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.estoque.database import DatabaseManager
    from src.relatorios.dashboard import DashboardWindow
    
    print("📊 DEMONSTRAÇÃO DO DASHBOARD FINANCEIRO")
    print("=" * 50)
    
    # Inicializar database
    db = DatabaseManager()
    
    # Criar dados de exemplo para demonstração
    print("📋 Criando dados de exemplo...")
    
    # Produtos de exemplo
    produtos_exemplo = [
        ("Hambúrguer Clássico", 25, 15.90, "Lanches"),
        ("Batata Frita", 30, 8.50, "Acompanhamentos"), 
        ("Refrigerante Cola", 50, 4.00, "Bebidas"),
        ("Água Mineral", 40, 2.50, "Bebidas"),
        ("X-Bacon", 15, 18.90, "Lanches"),
        ("Suco Natural", 20, 6.00, "Bebidas"),
        ("Pastel de Queijo", 35, 7.50, "Salgados"),
        ("Coxinha", 40, 5.00, "Salgados")
    ]
    
    # Inserir produtos se não existirem
    for produto, qtd, preco, categoria in produtos_exemplo:
        try:
            db.adicionar_produto(produto, qtd, preco, categoria)
        except:
            pass  # Produto já existe
    
    # Criar vendas de exemplo para os últimos 7 dias
    print("💰 Gerando histórico de vendas...")
    vendas_exemplo = []
    
    for i in range(7):
        data_venda = datetime.now() - timedelta(days=i)
        data_str = data_venda.strftime("%d/%m/%Y %H:%M:%S")
        
        # Diferentes padrões por dia
        if i == 0:  # Hoje
            vendas_dia = [
                ("Hambúrguer Clássico", 3, 15.90),
                ("Batata Frita", 2, 8.50),
                ("Refrigerante Cola", 5, 4.00),
                ("X-Bacon", 1, 18.90)
            ]
        elif i == 1:  # Ontem
            vendas_dia = [
                ("Hambúrguer Clássico", 4, 15.90),
                ("Batata Frita", 3, 8.50),
                ("Refrigerante Cola", 6, 4.00),
                ("Pastel de Queijo", 2, 7.50),
                ("Coxinha", 3, 5.00)
            ]
        elif i == 2:  # Anteontem
            vendas_dia = [
                ("X-Bacon", 2, 18.90),
                ("Suco Natural", 3, 6.00),
                ("Água Mineral", 4, 2.50),
                ("Hambúrguer Clássico", 2, 15.90)
            ]
        else:  # Dias anteriores
            vendas_dia = [
                ("Hambúrguer Clássico", 2, 15.90),
                ("Refrigerante Cola", 3, 4.00),
                ("Batata Frita", 1, 8.50)
            ]
        
        for produto, qtd, preco in vendas_dia:
            vendas_exemplo.append((produto, qtd, preco, data_str))
    
    # Inserir vendas no banco
    for produto, qtd, preco, data in vendas_exemplo:
        db.cursor.execute("""
            INSERT INTO historico_vendas 
            (produto, quantidade, preco_unitario, total, data_venda, vendedor, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (produto, qtd, preco, qtd * preco, data, "Sistema Demo", "Venda demonstrativa"))
    
    db.conn.commit()
    
    print("✅ Dados de exemplo criados!")
    print("\n📊 ANÁLISE DOS DADOS GERADOS:")
    print("-" * 40)
    
    # Mostrar estatísticas
    hoje = datetime.now().strftime("%d/%m/%Y")
    receita_hoje = db.obter_receita_periodo(hoje, hoje)
    vendas_hoje = db.contar_vendas_periodo(hoje, hoje)
    produto_top = db.obter_produto_mais_vendido()
    estoque_total = db.obter_valor_total_estoque()
    produtos_baixo = db.contar_produtos_estoque_baixo(5)
    
    print(f"💰 Receita Hoje: R$ {receita_hoje:.2f}")
    print(f"🛒 Vendas Hoje: {vendas_hoje}")
    print(f"🏆 Produto Top: {produto_top}")
    print(f"🎯 Ticket Médio: R$ {(receita_hoje/vendas_hoje if vendas_hoje > 0 else 0):.2f}")
    print(f"📦 Valor Estoque: R$ {estoque_total:.2f}")
    print(f"⚠️ Estoque Baixo: {produtos_baixo} produtos")
    
    # Criar relatório demonstrativo
    print(f"\n📄 Gerando relatório demonstrativo...")
    
    # Criar pasta de demonstração
    os.makedirs("data/demo", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/demo/dashboard_demonstracao_{timestamp}.xlsx"
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        
        # Aba 1: Métricas Principais
        metricas_data = {
            'Métrica': [
                'Receita Hoje', 'Vendas Hoje', 'Produto Mais Vendido',
                'Ticket Médio', 'Valor Estoque Total', 'Produtos Estoque Baixo'
            ],
            'Valor': [
                f'R$ {receita_hoje:.2f}',
                vendas_hoje,
                produto_top,
                f'R$ {(receita_hoje/vendas_hoje if vendas_hoje > 0 else 0):.2f}',
                f'R$ {estoque_total:.2f}',
                produtos_baixo
            ],
            'Descrição': [
                'Faturamento do dia atual',
                'Número de transações hoje',
                'Produto líder em vendas',
                'Valor médio por venda',
                'Patrimônio em estoque',
                'Produtos precisando reposição'
            ]
        }
        
        df_metricas = pd.DataFrame(metricas_data)
        df_metricas.to_excel(writer, sheet_name='Métricas Dashboard', index=False)
        
        # Aba 2: Vendas por Período
        dados_vendas = db.obter_vendas_ultimos_dias(7)
        if dados_vendas:
            df_vendas = pd.DataFrame(dados_vendas, columns=['Data', 'Receita', 'Quantidade'])
            df_vendas.to_excel(writer, sheet_name='Vendas 7 Dias', index=False)
        
        # Aba 3: Top Produtos
        produtos_performance = db.obter_top_produtos_receita(10)
        if produtos_performance:
            df_produtos = pd.DataFrame(produtos_performance, columns=['Produto', 'Receita Total', 'Quantidade Total'])
            df_produtos.to_excel(writer, sheet_name='Performance Produtos', index=False)
        
        # Aba 4: Estoque Completo
        estoque_completo = db.listar_estoque_completo()
        if estoque_completo:
            df_estoque = pd.DataFrame(
                estoque_completo,
                columns=['Produto', 'Quantidade', 'Preço', 'Categoria', 'Código', 'Cadastro', 'Atualização']
            )
            df_estoque.to_excel(writer, sheet_name='Situação Estoque', index=False)
    
    print(f"✅ Relatório demonstrativo salvo em: {filename}")
    
    print("\n🎯 FUNCIONALIDADES IMPLEMENTADAS:")
    print("-" * 45)
    print("✅ Interface visual do dashboard")
    print("✅ 8 métricas financeiras principais")
    print("✅ 4 tipos de gráficos analíticos")
    print("✅ Sistema de alertas inteligentes")
    print("✅ Exportação Excel automática")
    print("✅ Guia de usuário interativo")
    print("✅ Integração com sistema principal")
    print("✅ Métodos de análise no banco")
    
    print("\n🚀 DASHBOARD PRONTO PARA USO!")
    print("Para acessar no sistema principal, clique no botão:")
    print("'📊 Dashboard Executivo'")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("Certifique-se de que todas as dependências estão instaladas:")
    print("- pandas")
    print("- openpyxl")
    print("- matplotlib")
    
except Exception as e:
    print(f"❌ Erro na demonstração: {e}")
    print("Verifique se o banco de dados está acessível.")