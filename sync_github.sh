#!/bin/bash

# Script de sincronização rápida para GitHub
echo "🔄 Sincronização Rápida com GitHub"
echo "=================================="

# Verificar se é repositório git
if [ ! -d ".git" ]; then
    echo "📁 Inicializando repositório Git..."
    git init
fi

# Configurar remote se não existir
if ! git remote get-url origin >/dev/null 2>&1; then
    echo "🔗 Configurando repositório remoto..."
    git remote add origin https://github.com/victorsoaresferreiraa/sistema_lanchonete.git
fi

# Baixar mudanças do GitHub primeiro
echo "📥 Baixando mudanças do GitHub..."
git fetch origin

# Verificar se há mudanças remotas
if git log HEAD..origin/main --oneline 2>/dev/null | grep -q .; then
    echo "📋 Mudanças encontradas no GitHub, baixando..."
    git pull origin main
else
    echo "✅ Nenhuma mudança remota"
fi

# Verificar mudanças locais
if git status --porcelain | grep -q .; then
    echo "📋 Mudanças locais encontradas:"
    git status --short
    
    echo "📤 Enviando para GitHub..."
    git add .
    
    # Commit com timestamp
    timestamp=$(date '+%d/%m/%Y %H:%M')
    git commit -m "🔄 Sync Replit - $timestamp"
    
    # Push para GitHub
    git push origin main || git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo "✅ Sincronização completa!"
    else
        echo "❌ Erro ao enviar para GitHub"
    fi
else
    echo "✅ Nenhuma mudança local para enviar"
fi

echo "📊 Status atual:"
git log --oneline -3