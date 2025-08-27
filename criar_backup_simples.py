"""
Backup simples do projeto para sincronização
"""

import os
import shutil
from datetime import datetime

def criar_backup():
    """Cria uma cópia organizada do projeto"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta_backup = f"backup_sistema_{timestamp}"
    
    print(f"📦 Criando backup em: {pasta_backup}")
    
    # Criar pasta de backup
    os.makedirs(pasta_backup, exist_ok=True)
    
    # Arquivos principais
    arquivos_importantes = [
        'main.py',
        'requirements.txt',
        'pyproject.toml',
        'executar_lanchonete.bat',
        'build_pyinstaller.py',
        'build_exe.py',
        'README.md',
        'DOCUMENTACAO_COMPLETA.md',
        'INSTRUCOES_INSTALACAO.md',
        'GUIA_GITHUB.md',
        'INSTRUCOES_SINCRONIZACAO.md',
        'manual_instalar.md'
    ]
    
    # Copiar arquivos
    for arquivo in arquivos_importantes:
        if os.path.exists(arquivo):
            shutil.copy2(arquivo, pasta_backup)
            print(f"✅ {arquivo}")
    
    # Copiar pastas importantes
    pastas_importantes = ['src', 'tests', 'assets']
    
    for pasta in pastas_importantes:
        if os.path.exists(pasta):
            shutil.copytree(pasta, os.path.join(pasta_backup, pasta))
            print(f"✅ {pasta}/")
    
    # Criar estrutura data sem dados sensíveis
    data_backup = os.path.join(pasta_backup, 'data')
    os.makedirs(data_backup, exist_ok=True)
    with open(os.path.join(data_backup, '.gitkeep'), 'w') as f:
        f.write('# Manter pasta data no repositório\n')
    print("✅ data/ (estrutura)")
    
    # Criar arquivo de informações
    info = f"""# Backup do Sistema da Lanchonete

**Data do backup:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
**Versão:** 2.0.0
**Repositório:** https://github.com/victorsoaresferreiraa/sistema_lanchonete

## Conteúdo deste backup:

### Arquivos principais:
- main.py - Arquivo principal do sistema
- executar_lanchonete.bat - Execução rápida
- build_pyinstaller.py - Criar executável .exe

### Documentação:
- DOCUMENTACAO_COMPLETA.md - Manual técnico completo
- INSTRUCOES_INSTALACAO.md - Como instalar e usar
- GUIA_GITHUB.md - Como usar Git/GitHub
- README.md - Descrição do projeto

### Código fonte:
- src/ - Todo o código organizado em módulos
- tests/ - Testes do sistema
- assets/ - Recursos visuais

### Para usar este backup:
1. Copie todos os arquivos para uma pasta
2. Execute: pip install -r requirements.txt
3. Execute: python main.py
4. Ou use: executar_lanchonete.bat

### Para enviar ao GitHub:
1. Acesse: https://github.com/victorsoaresferreiraa/sistema_lanchonete
2. Upload todos estes arquivos
3. Commit: "🔄 Atualização completa do sistema"

## Status atual:
✅ Sistema completo e funcional
✅ Preços integrados em todos os processos  
✅ Documentação técnica completa
✅ Scripts de empacotamento funcionais
✅ Pronto para uso profissional na lanchonete
"""
    
    with open(os.path.join(pasta_backup, 'INFO_BACKUP.md'), 'w', encoding='utf-8') as f:
        f.write(info)
    
    print(f"\n🎉 Backup criado com sucesso!")
    print(f"📁 Pasta: {pasta_backup}")
    
    # Listar conteúdo
    print(f"\n📋 Conteúdo do backup:")
    for root, dirs, files in os.walk(pasta_backup):
        level = root.replace(pasta_backup, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")
    
    return pasta_backup

if __name__ == "__main__":
    print("🔄 Criando backup para sincronização com GitHub")
    print("=" * 50)
    
    pasta = criar_backup()
    
    print("\n💡 Próximos passos:")
    print("1. 📁 Baixe a pasta de backup criada")
    print("2. 🌐 Acesse: https://github.com/victorsoaresferreiraa/sistema_lanchonete")
    print("3. 📤 Upload todos os arquivos da pasta backup")
    print("4. ✅ Sistema sincronizado!")