# 🍔 Sistema de Gestão de Lanchonete

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
