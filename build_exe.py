"""
Script para empacotamento do sistema em executável
Utiliza Nuitka para criar um .exe otimizado
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def criar_icone():
    """Cria um ícone básico usando Pillow"""
    try:
        from PIL import Image, ImageDraw
        
        ico_path = "assets/icon.ico"
        
        # Criar um ícone simples
        img = Image.new('RGBA', (256, 256), (0, 100, 0, 255))  # Verde
        draw = ImageDraw.Draw(img)
        
        # Desenhar um círculo branco
        draw.ellipse([50, 50, 206, 206], fill=(255, 255, 255, 255))
        
        # Desenhar texto "L" no centro
        bbox = draw.textbbox((0, 0), "L", anchor="mm")
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (256 - text_width) // 2
        y = (256 - text_height) // 2
        draw.text((x, y), "L", fill=(0, 100, 0, 255), anchor="mm")
        
        # Salvar como ICO
        img.save(ico_path, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
        
        print(f"✓ Ícone criado: {ico_path}")
        return True
    except Exception as e:
        print(f"⚠ Erro ao criar ícone: {e}")
        return False

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    dependencias = ['nuitka', 'pillow', 'pandas', 'matplotlib', 'openpyxl', 'tabulate', 'requests']
    
    print("Verificando dependências...")
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✓ {dep}")
        except ImportError:
            print(f"✗ {dep} - instalando...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', dep], check=True)

def limpar_builds():
    """Remove arquivos de build anteriores"""
    dirs_para_remover = [
        'main.build',
        'main.dist',
        'main.onefile-build',
        'build',
        'dist'
    ]
    
    for dir_name in dirs_para_remover:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Removido: {dir_name}")

def empacotar():
    """Empacota a aplicação usando Nuitka"""
    print("\n=== Iniciando empacotamento ===")
    
    # Comando Nuitka
    cmd = [
        sys.executable, '-m', 'nuitka',
        '--onefile',
        '--enable-plugin=tk-inter',
        '--windows-disable-console',
        '--output-filename=SistemaLanchonete.exe',
        '--include-data-dir=data=data',
        '--include-data-dir=assets=assets',
        '--include-data-dir=src=src',
        '--follow-imports',
        '--show-progress',
        '--assume-yes-for-downloads',
        'main.py'
    ]
    
    # Adicionar ícone se existir
    if os.path.exists('assets/icon.ico'):
        cmd.extend(['--windows-icon-from-ico=assets/icon.ico'])
    
    try:
        print("Executando Nuitka...")
        subprocess.run(cmd, check=True)
        print("\n✓ Executável criado com sucesso!")
        
        # Verificar se o arquivo foi criado
        if os.path.exists('SistemaLanchonete.exe'):
            tamanho = os.path.getsize('SistemaLanchonete.exe') / (1024*1024)
            print(f"✓ Arquivo: SistemaLanchonete.exe ({tamanho:.1f} MB)")
            return True
        else:
            print("✗ Erro: Executável não foi criado")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro no empacotamento: {e}")
        return False

def criar_instalador():
    """Cria script de instalação/atualização"""
    script_instalador = """@echo off
echo ================================
echo  Sistema de Lanchonete v1.0.0
echo  Instalador/Atualizador
echo ================================
echo.

REM Criar diretórios necessários
if not exist "data" mkdir data
if not exist "assets" mkdir assets
if not exist "backup" mkdir backup

REM Fazer backup da versão anterior (se existir)
if exist "SistemaLanchonete.exe" (
    echo Fazendo backup da versão anterior...
    copy "SistemaLanchonete.exe" "backup\\SistemaLanchonete_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.exe" >nul
)

REM Fazer backup do banco de dados (se existir)
if exist "data\\banco.db" (
    echo Fazendo backup do banco de dados...
    copy "data\\banco.db" "backup\\banco_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db" >nul
)

echo.
echo Instalação/Atualização concluída!
echo.
echo Para executar o sistema, clique duas vezes em:
echo SistemaLanchonete.exe
echo.
pause
"""
    
    with open('instalar.bat', 'w', encoding='utf-8') as f:
        f.write(script_instalador)
    
    print("✓ Script de instalação criado: instalar.bat")

def main():
    """Função principal"""
    print("=== BUILD SISTEMA LANCHONETE ===")
    print("Preparando para empacotamento...\n")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('main.py'):
        print("✗ Erro: Execute este script no diretório raiz do projeto")
        return False
    
    # Criar diretórios necessários
    os.makedirs('data', exist_ok=True)
    os.makedirs('assets', exist_ok=True)
    os.makedirs('backup', exist_ok=True)
    
    # Verificar dependências
    verificar_dependencias()
    
    # Criar ícone
    criar_icone()
    
    # Limpar builds anteriores
    limpar_builds()
    
    # Empacotar
    sucesso = empacotar()
    
    if sucesso:
        # Criar instalador
        criar_instalador()
        
        print("\n=== EMPACOTAMENTO CONCLUÍDO ===")
        print("✓ Executável: SistemaLanchonete.exe")
        print("✓ Instalador: instalar.bat")
        print("\nPara distribuir:")
        print("1. Copie SistemaLanchonete.exe para o computador de destino")
        print("2. Execute instalar.bat para configurar")
        print("3. Execute SistemaLanchonete.exe para usar o sistema")
        
        return True
    else:
        print("\n✗ Falha no empacotamento")
        return False

if __name__ == "__main__":
    main()