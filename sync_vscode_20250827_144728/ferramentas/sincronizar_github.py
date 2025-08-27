"""
Sistema de sincronização com GitHub para Replit
Permite sincronizar mudanças bidirecionalmente
"""

import subprocess
import os
import json
from datetime import datetime

def executar_comando(comando, silent=False):
    """Executa comando e retorna resultado"""
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd='.')
        if not silent and result.stdout:
            print(result.stdout.strip())
        if result.stderr and "warning" not in result.stderr.lower():
            print(f"Aviso: {result.stderr.strip()}")
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        print(f"Erro: {e}")
        return False, ""

def verificar_repositorio():
    """Verifica se repositório está configurado"""
    print("🔍 Verificando configuração do repositório...")
    
    # Verificar se é repositório git
    if not os.path.exists('.git'):
        print("📁 Inicializando repositório Git...")
        executar_comando("git init")
    
    # Verificar remote
    sucesso, output = executar_comando("git remote get-url origin", silent=True)
    if not sucesso:
        print("🔗 Configurando repositório remoto...")
        executar_comando("git remote add origin https://github.com/victorsoaresferreiraa/sistema_lanchonete.git")
    else:
        print(f"✅ Repositório remoto: {output}")
    
    return True

def criar_arquivos_git():
    """Cria arquivos necessários para Git"""
    print("📄 Criando arquivos de configuração...")
    
    # .gitignore atualizado
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
.pytest_cache/
.coverage

# Sistema
.DS_Store
Thumbs.db
*.log
*.tmp
*~

# Replit
.replit
.config/
.pythonlibs/
.cache/
.local/
poetry.lock

# Build
build/
dist/
*.egg-info/
main.build/
main.dist/
main.onefile-build/

# Banco de dados (manter estrutura)
data/*.db
!data/.gitkeep

# Relatórios gerados
data/*.xlsx
data/*.png
data/backup_*.db

# Configurações locais
.env
config.local.json
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    # Garantir pasta data
    os.makedirs('data', exist_ok=True)
    with open('data/.gitkeep', 'w') as f:
        f.write('# Manter pasta data no repositório\n')
    
    print("✅ Arquivos criados")

def verificar_mudancas():
    """Verifica se há mudanças para sincronizar"""
    print("🔍 Verificando mudanças...")
    
    sucesso, output = executar_comando("git status --porcelain", silent=True)
    
    if output:
        print("📋 Mudanças encontradas:")
        executar_comando("git status --short")
        return True
    else:
        print("✅ Nenhuma mudança local para enviar")
        return False

def baixar_do_github():
    """Baixa mudanças do GitHub"""
    print("📥 Baixando mudanças do GitHub...")
    
    # Primeiro, fazer fetch
    sucesso, _ = executar_comando("git fetch origin")
    if not sucesso:
        print("❌ Erro ao buscar mudanças do GitHub")
        return False
    
    # Verificar se há mudanças remotas
    sucesso, output = executar_comando("git log HEAD..origin/main --oneline", silent=True)
    
    if output:
        print(f"📋 Mudanças encontradas no GitHub:")
        print(output)
        
        # Fazer pull
        sucesso, _ = executar_comando("git pull origin main")
        if sucesso:
            print("✅ Mudanças baixadas com sucesso!")
            return True
        else:
            print("❌ Erro ao baixar mudanças")
            return False
    else:
        print("✅ Nenhuma mudança no GitHub para baixar")
        return True

def enviar_para_github():
    """Envia mudanças para GitHub"""
    print("📤 Enviando mudanças para GitHub...")
    
    # Adicionar arquivos
    executar_comando("git add .")
    
    # Verificar se há algo para commit
    sucesso, output = executar_comando("git status --porcelain", silent=True)
    if not output:
        print("✅ Nenhuma mudança para enviar")
        return True
    
    # Criar commit
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    commit_msg = f"🔄 Atualização Replit - {timestamp}"
    
    print("💾 Criando commit...")
    sucesso, _ = executar_comando(f'git commit -m "{commit_msg}"')
    if not sucesso:
        print("❌ Erro ao criar commit")
        return False
    
    # Enviar para GitHub
    print("📤 Enviando para GitHub...")
    sucesso, _ = executar_comando("git push origin main")
    
    if not sucesso:
        # Tentar com master se main não funcionar
        print("🔄 Tentando com branch master...")
        executar_comando("git branch -M main")
        sucesso, _ = executar_comando("git push -u origin main")
    
    if sucesso:
        print("✅ Mudanças enviadas com sucesso!")
        return True
    else:
        print("❌ Erro ao enviar para GitHub")
        print("💡 Verifique se tem permissão de escrita no repositório")
        return False

def sincronizacao_completa():
    """Executa sincronização completa"""
    print("🔄 Sincronização Completa com GitHub")
    print("=" * 50)
    
    # Configurar repositório
    if not verificar_repositorio():
        return False
    
    # Criar arquivos necessários
    criar_arquivos_git()
    
    # 1. Baixar mudanças do GitHub primeiro
    print("\n1️⃣ BAIXANDO mudanças do GitHub...")
    baixar_sucesso = baixar_do_github()
    
    # 2. Verificar mudanças locais
    print("\n2️⃣ VERIFICANDO mudanças locais...")
    tem_mudancas = verificar_mudancas()
    
    # 3. Enviar mudanças se houver
    if tem_mudancas:
        print("\n3️⃣ ENVIANDO mudanças para GitHub...")
        enviar_sucesso = enviar_para_github()
    else:
        enviar_sucesso = True
    
    # Resultado final
    print("\n" + "=" * 50)
    if baixar_sucesso and enviar_sucesso:
        print("🎉 Sincronização completa realizada com sucesso!")
        print("📱 Seu código está sincronizado entre Replit e GitHub")
    else:
        print("⚠️ Sincronização parcial - verifique erros acima")
    
    # Mostrar status final
    print("\n📊 Status atual:")
    executar_comando("git log --oneline -3")
    
    return baixar_sucesso and enviar_sucesso

def sincronizar_apenas_envio():
    """Envia apenas mudanças locais para GitHub"""
    print("📤 Enviando Mudanças para GitHub")
    print("=" * 40)
    
    verificar_repositorio()
    criar_arquivos_git()
    
    if verificar_mudancas():
        return enviar_para_github()
    else:
        print("✅ Nada para enviar")
        return True

def sincronizar_apenas_download():
    """Baixa apenas mudanças do GitHub"""
    print("📥 Baixando Mudanças do GitHub")
    print("=" * 40)
    
    verificar_repositorio()
    return baixar_do_github()

def main():
    """Menu principal"""
    print("🐙 Sistema de Sincronização GitHub")
    print("Repositório: https://github.com/victorsoaresferreiraa/sistema_lanchonete")
    print("=" * 60)
    
    print("\nOpções:")
    print("1. 🔄 Sincronização completa (baixar + enviar)")
    print("2. 📤 Apenas enviar mudanças para GitHub")
    print("3. 📥 Apenas baixar mudanças do GitHub")
    print("4. ❌ Sair")
    
    try:
        opcao = input("\nEscolha uma opção (1-4): ").strip()
        
        if opcao == "1":
            sincronizacao_completa()
        elif opcao == "2":
            sincronizar_apenas_envio()
        elif opcao == "3":
            sincronizar_apenas_download()
        elif opcao == "4":
            print("👋 Até mais!")
        else:
            print("❌ Opção inválida")
    
    except KeyboardInterrupt:
        print("\n👋 Operação cancelada")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()