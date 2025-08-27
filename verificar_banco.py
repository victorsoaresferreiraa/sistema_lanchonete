#!/usr/bin/env python3
"""
Script para verificar e corrigir estrutura do banco de dados
"""

import sqlite3
import os

def verificar_estrutura_banco():
    """Verificar e corrigir estrutura do banco"""
    print("🔍 Verificando estrutura do banco de dados...")
    
    db_path = "data/banco.db"
    
    if not os.path.exists("data"):
        os.makedirs("data")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Verificar estrutura atual
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas_existentes = [row[0] for row in cursor.fetchall()]
    print(f"📋 Tabelas existentes: {tabelas_existentes}")
    
    # Verificar estrutura da tabela historico_vendas
    if 'historico_vendas' in tabelas_existentes:
        cursor.execute("PRAGMA table_info(historico_vendas)")
        colunas = cursor.fetchall()
        print(f"📊 Colunas historico_vendas: {[col[1] for col in colunas]}")
        
        # Verificar se coluna cliente existe
        tem_cliente = any(col[1] == 'cliente' for col in colunas)
        if not tem_cliente:
            print("⚠️ Coluna 'cliente' não encontrada. Adicionando...")
            try:
                cursor.execute("ALTER TABLE historico_vendas ADD COLUMN cliente TEXT")
                print("✅ Coluna 'cliente' adicionada")
            except Exception as e:
                print(f"❌ Erro ao adicionar coluna: {e}")
    
    # Criar tabela vendas_fiado se não existir
    if 'vendas_fiado' not in tabelas_existentes:
        print("📝 Criando tabela vendas_fiado...")
        cursor.execute("""
            CREATE TABLE vendas_fiado (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT NOT NULL,
                telefone TEXT,
                produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL,
                total REAL NOT NULL,
                data_vencimento TEXT NOT NULL,
                observacoes TEXT,
                status TEXT DEFAULT 'pendente',
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabela vendas_fiado criada")
    
    # Criar tabela configuracoes se não existir
    if 'configuracoes' not in tabelas_existentes:
        print("📝 Criando tabela configuracoes...")
        cursor.execute("""
            CREATE TABLE configuracoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chave TEXT UNIQUE NOT NULL,
                valor TEXT,
                descricao TEXT,
                data_modificacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Inserir configurações padrão
        configs_padrao = [
            ('versao_sistema', '2025.1.0', 'Versão atual do sistema'),
            ('nome_lanchonete', 'Minha Lanchonete', 'Nome da lanchonete'),
            ('moeda', 'BRL', 'Moeda padrão'),
            ('backup_automatico', 'true', 'Backup automático ativado')
        ]
        
        for chave, valor, desc in configs_padrao:
            cursor.execute("""
                INSERT OR IGNORE INTO configuracoes (chave, valor, descricao)
                VALUES (?, ?, ?)
            """, (chave, valor, desc))
        
        print("✅ Tabela configuracoes criada com dados padrão")
    
    conn.commit()
    
    # Verificar estrutura final
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas_finais = [row[0] for row in cursor.fetchall()]
    print(f"📋 Tabelas finais: {tabelas_finais}")
    
    conn.close()
    print("✅ Estrutura do banco verificada e corrigida")

if __name__ == "__main__":
    verificar_estrutura_banco()