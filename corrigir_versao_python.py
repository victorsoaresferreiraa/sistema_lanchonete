#!/usr/bin/env python3
"""
Script para corrigir versão do Python no pyproject.toml
Permite Python 3.10+ ao invés de apenas 3.11+
"""

import os
import shutil
from datetime import datetime

def corrigir_pyproject_toml():
    """Corrige versão do Python no pyproject.toml"""
    
    print("🔧 Corrigindo versão Python no pyproject.toml...")
    
    # Verificar se arquivo existe
    if not os.path.exists("pyproject.toml"):
        print("❌ Arquivo pyproject.toml não encontrado!")
        return False
    
    # Fazer backup
    backup_name = f"pyproject.toml.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2("pyproject.toml", backup_name)
    print(f"📋 Backup criado: {backup_name}")
    
    # Ler arquivo atual
    with open("pyproject.toml", "r", encoding="utf-8") as f:
        conteudo = f.read()
    
    # Mostrar versão atual
    if 'python = "^3.11"' in conteudo:
        print("📍 Versão atual: Python ^3.11 (requer 3.11+)")
        
        # Corrigir para aceitar 3.10+
        conteudo_corrigido = conteudo.replace('python = "^3.11"', 'python = "^3.10"')
        
        # Salvar arquivo corrigido
        with open("pyproject.toml", "w", encoding="utf-8") as f:
            f.write(conteudo_corrigido)
        
        print("✅ Corrigido para: Python ^3.10 (aceita 3.10+)")
        print("🎯 Agora compatível com seu Python 3.10.0")
        
        return True
    
    elif 'python = "^3.10"' in conteudo:
        print("✅ Já está correto: Python ^3.10")
        return True
    
    else:
        print("⚠️  Configuração Python não encontrada ou diferente")
        print("📋 Conteúdo atual:")
        print(conteudo[:500] + "..." if len(conteudo) > 500 else conteudo)
        return False

def criar_pyproject_toml_compativel():
    """Cria pyproject.toml compatível com Python 3.10"""
    
    pyproject_content = '''[tool.poetry]
name = "sistema-lanchonete"
version = "2.0.0"
description = "Sistema completo de gestão para lanchonetes com interface gráfica"
authors = ["Victor Soares <victorsoaresferreiraa@gmail.com>"]
readme = "README.md"
packages = [{include = "src"}]

[tool.poetry.dependencies]
python = "^3.10"
pandas = "^2.0.0"
matplotlib = "^3.7.0"
openpyxl = "^3.1.0"
tabulate = "^0.9.0"
pillow = "^10.0.0"
requests = "^2.31.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
black = "^23.7.0"
flake8 = "^6.0.0"
mypy = "^1.5.0"

[tool.poetry.group.build.dependencies]
pyinstaller = "^5.13.0"
nuitka = "^1.7.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88
target-version = ['py310']
include = '\\.pyi?$'
extend-exclude = '''
/(
  # directories
  \\.eggs
  | \\.git
  | \\.hg
  | \\.mypy_cache
  | \\.tox
  | \\.venv
  | build
  | dist
)/
'''

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=src --cov-report=html --cov-report=term-missing"

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
'''
    
    with open("pyproject.toml", "w", encoding="utf-8") as f:
        f.write(pyproject_content)
    
    print("✅ pyproject.toml compatível criado")

def main():
    """Função principal"""
    print("🐍 CORRETOR DE VERSÃO PYTHON")
    print("=" * 40)
    
    # Tentar corrigir arquivo existente
    if os.path.exists("pyproject.toml"):
        sucesso = corrigir_pyproject_toml()
        
        if not sucesso:
            print("\n🔄 Criando novo pyproject.toml compatível...")
            criar_pyproject_toml_compativel()
    else:
        print("📁 pyproject.toml não encontrado, criando novo...")
        criar_pyproject_toml_compativel()
    
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("1. Execute: poetry install")
    print("2. Execute: poetry run python main_funcional.py")
    print("3. Se der erro, execute: poetry env use python3.10")
    
    print("\n💡 COMANDOS ÚTEIS:")
    print("• poetry env info - Ver ambiente atual")
    print("• poetry env list - Listar ambientes")
    print("• poetry env use python3.10 - Usar Python 3.10")
    print("• poetry shell - Ativar ambiente virtual")

if __name__ == "__main__":
    main()