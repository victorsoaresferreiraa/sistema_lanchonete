# 🚀 Comandos para Executar no VS Code

## 📁 Abrir Terminal no VS Code

1. **Ctrl + `** (abre terminal integrado)
2. **Ou**: Menu Terminal → New Terminal
3. **Navegue** até a pasta do projeto

## 🐍 Comandos Poetry (Recomendado)

### Instalar Dependências
```bash
# Instalar todas as dependências
poetry install

# Se der erro de versão Python
poetry env use python3.10
poetry install
```

### Executar o Sistema
```bash
# Comando principal (recomendado)
poetry run python main_funcional.py

# Ou ativar ambiente primeiro
poetry shell
python main_funcional.py
```

### Verificar Ambiente
```bash
# Ver informações do ambiente
poetry env info

# Ver dependências instaladas
poetry show

# Ver versão Python sendo usada
poetry run python --version
```

## 💻 Comandos Alternativos (pip)

### Se Poetry não funcionar
```bash
# Instalar dependências direto
pip install pandas matplotlib openpyxl tabulate pillow

# Executar sistema
python main_funcional.py
```

## 🔧 Solução de Problemas

### Se der erro de módulo não encontrado:
```bash
# Verificar Python ativo
python --version
where python

# Reinstalar dependências
poetry env remove python
poetry install
```

### Se der erro de permissão:
```bash
# No Windows (como administrador)
poetry run python main_funcional.py

# Ou ativar ambiente manualmente
poetry shell
```

## ⚡ Comandos Rápidos

### Executar Sistema
```bash
poetry run python main_funcional.py
```

### Gerar Executável
```bash
poetry run python build_pyinstaller.py
```

### Executar Testes
```bash
poetry run pytest
```

### Verificar Código
```bash
poetry run black .
poetry run flake8
```

## 🎯 Sequência Recomendada

1. **Abrir terminal** no VS Code (Ctrl + `)
2. **Navegar** para pasta do projeto
3. **Instalar**: `poetry install`
4. **Executar**: `poetry run python main_funcional.py`

## 📋 Se Nada Funcionar

### Método direto (sem Poetry):
```bash
# Instalar Python puro
pip install pandas==2.0.3 matplotlib==3.7.5 numpy==1.24.4 openpyxl==3.1.2

# Executar direto
python main_funcional.py
```

### Verificar instalação:
```bash
# Testar imports
python -c "import pandas, matplotlib, tkinter; print('OK')"
```

**O comando principal é: `poetry run python main_funcional.py`**