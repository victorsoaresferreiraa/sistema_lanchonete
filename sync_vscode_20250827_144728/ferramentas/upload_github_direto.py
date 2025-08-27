#!/usr/bin/env python3
"""
Script para fazer upload direto do projeto para GitHub
Ignora configurações Git complexas e foca em subir os arquivos
"""

import os
import shutil
import zipfile
from datetime import datetime

def criar_backup_projeto():
    """Cria backup compactado do projeto para upload manual"""
    print("📦 Criando backup do projeto para GitHub...")
    
    # Nome do arquivo de backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_backup = f"sistema_lanchonete_completo_{timestamp}.zip"
    
    # Arquivos e pastas para incluir
    incluir = [
        "main_funcional.py",
        "main.py",
        "README.md",
        "DOCUMENTACAO_COMPLETA.md",
        "INSTRUCOES_INSTALACAO.md",
        "INSTRUCOES_SINCRONIZACAO.md",
        "MANUAL_TREINAMENTO_SISTEMA_LANCHONETE.md",
        "GUIA_GITHUB.md",
        "AJUSTES_LAYOUT_DASHBOARD.md",
        "DASHBOARD_COMPLETO.md",
        "SOLUCAO_AMBIENTE_VIRTUAL.md",
        "executar_lanchonete.bat",
        "build_pyinstaller.py",
        "build_exe.py",
        "pyproject.toml",
        "sincronizar_github.py",
        "setup_git.py",
        "atualizar_github.bat",
        "sync_github.sh",
        "manual_instalar.md",
        "test_simples.py",
        "test_dashboard_demo.py",
        "src/",
        "assets/",
        "tests/"
    ]
    
    # Criar arquivo ZIP
    with zipfile.ZipFile(nome_backup, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in incluir:
            if os.path.exists(item):
                if os.path.isfile(item):
                    zipf.write(item)
                    print(f"✓ Adicionado: {item}")
                elif os.path.isdir(item):
                    for root, dirs, files in os.walk(item):
                        # Ignorar __pycache__ e outros arquivos temporários
                        dirs[:] = [d for d in dirs if not d.startswith('__pycache__')]
                        
                        for file in files:
                            if not file.endswith(('.pyc', '.pyo', '.tmp')):
                                file_path = os.path.join(root, file)
                                zipf.write(file_path)
                                print(f"✓ Adicionado: {file_path}")
        
        # Adicionar estrutura da pasta data (sem banco de dados)
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Criar .gitkeep na pasta data
        gitkeep_path = os.path.join(data_dir, ".gitkeep")
        with open(gitkeep_path, 'w') as f:
            f.write("# Manter estrutura da pasta data\n")
        
        zipf.write(gitkeep_path)
        print(f"✓ Adicionado: {gitkeep_path}")
    
    tamanho_mb = os.path.getsize(nome_backup) / (1024 * 1024)
    
    print(f"\n✅ Backup criado: {nome_backup}")
    print(f"📏 Tamanho: {tamanho_mb:.2f} MB")
    
    return nome_backup

def criar_readme_atualizado():
    """Cria README.md atualizado com todas as funcionalidades"""
    readme_content = """# 🍔 Sistema de Gestão de Lanchonete

## 📋 Descrição
Sistema completo para gestão de lanchonete desenvolvido em Python com interface Tkinter. Oferece controle total de estoque, vendas, caixa, clientes e relatórios financeiros.

## ✨ Funcionalidades Principais

### 🏪 Gestão Completa
- **📦 Controle de Estoque**: Cadastro, atualização e monitoramento de produtos
- **💰 Sistema de Vendas**: Vendas à vista e fiado com controle completo
- **📋 Contas em Aberto**: Gestão de crediário e cobrança de clientes
- **💳 Controle de Caixa**: Abertura, sangria, reforço e fechamento diário
- **📊 Dashboard Financeiro**: Métricas, gráficos e análises em tempo real
- **💾 Backup Automático**: Proteção completa dos dados
- **📄 Relatórios**: Exportação para Excel com múltiplas planilhas

### 🎯 Características Técnicas
- Interface gráfica moderna com Tkinter
- Banco de dados SQLite para persistência
- Exportação de dados em Excel (pandas/openpyxl)
- Gráficos interativos (matplotlib)
- Sistema de backup integrado
- Geração de executável (.exe)

## 🚀 Como Usar

### Instalação Rápida
```bash
# Clonar repositório
git clone https://github.com/victorsoaresferreiraa/sistema_lanchonete.git

# Instalar dependências
pip install -r requirements.txt

# Executar sistema
python main_funcional.py
```

### Executável Windows
```bash
# Gerar executável
python build_pyinstaller.py

# Ou usar arquivo bat
executar_lanchonete.bat
```

## 📚 Documentação

- **[Manual de Treinamento](MANUAL_TREINAMENTO_SISTEMA_LANCHONETE.md)**: Guia completo de uso
- **[Documentação Técnica](DOCUMENTACAO_COMPLETA.md)**: Arquitetura e manutenção
- **[Instruções de Instalação](INSTRUCOES_INSTALACAO.md)**: Setup detalhado
- **[Guia GitHub](GUIA_GITHUB.md)**: Versionamento e colaboração

## 🏗️ Arquitetura

```
sistema_lanchonete/
├── main_funcional.py           # Sistema principal completo
├── src/                        # Código fonte modular
│   ├── interface/             # Interfaces gráficas
│   ├── estoque/               # Gestão de inventário
│   ├── pedidos/               # Sistema de vendas
│   ├── relatorios/            # Dashboard e relatórios
│   └── utils/                 # Utilitários
├── data/                      # Banco de dados
├── assets/                    # Recursos visuais
├── tests/                     # Testes automatizados
└── docs/                      # Documentação
```

## 💼 Funcionalidades de Negócio

### Sistema de Vendas
- Vendas à vista e fiado
- Controle de estoque automático
- Histórico completo de transações
- Clientes e telefones

### Controle Financeiro
- Abertura/fechamento de caixa
- Sangria e reforço
- Relatórios de movimentação
- Dashboard com métricas

### Gestão de Clientes
- Cadastro de contas em aberto
- Controle de vencimentos
- Status de pagamento
- Histórico de compras

## 📊 Dashboard e Relatórios

### Métricas Disponíveis
- Vendas do dia/mês
- Produtos mais vendidos
- Ticket médio
- Contas em aberto
- Análise de categorias

### Exportações
- Excel com múltiplas planilhas
- Gráficos em PNG
- Backup completo
- Relatórios de caixa

## 🔧 Tecnologias

- **Python 3.8+**: Linguagem principal
- **Tkinter**: Interface gráfica
- **SQLite**: Banco de dados
- **Pandas**: Manipulação de dados
- **Matplotlib**: Gráficos
- **OpenPyXL**: Exportação Excel
- **PyInstaller**: Geração de executável

## 📱 Compatibilidade

- ✅ Windows 10/11
- ✅ Linux (Ubuntu, Debian)
- ✅ macOS (com Python instalado)
- ✅ Resolução mínima: 1024x768

## 🎓 Treinamento

O sistema inclui manual completo de treinamento com:
- Fluxo de trabalho diário
- Operações passo a passo
- Dicas e boas práticas
- Solução de problemas
- Treinamento por níveis (3 semanas)

## 📞 Suporte

- **Documentação**: Arquivos .md inclusos
- **Issues**: Use o GitHub Issues
- **Atualizações**: Git pull ou download
- **Backup**: Sistema automático integrado

## 🏆 Casos de Uso

### Ideal Para:
- 🍔 Lanchonetes e restaurantes pequenos
- ☕ Cafeterias e padarias
- 🛒 Pequenos comércios
- 📊 Controle financeiro simples
- 👥 Negócios familiares

### Benefícios:
- ⚡ Rapidez nas vendas
- 📊 Controle financeiro completo
- 💾 Dados sempre protegidos
- 📈 Análises para crescimento
- 🎯 Operação profissional

## 🔄 Atualizações

Sistema em desenvolvimento ativo com:
- Novas funcionalidades mensais
- Correções e melhorias
- Documentação atualizada
- Suporte contínuo

## 📜 Licença

MIT License - Use livremente em seus projetos

---

**Desenvolvido para maximizar a eficiência operacional de pequenos negócios**

*Sistema testado e aprovado em ambiente real de lanchonete*
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ README.md atualizado")

def criar_gitignore_completo():
    """Cria .gitignore completo para o projeto"""
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

# Backups
backup_sistema_*/
*.zip

# Ambiente virtual
venv_clean/
"""
    
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore criado")

def main():
    """Função principal"""
    print("🐙 Upload Direto para GitHub")
    print("=" * 40)
    
    # Criar arquivos necessários
    criar_readme_atualizado()
    criar_gitignore_completo()
    
    # Criar backup
    arquivo_backup = criar_backup_projeto()
    
    print("\n" + "=" * 50)
    print("📦 PROJETO PRONTO PARA GITHUB!")
    print("=" * 50)
    
    print(f"\n✅ Arquivo criado: {arquivo_backup}")
    print(f"📏 Tamanho: {os.path.getsize(arquivo_backup) / (1024 * 1024):.2f} MB")
    
    print("\n🔼 COMO FAZER UPLOAD:")
    print("1. Acesse: https://github.com/victorsoaresferreiraa/sistema_lanchonete")
    print("2. Clique em 'Add file' > 'Upload files'")
    print(f"3. Arraste o arquivo: {arquivo_backup}")
    print("4. Escreva mensagem: 'Sistema completo com todas as funcionalidades'")
    print("5. Clique 'Commit changes'")
    
    print("\n📋 ARQUIVOS INCLUÍDOS:")
    print("- Sistema principal completo")
    print("- Documentação técnica")
    print("- Manual de treinamento")
    print("- Scripts de build e execução")
    print("- Código fonte modularizado")
    print("- Testes e utilitários")
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("- Fazer upload do arquivo ZIP no GitHub")
    print("- Extrair arquivos no repositório")
    print("- Atualizar README com informações do projeto")
    print("- Configurar releases e tags")
    
    return arquivo_backup

if __name__ == "__main__":
    main()