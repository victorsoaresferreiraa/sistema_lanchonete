#!/usr/bin/env python3
"""
Script para criar pacote de sincronização com VS Code
Copia todos os arquivos importantes para uma pasta organizada
"""

import os
import shutil
import zipfile
from datetime import datetime

def criar_pacote_vscode():
    """Cria pacote organizado para sincronizar com VS Code"""
    
    print("📦 Criando pacote para sincronização VS Code...")
    
    # Nome da pasta de sincronização
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta_sync = f"sync_vscode_{timestamp}"
    
    # Criar estrutura de pastas
    os.makedirs(pasta_sync, exist_ok=True)
    os.makedirs(f"{pasta_sync}/documentacao", exist_ok=True)
    os.makedirs(f"{pasta_sync}/protecao_comercial", exist_ok=True)
    os.makedirs(f"{pasta_sync}/ferramentas", exist_ok=True)
    os.makedirs(f"{pasta_sync}/codigo_fonte", exist_ok=True)
    
    # Arquivos principais para copiar
    arquivos_principais = {
        # Arquivo principal (CRÍTICO)
        "main_funcional.py": "main_funcional.py",
        "main.py": "main.py",
        "README.md": "README.md",
        ".gitignore": ".gitignore",
        "pyproject.toml": "pyproject.toml",
        
        # Documentação
        "MANUAL_TREINAMENTO_SISTEMA_LANCHONETE.md": "documentacao/",
        "DOCUMENTACAO_COMPLETA.md": "documentacao/",
        "DOCUMENTACAO_TECNICA_COMPLETA.md": "documentacao/",
        "GUIA_PROGRAMADOR_EXCELENTE.md": "documentacao/",
        "GUIA_LICENCIAMENTO.md": "documentacao/",
        "GUIA_GITHUB.md": "documentacao/",
        "INSTRUCOES_INSTALACAO.md": "documentacao/",
        "INSTRUCOES_SINCRONIZACAO.md": "documentacao/",
        "AJUSTES_LAYOUT_DASHBOARD.md": "documentacao/",
        "DASHBOARD_COMPLETO.md": "documentacao/",
        "SOLUCAO_AMBIENTE_VIRTUAL.md": "documentacao/",
        
        # Curso Completo de Python
        "CURSO_PYTHON_COMPLETO.md": "documentacao/",
        "CURSO_PYTHON_PARTE2.md": "documentacao/",
        "CURSO_PYTHON_RESUMO_COMPLETO.md": "documentacao/",
        
        # Proteção comercial
        "protecao_comercial.py": "protecao_comercial/",
        "exemplo_licenciamento.py": "protecao_comercial/",
        "license_system.py": "protecao_comercial/",
        "build_commercial.py": "protecao_comercial/",
        
        # Ferramentas
        "executar_lanchonete.bat": "ferramentas/",
        "build_pyinstaller.py": "ferramentas/",
        "sincronizar_github.py": "ferramentas/",
        "upload_github_direto.py": "ferramentas/",
        "setup_git.py": "ferramentas/",
        "atualizar_github.bat": "ferramentas/",
        
        # Testes
        "test_simples.py": "codigo_fonte/",
        "test_dashboard_demo.py": "codigo_fonte/",
    }
    
    # Copiar arquivos
    arquivos_copiados = 0
    for origem, destino in arquivos_principais.items():
        if os.path.exists(origem):
            if destino.endswith("/"):
                destino_completo = os.path.join(pasta_sync, destino, origem)
            else:
                destino_completo = os.path.join(pasta_sync, destino)
            
            # Criar diretório se necessário
            os.makedirs(os.path.dirname(destino_completo), exist_ok=True)
            
            # Copiar arquivo
            shutil.copy2(origem, destino_completo)
            print(f"✓ Copiado: {origem} → {destino_completo}")
            arquivos_copiados += 1
        else:
            print(f"⚠️  Não encontrado: {origem}")
    
    # Copiar pasta src/ se existir
    if os.path.exists("src"):
        shutil.copytree("src", f"{pasta_sync}/codigo_fonte/src", dirs_exist_ok=True)
        print("✓ Copiada pasta: src/")
    
    # Copiar pasta assets/ se existir
    if os.path.exists("assets"):
        shutil.copytree("assets", f"{pasta_sync}/assets", dirs_exist_ok=True)
        print("✓ Copiada pasta: assets/")
    
    # Copiar pasta tests/ se existir
    if os.path.exists("tests"):
        shutil.copytree("tests", f"{pasta_sync}/codigo_fonte/tests", dirs_exist_ok=True)
        print("✓ Copiada pasta: tests/")
    
    # Criar arquivo de instruções
    criar_instrucoes_sync(pasta_sync)
    
    # Criar configuração Poetry
    criar_poetry_config(pasta_sync)
    
    # Criar ZIP final
    nome_zip = f"{pasta_sync}.zip"
    with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(pasta_sync):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, pasta_sync)
                zipf.write(file_path, arc_path)
    
    # Calcular tamanhos
    tamanho_pasta = sum(os.path.getsize(os.path.join(dirpath, filename))
                       for dirpath, dirnames, filenames in os.walk(pasta_sync)
                       for filename in filenames) / (1024 * 1024)
    
    tamanho_zip = os.path.getsize(nome_zip) / (1024 * 1024)
    
    print(f"\n✅ Pacote criado com sucesso!")
    print(f"📁 Pasta: {pasta_sync} ({tamanho_pasta:.2f} MB)")
    print(f"📦 ZIP: {nome_zip} ({tamanho_zip:.2f} MB)")
    print(f"📋 Arquivos: {arquivos_copiados}")
    
    return pasta_sync, nome_zip

def criar_instrucoes_sync(pasta_sync):
    """Cria arquivo de instruções para sincronização"""
    
    instrucoes = """# 🔄 INSTRUÇÕES DE SINCRONIZAÇÃO

## 📋 Conteúdo deste Pacote

### 📁 Estrutura das Pastas:
- `main_funcional.py` - Sistema principal COMPLETO
- `documentacao/` - Todos os manuais e guias
- `protecao_comercial/` - Sistema de licenças
- `ferramentas/` - Scripts de build e sync
- `codigo_fonte/` - Código modular e testes
- `assets/` - Recursos visuais

## 🚀 Como Sincronizar

### Passo 1: Backup
```bash
# Faça backup do seu projeto atual
cp -r seu_projeto/ backup_$(date +%Y%m%d)/ 
```

### Passo 2: Substituir Arquivos Principais
1. **CRÍTICO**: Substitua `main_funcional.py` 
2. Atualize `README.md`
3. Substitua `.gitignore`

### Passo 3: Adicionar Documentação
- Copie toda pasta `documentacao/` para seu projeto
- Especial atenção ao `MANUAL_TREINAMENTO_SISTEMA_LANCHONETE.md`

### Passo 4: Sistema Comercial (Opcional)
- Copie pasta `protecao_comercial/` se for vender
- Configure chaves de licença conforme necessário

### Passo 5: Dependências
```bash
# Com Poetry (recomendado)
poetry install

# OU com pip (alternativa)
pip install -r requirements.txt
```

### Passo 6: Testar
```bash
# Com Poetry
poetry run python main_funcional.py

# OU direto
python main_funcional.py
```

## ✨ Principais Novidades

### Sistema de Caixa Avançado
- Abertura/fechamento com relatórios
- Sangria e reforço controlados
- Movimentações rastreadas

### Backup e Sincronização
- Backup completo automático
- Exportação Excel multi-abas
- Histórico de backups

### Contas em Aberto (Crediário)
- Vendas fiado com cliente
- Controle vencimentos
- Status pagamento

### Documentação Técnica Completa
- `DOCUMENTACAO_TECNICA_COMPLETA.md` - Arquitetura do sistema
- `GUIA_PROGRAMADOR_EXCELENTE.md` - Padrões de programação
- Explicação de 10+ padrões de design aplicados
- Análise completa da arquitetura MVC

### Curso Completo de Python
- `CURSO_PYTHON_COMPLETO.md` - 40 aulas estruturadas
- `CURSO_PYTHON_PARTE2.md` - Interface Tkinter avançada
- `CURSO_PYTHON_RESUMO_COMPLETO.md` - Visão geral de 8 módulos
- 16 semanas de conteúdo do básico ao avançado
- Baseado 100% no projeto da lanchonete

### Manual Completo
- 300+ linhas de treinamento
- Fluxo de trabalho diário
- Solução de problemas

### Sistema de Licenciamento
- Chaves únicas por cliente
- Validação automática
- Proteção comercial

## 🆘 Se Algo Der Errado

1. **Restaure backup**: `cp -r backup_*/ seu_projeto/`
2. **Compare arquivos**: Use diff para ver diferenças
3. **Teste individual**: Execute cada módulo separadamente
4. **Verifique deps**: `pip list` para conferir bibliotecas

## 📞 Suporte

- Documentação completa na pasta `documentacao/`
- Exemplos práticos em `protecao_comercial/`
- Scripts de build em `ferramentas/`

**Boa sincronização!** 🚀
"""
    
    with open(f"{pasta_sync}/LEIA_PRIMEIRO.md", "w", encoding="utf-8") as f:
        f.write(instrucoes)

def criar_poetry_config(pasta_sync):
    """Cria configuração Poetry atualizada"""
    
    # Copiar pyproject.toml existente
    if os.path.exists("pyproject.toml"):
        shutil.copy2("pyproject.toml", f"{pasta_sync}/pyproject.toml")
        print("✓ Copiado: pyproject.toml (Poetry)")
    
    # Criar requirements.txt para compatibilidade
    requirements = """# Sistema de Lanchonete - Para quem não usa Poetry
# Use: pip install -r requirements.txt
# OU: poetry install (recomendado)

pandas>=1.5.0
openpyxl>=3.0.0
matplotlib>=3.5.0
tabulate>=0.9.0
pyinstaller>=5.0
pytest>=7.0.0
pytest-cov>=4.0.0
black>=22.0.0
flake8>=5.0.0
mypy>=1.0.0
nuitka>=1.0.0
"""
    
    with open(f"{pasta_sync}/requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements)

def main():
    """Função principal"""
    print("🔄 CRIADOR DE PACOTE VS CODE")
    print("=" * 40)
    
    try:
        pasta, zip_file = criar_pacote_vscode()
        
        print(f"\n📦 PACOTE PRONTO!")
        print(f"📁 Pasta: {pasta}")
        print(f"📦 ZIP: {zip_file}")
        
        print(f"\n🚀 PRÓXIMOS PASSOS:")
        print(f"1. Baixe o arquivo: {zip_file}")
        print(f"2. Extraia no seu computador")
        print(f"3. Leia o arquivo: LEIA_PRIMEIRO.md")
        print(f"4. Sincronize com seu VS Code")
        print(f"5. Teste o sistema: python main_funcional.py")
        
        print(f"\n✨ FUNCIONALIDADES INCLUÍDAS:")
        print(f"- Sistema de caixa avançado")
        print(f"- Backup e sincronização")
        print(f"- Contas em aberto (crediário)")
        print(f"- Manual de treinamento completo")
        print(f"- Sistema de licenciamento comercial")
        print(f"- Documentação técnica atualizada")
        
        return pasta, zip_file
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None, None

if __name__ == "__main__":
    main()