#!/usr/bin/env python3
"""
Script para criar ambiente virtual limpo e instalar dependências
"""
import os
import sys
import subprocess
import shutil

def limpar_ambiente():
    """Limpar instalações conflitantes"""
    print("🧹 Limpando ambiente...")
    
    # Remover diretórios problemáticos
    dirs_para_remover = ['.pythonlibs', '__pycache__', '.pytest_cache', 'venv_lanchonete']
    for dir_name in dirs_para_remover:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Removido: {dir_name}")
    
    # Remover arquivos .pyc
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def criar_venv():
    """Criar ambiente virtual"""
    print("🏗️ Criando ambiente virtual...")
    
    # Usar python3.11 especificamente
    result = subprocess.run([sys.executable, '-m', 'venv', 'venv_clean'], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Erro ao criar venv: {result.stderr}")
        return False
    
    print("✓ Ambiente virtual criado")
    return True

def instalar_dependencias():
    """Instalar dependências no ambiente virtual"""
    print("📦 Instalando dependências...")
    
    # Ativar venv e instalar
    if os.name == 'nt':  # Windows
        pip_path = 'venv_clean/Scripts/pip'
        python_path = 'venv_clean/Scripts/python'
    else:  # Linux/Mac
        pip_path = 'venv_clean/bin/pip'
        python_path = 'venv_clean/bin/python'
    
    # Atualizar pip
    subprocess.run([pip_path, 'install', '--upgrade', 'pip'], check=True)
    
    # Instalar dependências específicas
    dependencias = [
        'numpy==1.24.4',  # Versão compatível com Python 3.11
        'pandas==2.0.3',
        'matplotlib==3.7.2',
        'openpyxl==3.1.2',
        'pillow==10.0.1'
    ]
    
    for dep in dependencias:
        print(f"Instalando {dep}...")
        result = subprocess.run([pip_path, 'install', dep], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {dep}")
        else:
            print(f"❌ Erro em {dep}: {result.stderr}")
    
    # Testar imports
    test_code = """
import numpy, pandas, matplotlib
print(f"✅ numpy: {numpy.__version__}")
print(f"✅ pandas: {pandas.__version__}")
print(f"✅ matplotlib: {matplotlib.__version__}")
"""
    
    result = subprocess.run([python_path, '-c', test_code], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("🎉 Todas as dependências instaladas com sucesso!")
        print(result.stdout)
        return True
    else:
        print(f"❌ Erro no teste: {result.stderr}")
        return False

def criar_script_execucao():
    """Criar script para executar com ambiente virtual"""
    script_content = '''#!/bin/bash
# Script para executar sistema com ambiente virtual limpo

echo "🚀 Iniciando Sistema de Lanchonete..."

# Verificar se venv existe
if [ ! -d "venv_clean" ]; then
    echo "❌ Ambiente virtual não encontrado. Execute: python criar_ambiente_limpo.py"
    exit 1
fi

# Ativar ambiente virtual
source venv_clean/bin/activate

# Verificar dependências
python -c "import numpy, pandas, matplotlib, tkinter; print('✅ Dependências OK')" || {
    echo "❌ Erro nas dependências"
    exit 1
}

# Executar sistema
python main.py
'''
    
    with open('executar_sistema.sh', 'w') as f:
        f.write(script_content)
    
    os.chmod('executar_sistema.sh', 0o755)
    print("✓ Script de execução criado: executar_sistema.sh")

if __name__ == "__main__":
    print("🚀 Configurando ambiente limpo para Sistema de Lanchonete...")
    
    # Etapa 1: Limpar
    limpar_ambiente()
    
    # Etapa 2: Criar venv
    if not criar_venv():
        sys.exit(1)
    
    # Etapa 3: Instalar dependências
    if not instalar_dependencias():
        sys.exit(1)
    
    # Etapa 4: Criar script
    criar_script_execucao()
    
    print("\n🎉 Ambiente configurado com sucesso!")
    print("Para executar o sistema: ./executar_sistema.sh")