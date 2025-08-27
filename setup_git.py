"""
Script para configurar Git e conectar com GitHub
Automatiza o processo de versionamento e sincronização
"""

import os
import subprocess
import json
from datetime import datetime

def executar_comando(comando, mostrar_output=True):
    """Executa comando no terminal e retorna resultado"""
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd='.')
        if mostrar_output and result.stdout:
            print(result.stdout.strip())
        if result.stderr and "warning" not in result.stderr.lower():
            print(f"Aviso: {result.stderr.strip()}")
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        print(f"Erro ao executar comando: {e}")
        return False, ""

def verificar_git():
    """Verifica se Git está instalado"""
    print("🔍 Verificando instalação do Git...")
    sucesso, _ = executar_comando("git --version")
    if sucesso:
        print("✅ Git está instalado")
        return True
    else:
        print("❌ Git não está instalado")
        print("📥 Baixe e instale o Git de: https://git-scm.com/downloads")
        return False

def configurar_git_usuario():
    """Configura usuário do Git se necessário"""
    print("\n🔧 Verificando configuração do usuário Git...")
    
    sucesso, nome = executar_comando("git config --global user.name", False)
    if not nome:
        nome_usuario = input("Digite seu nome para o Git: ")
        executar_comando(f'git config --global user.name "{nome_usuario}"')
    
    sucesso, email = executar_comando("git config --global user.email", False)
    if not email:
        email_usuario = input("Digite seu email do GitHub: ")
        executar_comando(f'git config --global user.email "{email_usuario}"')
    
    print("✅ Usuário Git configurado")

def inicializar_repositorio():
    """Inicializa repositório Git local"""
    print("\n📁 Inicializando repositório Git...")
    
    if os.path.exists('.git'):
        print("✅ Repositório Git já existe")
        return True
    
    sucesso, _ = executar_comando("git init")
    if sucesso:
        print("✅ Repositório Git inicializado")
        return True
    else:
        print("❌ Erro ao inicializar repositório")
        return False

def criar_gitignore():
    """Cria arquivo .gitignore apropriado"""
    print("\n📄 Criando .gitignore...")
    
    gitignore_content = """# Arquivos Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
env.bak/
venv.bak/

# Arquivos do sistema
.DS_Store
Thumbs.db
*.log

# Arquivos de desenvolvimento
.pytest_cache/
.coverage
.vscode/
.idea/

# Arquivos temporários
*.tmp
*.temp
*~

# Arquivos de build
build/
dist/
*.egg-info/
main.build/
main.dist/
main.onefile-build/

# Banco de dados (manter estrutura, não dados)
data/*.db
!data/.gitkeep

# Relatórios gerados
data/estoque_*.xlsx
data/historico_*.xlsx
data/grafico_*.png
data/backup_*.db

# Configurações locais
config.local.json
.env
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    # Criar arquivo .gitkeep para manter pasta data
    os.makedirs('data', exist_ok=True)
    with open('data/.gitkeep', 'w') as f:
        f.write('')
    
    print("✅ .gitignore criado")

def criar_readme():
    """Cria README.md profissional"""
    print("\n📄 Criando README.md...")
    
    readme_content = """# 🍔 Sistema de Gerenciamento para Lanchonete

Sistema completo de gestão para lanchonetes desenvolvido em Python com interface gráfica Tkinter.

## 📋 Funcionalidades

- ✅ **Controle de Estoque** - Gestão completa de produtos, preços e categorias
- ✅ **Registro de Vendas** - Sistema de vendas com cálculo automático de totais
- ✅ **Histórico Financeiro** - Acompanhamento de todas as vendas e receitas
- ✅ **Relatórios Excel** - Exportação de dados para análise
- ✅ **Gráficos de Análise** - Visualizações de performance e vendas
- ✅ **Sistema de Backup** - Proteção automática dos dados

## 🚀 Como Usar

### Opção 1: Executável (Recomendado)
1. Baixe o arquivo `SistemaLanchonete.exe`
2. Execute diretamente - não precisa instalar Python

### Opção 2: Execução Direta
1. Certifique-se que tem Python 3.8+ instalado
2. Execute `executar_lanchonete.bat` (Windows) ou `python main.py`

### Opção 3: Desenvolvimento
```bash
# Clonar repositório
git clone https://github.com/SEU_USUARIO/sistema-lanchonete.git
cd sistema-lanchonete

# Instalar dependências
pip install -r requirements.txt

# Executar sistema
python main.py
```

## 📦 Dependências

- Python 3.8+
- tkinter (incluído no Python)
- pandas
- matplotlib
- openpyxl
- pillow
- requests

## 🛠️ Desenvolvimento

O sistema está organizado em módulos:

- `src/estoque/` - Gerenciamento de produtos e estoque
- `src/interface/` - Interface gráfica do usuário
- `src/pedidos/` - Controle de vendas e relatórios
- `src/utils/` - Funções auxiliares
- `data/` - Banco de dados SQLite

## 📊 Estrutura do Banco de Dados

### Tabela `estoque`
- produto (TEXT) - Nome do produto
- quantidade (INTEGER) - Quantidade em estoque
- preco (REAL) - Preço unitário
- categoria (TEXT) - Categoria do produto

### Tabela `historico_vendas`
- id (INTEGER) - ID único da venda
- produto (TEXT) - Produto vendido
- quantidade (INTEGER) - Quantidade vendida
- preco_unitario (REAL) - Preço na venda
- valor_total (REAL) - Total da venda
- data_hora (TEXT) - Data e hora da venda

## 🔧 Configuração

1. **Primeira execução**: O sistema cria automaticamente o banco de dados
2. **Backup**: Dados salvos em `data/banco.db`
3. **Relatórios**: Exportados para pasta `data/`

## 📈 Atualizações

O sistema inclui verificação automática de atualizações. Novas versões são baixadas automaticamente.

## 🆘 Suporte

Para problemas ou sugestões:
1. Abra uma [Issue](https://github.com/SEU_USUARIO/sistema-lanchonete/issues)
2. Consulte a [Documentação Completa](DOCUMENTACAO_COMPLETA.md)
3. Verifique as [Instruções de Instalação](INSTRUCOES_INSTALACAO.md)

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Desenvolvedor

Desenvolvido para uso em lanchonetes e pequenos comércios alimentícios.

---

**Versão:** 2.0.0  
**Última atualização:** $(date +'%d/%m/%Y')
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README.md criado")

def criar_requirements():
    """Cria arquivo requirements.txt"""
    print("\n📄 Criando requirements.txt...")
    
    requirements = """pandas>=1.5.0
matplotlib>=3.5.0
openpyxl>=3.0.0
Pillow>=9.0.0
requests>=2.28.0
"""
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)
    
    print("✅ requirements.txt criado")

def criar_license():
    """Cria arquivo de licença MIT"""
    print("\n📄 Criando LICENSE...")
    
    ano_atual = datetime.now().year
    license_content = f"""MIT License

Copyright (c) {ano_atual} Sistema Lanchonete

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    with open('LICENSE', 'w', encoding='utf-8') as f:
        f.write(license_content)
    
    print("✅ LICENSE criado")

def adicionar_arquivos_git():
    """Adiciona arquivos ao Git"""
    print("\n➕ Adicionando arquivos ao Git...")
    
    # Adicionar todos os arquivos importantes
    arquivos = [
        "main.py",
        "src/",
        "assets/",
        "tests/",
        "*.py",
        "*.md",
        "requirements.txt",
        "LICENSE",
        ".gitignore",
        "data/.gitkeep"
    ]
    
    for arquivo in arquivos:
        executar_comando(f"git add {arquivo}", False)
    
    print("✅ Arquivos adicionados ao Git")

def fazer_primeiro_commit():
    """Faz o primeiro commit"""
    print("\n💾 Fazendo primeiro commit...")
    
    commit_message = "🎉 Initial commit - Sistema completo de gerenciamento para lanchonete"
    sucesso, _ = executar_comando(f'git commit -m "{commit_message}"')
    
    if sucesso:
        print("✅ Primeiro commit realizado")
        return True
    else:
        print("⚠️ Commit já existe ou não há mudanças")
        return True

def conectar_github():
    """Conecta com repositório do GitHub"""
    print("\n🔗 Conectando com GitHub...")
    
    print("Para conectar com GitHub, você precisa:")
    print("1. Ter um repositório no GitHub (pode estar vazio)")
    print("2. Ter a URL do repositório")
    print("\nExemplo de URL: https://github.com/seunome/sistema-lanchonete.git")
    
    github_url = input("\nDigite a URL do seu repositório GitHub: ").strip()
    
    if not github_url:
        print("❌ URL não fornecida")
        return False
    
    # Verificar se já tem remote origin
    sucesso, _ = executar_comando("git remote get-url origin", False)
    if sucesso:
        print("📝 Atualizando URL do repositório remoto...")
        executar_comando(f"git remote set-url origin {github_url}")
    else:
        print("📝 Adicionando repositório remoto...")
        executar_comando(f"git remote add origin {github_url}")
    
    print("✅ GitHub conectado")
    return True

def enviar_para_github():
    """Envia código para GitHub"""
    print("\n📤 Enviando código para GitHub...")
    
    # Verificar se tem commits
    sucesso, _ = executar_comando("git log --oneline -1", False)
    if not sucesso:
        print("❌ Nenhum commit encontrado. Fazendo commit primeiro...")
        fazer_primeiro_commit()
    
    # Enviar para GitHub
    print("📤 Fazendo push para GitHub...")
    sucesso, output = executar_comando("git push -u origin main")
    
    if not sucesso:
        print("⚠️ Tentando com branch master...")
        executar_comando("git branch -M main")
        sucesso, _ = executar_comando("git push -u origin main")
    
    if sucesso:
        print("✅ Código enviado para GitHub com sucesso!")
        return True
    else:
        print("❌ Erro ao enviar para GitHub")
        print("💡 Possíveis soluções:")
        print("   1. Verificar se a URL do repositório está correta")
        print("   2. Fazer login no GitHub: gh auth login")
        print("   3. Usar token de acesso pessoal")
        return False

def criar_script_atualizacao():
    """Cria script para atualizações futuras"""
    print("\n🔄 Criando script de atualização...")
    
    script_content = """@echo off
echo ================================
echo   Atualizando Sistema GitHub
echo ================================
echo.

REM Verificar se há mudanças
git status --porcelain > temp_status.txt
set /p changes=<temp_status.txt
del temp_status.txt

if "%changes%"=="" (
    echo Nenhuma mudança para enviar.
    pause
    exit /b 0
)

REM Adicionar mudanças
echo Adicionando mudanças...
git add .

REM Commit com timestamp
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "MIN=%dt:~10,2%" & set "SS=%dt:~12,2%"
set "timestamp=%DD%/%MM%/%YYYY% %HH%:%MIN%"

set /p "mensagem=Digite a mensagem do commit (ou pressione Enter para usar automática): "
if "%mensagem%"=="" set "mensagem=🔄 Atualização automática - %timestamp%"

echo Fazendo commit...
git commit -m "%mensagem%"

REM Enviar para GitHub
echo Enviando para GitHub...
git push

if %errorlevel% equ 0 (
    echo.
    echo ✅ Atualização enviada para GitHub com sucesso!
) else (
    echo.
    echo ❌ Erro ao enviar atualização
)

echo.
pause
"""
    
    with open('atualizar_github.bat', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Script atualizar_github.bat criado")
    print("💡 Para futuras atualizações, execute este arquivo!")

def main():
    """Função principal de configuração"""
    print("🚀 Configuração Git + GitHub para Sistema da Lanchonete")
    print("=" * 60)
    
    # Verificações iniciais
    if not verificar_git():
        return
    
    # Configurações
    configurar_git_usuario()
    
    if not inicializar_repositorio():
        return
    
    # Criar arquivos necessários
    criar_gitignore()
    criar_readme()
    criar_requirements()
    criar_license()
    
    # Git operations
    adicionar_arquivos_git()
    fazer_primeiro_commit()
    
    # GitHub
    if conectar_github():
        enviar_para_github()
    
    # Script para futuras atualizações
    criar_script_atualizacao()
    
    print("\n🎉 Configuração concluída!")
    print("\n📋 Próximos passos:")
    print("1. ✅ Seu código já está no GitHub")
    print("2. 🔄 Para futuras atualizações: execute 'atualizar_github.bat'")
    print("3. 🌐 Acesse seu repositório no GitHub para ver o código")
    print("4. 📝 Edite o README.md para personalizar as informações")
    
    print("\n💡 Comandos Git úteis:")
    print("   git status          - Ver status das mudanças")
    print("   git add .           - Adicionar todas as mudanças")
    print("   git commit -m 'msg' - Fazer commit")
    print("   git push            - Enviar para GitHub")

if __name__ == "__main__":
    main()