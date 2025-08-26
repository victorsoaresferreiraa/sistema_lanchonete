# Guia de Instalação - Sistema de Lanchonete

## Como transformar em executável (.exe)

### Pré-requisitos
1. **Python 3.10 ou superior** instalado no Windows
2. **Git** (opcional, para baixar o código)

### Passos para criar o executável

#### 1. Baixar e preparar o projeto
```bash
# Se você tem o código em uma pasta, navegue até ela
cd caminho/para/sistema-lanchonete

# Ou baixe de um repositório (se aplicável)
# git clone [URL_DO_REPOSITORIO]
# cd sistema-lanchonete
```

#### 2. Instalar dependências
```bash
# Instalar todas as bibliotecas necessárias
pip install pillow tabulate matplotlib pandas openpyxl requests nuitka

# Ou se usar poetry
poetry install
```

#### 3. Executar o script de build
```bash
# Executar o script que criará o executável
python build_exe.py
```

#### 4. Resultado
Após a execução bem-sucedida, você terá:
- **SistemaLanchonete.exe** - O executável principal
- **instalar.bat** - Script de instalação/atualização
- **backup/** - Pasta para backups automáticos

### Distribuindo o sistema

#### Para instalar em outro computador:
1. Copie o arquivo **SistemaLanchonete.exe** para o computador de destino
2. Copie o arquivo **instalar.bat** junto
3. Execute **instalar.bat** como administrador
4. Execute **SistemaLanchonete.exe** para usar o sistema

#### Sistema de atualizações futuras:
- O sistema está preparado para receber atualizações automaticamente
- Cada nova versão pode ser distribuída como um novo executável
- O banco de dados e configurações são preservados entre atualizações
- Backups automáticos são criados antes de cada atualização

### Recursos incluídos no executável:

#### ✅ Funcionalidades implementadas:
- **Controle de estoque completo** com preços, categorias e códigos de barras
- **Sistema de vendas** com cálculo automático de valores
- **Histórico detalhado** de todas as vendas com informações financeiras
- **Exportação para Excel** de relatórios de estoque e vendas
- **Gráficos e estatísticas** de desempenho de vendas
- **Sistema de versionamento** para futuras atualizações
- **Banco de dados SQLite** com migração automática de esquemas
- **Interface intuitiva** com formulários de fácil uso

#### 💰 Sistema de preços integrado:
- Cadastro de preços por produto
- Cálculo automático do valor total das vendas
- Controle do valor total do estoque
- Relatórios financeiros detalhados
- Histórico de preços e receitas

#### 🔄 Sistema de atualizações:
- Verificação automática de novas versões (configurável)
- Backup automático antes de atualizações
- Migração automática do banco de dados
- Preservação de dados entre versões
- Controle de versão interno

### Estrutura de arquivos do executável:
```
SistemaLanchonete.exe    # Aplicação principal
data/                    # Banco de dados e configurações
├── banco.db            # Base de dados SQLite
└── config.json         # Configurações do sistema
assets/                  # Recursos visuais
└── icon.ico            # Ícone da aplicação
backup/                  # Backups automáticos
├── banco_backup_*.db   # Backups do banco
└── SistemaLanchonete_backup_*.exe  # Backups de versões anteriores
```

### Solução de problemas comuns:

#### Erro: "No module named 'X'"
- Execute: `pip install X` onde X é o módulo faltante
- Ou execute: `pip install -r requirements.txt` se houver o arquivo

#### Erro durante o build:
- Verifique se tem espaço suficiente no disco (pelo menos 500MB)
- Execute como administrador
- Verifique se o antivírus não está bloqueando

#### Sistema não abre no Windows:
- Instale o Microsoft Visual C++ Redistributable
- Execute como administrador
- Verifique se o Windows Defender não está bloqueando

#### Banco de dados corrompido:
- O sistema automaticamente cria backups
- Restaure de um backup em `backup/banco_backup_*.db`
- Substitua o arquivo `data/banco.db` pelo backup

### Próximas atualizações planejadas:
- Sistema de relatórios mais avançados
- Integração com impressoras para cupons
- Sistema de fornecedores e compras
- Controle de usuários múltiplos
- Aplicativo mobile complementar
- Integração com sistema de pagamentos

### Suporte:
Para problemas técnicos ou sugestões de melhorias, mantenha um registro das mensagens de erro e versão do sistema em uso.