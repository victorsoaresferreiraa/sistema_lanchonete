"""
Script alternativo para empacotamento usando PyInstaller
Solução mais estável que o Nuitka para problemas de conexão
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def verificar_pyinstaller():
    """Verifica e instala PyInstaller se necessário"""
    try:
        import PyInstaller
        print("✓ PyInstaller já está instalado")
        return True
    except ImportError:
        print("📦 Instalando PyInstaller...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
            print("✓ PyInstaller instalado com sucesso")
            return True
        except subprocess.CalledProcessError:
            print("✗ Erro ao instalar PyInstaller")
            return False

def limpar_builds():
    """Remove arquivos de build anteriores"""
    dirs_para_remover = [
        'build', 'dist', '__pycache__',
        'main.spec'
    ]
    
    for dir_name in dirs_para_remover:
        if os.path.exists(dir_name):
            if os.path.isdir(dir_name):
                shutil.rmtree(dir_name)
            else:
                os.remove(dir_name)
            print(f"✓ Removido: {dir_name}")

def criar_icone():
    """Cria um ícone básico se não existir"""
    ico_path = "assets/icon.ico"
    
    if os.path.exists(ico_path):
        print(f"✓ Ícone já existe: {ico_path}")
        return ico_path
    
    try:
        from PIL import Image, ImageDraw
        
        os.makedirs("assets", exist_ok=True)
        
        # Criar um ícone simples
        img = Image.new('RGBA', (256, 256), (34, 139, 34, 255))  # Verde floresta
        draw = ImageDraw.Draw(img)
        
        # Desenhar um círculo branco
        draw.ellipse([40, 40, 216, 216], fill=(255, 255, 255, 255))
        
        # Desenhar "L" no centro
        draw.text((128, 128), "L", fill=(34, 139, 34, 255), anchor="mm", 
                 font_size=100 if hasattr(draw, 'font_size') else None)
        
        # Salvar como ICO
        img.save(ico_path, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
        print(f"✓ Ícone criado: {ico_path}")
        return ico_path
    except Exception as e:
        print(f"⚠ Erro ao criar ícone: {e}")
        return None

def empacotar_pyinstaller():
    """Empacota usando PyInstaller"""
    print("\n🔄 Empacotando com PyInstaller...")
    
    # Criar ícone
    icone = criar_icone()
    
    # Comando PyInstaller
    comando = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",  # Remove console no Windows
        "--name=SistemaLanchonete",
        "--add-data=data;data",
        "--add-data=src;src", 
        "--add-data=assets;assets",
        "--hidden-import=PIL",
        "--hidden-import=pandas",
        "--hidden-import=matplotlib",
        "--hidden-import=openpyxl",
        "--hidden-import=tkinter",
        "--clean",
        "main.py"
    ]
    
    # Adicionar ícone se criado
    if icone:
        comando.extend(["--icon", icone])
    
    try:
        print("📦 Executando PyInstaller...")
        result = subprocess.run(comando, capture_output=True, text=True, timeout=1800)
        
        if result.returncode == 0:
            print("✅ Empacotamento concluído com sucesso!")
            
            # Verificar se arquivo foi criado
            exe_path = "dist/SistemaLanchonete.exe"
            if os.path.exists(exe_path):
                size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
                print(f"📁 Executável criado: {exe_path} ({size:.1f} MB)")
                
                # Copiar para raiz do projeto
                shutil.copy2(exe_path, "SistemaLanchonete.exe")
                print("✓ Executável copiado para raiz do projeto")
                
                return True
            else:
                print("✗ Arquivo executável não foi encontrado")
                return False
        else:
            print(f"✗ Erro no empacotamento:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Timeout - processo muito lento")
        return False
    except Exception as e:
        print(f"✗ Erro: {str(e)}")
        return False

def main():
    """Função principal"""
    print("=== Sistema de Empacotamento Alternativo ===")
    print("🔧 Usando PyInstaller como alternativa ao Nuitka")
    
    # Verificar se está no diretório correto
    if not os.path.exists("main.py"):
        print("✗ Erro: main.py não encontrado")
        print("📁 Execute este script na pasta raiz do projeto")
        return False
    
    # Limpar builds anteriores
    limpar_builds()
    
    # Verificar PyInstaller
    if not verificar_pyinstaller():
        return False
    
    # Empacotar
    sucesso = empacotar_pyinstaller()
    
    if sucesso:
        print("\n🎉 Empacotamento concluído!")
        print("📱 Execute o arquivo SistemaLanchonete.exe para testar")
        print("\n💡 Dicas:")
        print("  • O executável inclui todas as dependências")
        print("  • Pode ser distribuído sem instalar Python")
        print("  • Para atualizar, substitua o .exe por uma nova versão")
    else:
        print("\n❌ Falha no empacotamento")
        print("\n🔄 Soluções alternativas:")
        print("  1. Execute diretamente com: python main.py")
        print("  2. Crie um script .bat para facilitar a execução")
        print("  3. Use o empacotamento online em serviços como auto-py-to-exe")
    
    return sucesso

if __name__ == "__main__":
    main()