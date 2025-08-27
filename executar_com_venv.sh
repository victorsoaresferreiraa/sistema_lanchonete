#!/bin/bash
# Script para executar sistema com ambiente virtual

echo "🚀 Iniciando Sistema de Lanchonete com ambiente virtual..."

# Ativar ambiente virtual
source venv_lanchonete/bin/activate

# Verificar dependências
python -c "import numpy, pandas, matplotlib, tkinter; print('✅ Todas as dependências OK')"

# Executar sistema principal
python main.py