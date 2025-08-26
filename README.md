# Sistema de Gerenciamento de Lanchonete

Um sistema completo para gerenciamento de lanchonetes, desenvolvido em Python com interface gráfica Tkinter. O sistema oferece controle de estoque, registro de vendas, exportação de dados e visualização de gráficos.

## 🚀 Características

### Funcionalidades Principais
- **Controle de Estoque**: Adicione, atualize e remova produtos do estoque
- **Registro de Vendas**: Registre vendas automaticamente atualizando o estoque
- **Histórico Completo**: Visualize todas as vendas realizadas com filtros
- **Exportação de Dados**: Exporte relatórios em formato Excel
- **Gráficos**: Visualize estatísticas de vendas em gráficos interativos
- **Interface Intuitiva**: Design limpo e responsivo com Tkinter

### Recursos Técnicos
- **Banco de Dados SQLite**: Armazenamento local seguro
- **Arquitetura Modular**: Código organizado e fácil de manter
- **Validação de Dados**: Verificação robusta de entradas
- **Tratamento de Erros**: Sistema resiliente com mensagens claras
- **Empacotamento Executável**: Geração de .exe para Windows

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.10+**: Linguagem principal
- **SQLite**: Banco de dados local
- **Tkinter/ttk**: Interface gráfica
- **Pandas**: Manipulação de dados
- **Matplotlib**: Geração de gráficos

### Bibliotecas Específicas
- **Pillow**: Manipulação de imagens
- **Tabulate**: Formatação de tabelas
- **OpenPyXL**: Exportação para Excel
- **Nuitka**: Empacotamento executável

### Ferramentas de Desenvolvimento
- **Poetry**: Gerenciamento de dependências
- **Pytest**: Framework de testes
- **Black**: Formatação de código
- **Flake8**: Análise de código
- **MyPy**: Verificação de tipos

## 📦 Instalação

### Pré-requisitos
- Python 3.10 ou superior
- Poetry (recomendado) ou pip

### Opção 1: Usando Poetry (Recomendado)
```bash
# Clonar o repositório
git clone <repository-url>
cd sistema-lanchonete

# Instalar dependências
poetry install

# Ativar ambiente virtual
poetry shell

# Executar aplicação
poetry run python main.py
