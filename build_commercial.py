
import PyInstaller.__main__
import os

def build_commercial():
    """Compila versão comercial com proteções"""
    
    # Opções do PyInstaller
    options = [
        'main_funcional.py',
        '--onefile',
        '--windowed',
        '--name=SistemaLanchonete_v2.0',
        '--icon=assets/icon.ico',
        '--add-data=assets;assets',
        '--hidden-import=tkinter',
        '--hidden-import=sqlite3',
        '--hidden-import=pandas',
        '--hidden-import=matplotlib',
        '--noconsole',
        '--distpath=dist_commercial',
        '--workpath=build_commercial',
        '--specpath=.',
        '--key=minha_chave_secreta_123'  # Criptografia
    ]
    
    PyInstaller.__main__.run(options)
    print("✅ Versão comercial criada em dist_commercial/")

if __name__ == "__main__":
    build_commercial()
