#!/usr/bin/env python3
"""
Teste simples do sistema - Interface console
Para verificar funcionalidades básicas
"""

import sys
import os
import sqlite3
from datetime import datetime

def testar_banco():
    """Testar conexão e estrutura do banco"""
    print("🔧 Testando banco de dados...")
    
    # Criar diretório se não existir
    os.makedirs("data", exist_ok=True)
    
    try:
        with sqlite3.connect("data/banco.db") as conn:
            cursor = conn.cursor()
            
            # Criar tabela de teste
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS estoque (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto TEXT NOT NULL,
                    quantidade INTEGER NOT NULL DEFAULT 0,
                    preco REAL DEFAULT 0.0,
                    categoria TEXT DEFAULT 'Geral',
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Teste de inserção
            cursor.execute("""
                INSERT OR IGNORE INTO estoque (produto, quantidade, preco, categoria) 
                VALUES (?, ?, ?, ?)
            """, ("Refrigerante", 10, 3.50, "Bebidas"))
            
            # Teste de consulta
            cursor.execute("SELECT * FROM estoque WHERE produto = 'Refrigerante'")
            resultado = cursor.fetchone()
            
            if resultado:
                print("✅ Banco funcionando - Produto encontrado:", resultado)
                return True
            else:
                print("❌ Erro no banco - Produto não encontrado")
                return False
                
    except Exception as e:
        print(f"❌ Erro no banco: {e}")
        return False

def testar_interface_console():
    """Interface console simples para testes"""
    print("\n🍔 Sistema de Lanchonete - Teste Console")
    print("="*50)
    
    while True:
        print("\nOpções:")
        print("1. Adicionar produto")
        print("2. Listar produtos")
        print("3. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            adicionar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            print("👋 Sistema finalizado!")
            break
        else:
            print("❌ Opção inválida!")

def adicionar_produto():
    """Adicionar produto via console"""
    print("\n📦 Adicionar Produto")
    
    produto = input("Nome do produto: ")
    if not produto:
        print("❌ Nome obrigatório!")
        return
    
    try:
        quantidade = int(input("Quantidade: "))
        preco = float(input("Preço: R$ "))
        categoria = input("Categoria (ou Enter para 'Geral'): ") or "Geral"
        
        with sqlite3.connect("data/banco.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO estoque (produto, quantidade, preco, categoria) 
                VALUES (?, ?, ?, ?)
            """, (produto, quantidade, preco, categoria))
            
        print(f"✅ Produto '{produto}' adicionado com sucesso!")
        
    except ValueError:
        print("❌ Erro: Valores numéricos inválidos!")
    except Exception as e:
        print(f"❌ Erro ao adicionar: {e}")

def listar_produtos():
    """Listar produtos do estoque"""
    print("\n📋 Lista de Produtos")
    
    try:
        with sqlite3.connect("data/banco.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estoque ORDER BY produto")
            produtos = cursor.fetchall()
            
        if produtos:
            print("\nID | Produto | Qtd | Preço | Categoria")
            print("-" * 50)
            for p in produtos:
                print(f"{p[0]} | {p[1]} | {p[2]} | R$ {p[3]:.2f} | {p[4]}")
        else:
            print("📦 Nenhum produto cadastrado")
            
    except Exception as e:
        print(f"❌ Erro ao listar: {e}")

def main():
    """Função principal"""
    print("🚀 Iniciando testes do sistema...")
    
    # Testar banco primeiro
    if testar_banco():
        print("✅ Banco OK - Iniciando interface")
        testar_interface_console()
    else:
        print("❌ Falha no banco - Verifique a instalação")
        sys.exit(1)

if __name__ == "__main__":
    main()