"""
Sistema de backup e sincronização para GitHub
Funciona independentemente das limitações do Git no Replit
"""

import os
import zipfile
import json
from datetime import datetime
import subprocess

def criar_backup_completo():
    """Cria backup completo do projeto"""
    print("📦 Criando backup completo do projeto...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_backup = f"sistema_lanchonete_backup_{timestamp}.zip"
    
    # Arquivos e pastas para incluir
    incluir = [
        'main.py',
        'src/',
        'tests/',
        'assets/',
        'requirements.txt',
        'pyproject.toml',
        '*.md',
        '*.py',
        '*.bat',
        '*.sh',
        'data/.gitkeep'  # Estrutura da pasta data, sem dados
    ]
    
    # Arquivos para excluir
    excluir = [
        '__pycache__',
        '.git',
        '.replit',
        '.config',
        '.pythonlibs',
        '.cache',
        '.local',
        'data/*.db',  # Não incluir dados reais
        'data/*.xlsx',
        'data/*.png',
        '*.log',
        '*.tmp'
    ]
    
    try:
        with zipfile.ZipFile(nome_backup, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk('.'):
                # Filtrar diretórios a excluir
                dirs[:] = [d for d in dirs if not any(ex in os.path.join(root, d) for ex in excluir)]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Verificar se deve incluir o arquivo
                    if not any(ex in file_path for ex in excluir):
                        # Incluir arquivos relevantes
                        if any(inc.replace('*', '') in file_path or file_path.endswith(inc.replace('*', '')) for inc in incluir):
                            zipf.write(file_path, file_path)
        
        tamanho = os.path.getsize(nome_backup) / (1024 * 1024)  # MB
        print(f"✅ Backup criado: {nome_backup} ({tamanho:.1f} MB)")
        return nome_backup
        
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        return None

def gerar_relatorio_mudancas():
    """Gera relatório das mudanças recentes"""
    print("📋 Gerando relatório de mudanças...")
    
    relatorio = {
        "timestamp": datetime.now().isoformat(),
        "versao": "2.0.0",
        "mudancas_recentes": [
            "🔧 Sistema de sincronização com GitHub implementado",
            "📚 Documentação completa de 94 páginas criada",
            "🔄 Scripts de empacotamento PyInstaller e Nuitka",
            "💰 Sistema de preços integrado em todos os processos",
            "📊 Base para dashboard financeiro preparada",
            "🛠️ Scripts de backup e atualização automática",
            "📁 Estrutura modular organizada para manutenção",
            "✅ Sistema pronto para uso profissional na lanchonete"
        ],
        "arquivos_principais": [
            "main.py - Arquivo principal do sistema",
            "src/interface/main_window.py - Interface principal",
            "src/estoque/database.py - Gerenciamento do banco",
            "src/pedidos/controller.py - Lógica de vendas",
            "DOCUMENTACAO_COMPLETA.md - Documentação técnica",
            "executar_lanchonete.bat - Execução rápida",
            "build_pyinstaller.py - Criação de executável"
        ],
        "proximos_passos": [
            "Conectar com repositório GitHub existente",
            "Implementar dashboard avançado de análise",
            "Sistema de usuários e permissões",
            "Alertas automáticos de estoque baixo",
            "Backup automático agendado",
            "Integração com APIs de fornecedores"
        ]
    }
    
    nome_relatorio = f"relatorio_projeto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(nome_relatorio, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Relatório criado: {nome_relatorio}")
        return relatorio
        
    except Exception as e:
        print(f"❌ Erro ao criar relatório: {e}")
        return None

def gerar_instrucoes_para_github():
    """Gera instruções detalhadas para sincronizar com GitHub"""
    print("📝 Gerando instruções para GitHub...")
    
    instrucoes = """# 🔄 Como Sincronizar Este Projeto com seu GitHub

## 📥 Para BAIXAR este projeto para seu GitHub:

### Método 1: Upload Direto (Mais Simples)
1. **Baixe o backup:** `sistema_lanchonete_backup_XXXXXX.zip`
2. **Acesse:** https://github.com/victorsoaresferreiraa/sistema_lanchonete
3. **Clique:** "Upload files"
4. **Arraste:** todo o conteúdo do zip descompactado
5. **Commit:** "🔄 Atualização completa do sistema da lanchonete"

### Método 2: Git Clone + Replace (Mais Técnico)
```bash
# No seu computador local:
git clone https://github.com/victorsoaresferreiraa/sistema_lanchonete.git
cd sistema_lanchonete

# Substituir arquivos com os novos
# (copiar arquivos do backup para esta pasta)

git add .
git commit -m "🔄 Atualização completa - versão 2.0"
git push origin main
```

## 📤 Para FUTURAS ATUALIZAÇÕES:

### Quando Trabalhar no Replit:
1. **Execute:** `python backup_github.py`
2. **Baixe** o backup gerado
3. **Faça upload** no GitHub

### Quando Trabalhar Localmente:
1. **Faça** suas modificações
2. **Commit e push** normalmente
3. **Compartilhe** mudanças importantes comigo

## 📋 Arquivos Importantes que DEVEM ir para GitHub:
- ✅ Todos os arquivos .py (código fonte)
- ✅ Toda pasta src/ (módulos do sistema)
- ✅ Documentação (.md files)
- ✅ Scripts de build (.py, .bat, .sh)
- ✅ requirements.txt
- ✅ Estrutura de pastas

## ❌ Arquivos que NÃO devem ir para GitHub:
- ❌ data/*.db (banco com dados reais)
- ❌ Relatórios gerados (.xlsx, .png)
- ❌ Configurações do Replit (.replit, .config/)
- ❌ Arquivos temporários (__pycache__, .tmp)

## 🎯 Resultado Final:
Seu GitHub terá a versão mais atualizada do sistema, pronta para:
- 💻 Desenvolvimento em qualquer máquina
- 🚀 Deploy profissional
- 👥 Colaboração futura
- 📊 Controle de versão completo
"""
    
    with open('SYNC_GITHUB_INSTRUCTIONS.md', 'w', encoding='utf-8') as f:
        f.write(instrucoes)
    
    print("✅ Instruções criadas: SYNC_GITHUB_INSTRUCTIONS.md")

def main():
    """Executa backup completo para sincronização"""
    print("🔄 Sistema de Backup para Sincronização GitHub")
    print("=" * 55)
    print(f"Repositório: https://github.com/victorsoaresferreiraa/sistema_lanchonete")
    print()
    
    # Criar backup
    backup_file = criar_backup_completo()
    
    # Gerar relatório
    relatorio = gerar_relatorio_mudancas()
    
    # Gerar instruções
    gerar_instrucoes_para_github()
    
    print("\n" + "=" * 55)
    print("✅ Backup completo gerado!")
    print("\n📋 Próximos passos:")
    print("1. 📥 Baixe o arquivo de backup gerado")
    print("2. 🌐 Acesse seu GitHub: https://github.com/victorsoaresferreiraa/sistema_lanchonete")
    print("3. 📤 Faça upload dos arquivos (seguir SYNC_GITHUB_INSTRUCTIONS.md)")
    print("4. 🎉 Sistema sincronizado!")
    
    print("\n💡 Para futuras atualizações:")
    print("   • Execute este script novamente")
    print("   • Baixe o novo backup")
    print("   • Atualize no GitHub")
    
    if backup_file:
        print(f"\n📦 Arquivo de backup: {backup_file}")
    
    return backup_file is not None

if __name__ == "__main__":
    main()