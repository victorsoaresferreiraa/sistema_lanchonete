#!/bin/bash
# Script para configurar ambiente virtual limpo

echo "🚀 Configurando ambiente virtual para Sistema de Lanchonete..."

# Remover instalações conflitantes
rm -rf .pythonlibs
rm -rf __pycache__
find . -name "*.pyc" -delete

# Criar ambiente virtual limpo
python3 -m venv venv_lanchonete
source venv_lanchonete/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências específicas sem conflitos
pip install --no-user numpy==1.24.3
pip install --no-user pandas==2.0.3
pip install --no-user matplotlib==3.7.2
pip install --no-user openpyxl==3.1.2
pip install --no-user pillow==10.0.1
pip install --no-user tabulate==0.9.0

echo "✅ Ambiente virtual configurado com sucesso!"
echo "Para usar: source venv_lanchonete/bin/activate"