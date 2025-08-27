@echo off
echo ================================
echo  Sistema de Gerenciamento 
echo      da Lanchonete v2.0
echo ================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao esta instalado!
    echo.
    echo Por favor, instale o Python 3.8+ de: https://python.org
    pause
    exit /b 1
)

REM Verificar se o arquivo principal existe
if not exist "main.py" (
    echo ERRO: main.py nao encontrado!
    echo.
    echo Execute este arquivo na pasta do sistema.
    pause
    exit /b 1
)

REM Instalar dependências se necessário
echo Verificando dependencias...
pip install --quiet pandas matplotlib openpyxl pillow tabulate requests

REM Executar o sistema
echo.
echo Iniciando sistema da lanchonete...
echo.
python main.py

REM Pausar se houve erro
if errorlevel 1 (
    echo.
    echo ERRO: Falha ao executar o sistema!
    pause
)