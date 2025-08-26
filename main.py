"""
Sistema de Gerenciamento de Lanchonete
Aplicação principal

Autor: Victor Soares Ferreira
Versão: 1.0.0
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Adicionar src ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.interface.main_window import MainWindow
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Certifique-se de que todas as dependências estão instaladas.")
    sys.exit(1)


def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    dependencias = [
        ('tkinter', 'tkinter'),
        ('sqlite3', 'sqlite3'),
        ('pandas', 'pandas'),
        ('matplotlib', 'matplotlib.pyplot'),
        ('PIL', 'PIL'),
        ('openpyxl', 'openpyxl')
    ]
    
    missing = []
    for nome, modulo in dependencias:
        try:
            __import__(modulo)
        except ImportError:
            missing.append(nome)
    
    if missing:
        message = f"As seguintes dependências não foram encontradas:\n{', '.join(missing)}\n\n"
        message += "Instale as dependências usando:\n"
        message += "poetry install\n\nou\n"
        message += f"pip install {' '.join(missing)}"
        
        # Tentar mostrar mensagem gráfica se tkinter estiver disponível
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Dependências Faltando", message)
            root.destroy()
        except:
            print(message)
        
        return False
    
    return True


def main():
    """Função principal da aplicação"""
    try:
        # Verificar dependências
        if not verificar_dependencias():
            sys.exit(1)
        
        # Configurar diretório de trabalho
        if hasattr(sys, '_MEIPASS'):
            # Executando como executável empacotado
            os.chdir(sys._MEIPASS)
        else:
            # Executando como script Python
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Criar diretórios necessários
        os.makedirs('data', exist_ok=True)
        os.makedirs('assets', exist_ok=True)
        
        # Inicializar e executar aplicação
        app = MainWindow()
        app.run()
        
    except KeyboardInterrupt:
        print("\nAplicação interrompida pelo usuário.")
        sys.exit(0)
        
    except Exception as e:
        error_message = f"Erro inesperado ao iniciar a aplicação:\n{str(e)}"
        
        # Tentar mostrar mensagem gráfica
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Erro Fatal", error_message)
            root.destroy()
        except:
            print(error_message)
        
        sys.exit(1)


if __name__ == "__main__":
    main()
