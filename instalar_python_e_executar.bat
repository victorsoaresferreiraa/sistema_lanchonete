@echo off
echo ========================================
echo   INSTALADOR AUTOMATICO - LANCHONETE
echo ========================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Python ja esta instalado!
    goto :executar_sistema
)

echo [INFO] Python nao encontrado. Instalando automaticamente...
echo.

REM Criar pasta temporaria para downloads
if not exist "temp_install" mkdir temp_install
cd temp_install

echo [1/4] Baixando Python 3.11.9 (64-bit)...
echo Aguarde, fazendo download do Python...

REM Baixar Python usando PowerShell (funciona no Windows 10/11)
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python_installer.exe'}"

if not exist "python_installer.exe" (
    echo [ERRO] Falha ao baixar Python. Verifique sua conexao com internet.
    echo.
    echo SOLUCAO MANUAL:
    echo 1. Baixe Python em: https://www.python.org/downloads/
    echo 2. Instale marcando "Add Python to PATH"
    echo 3. Execute este arquivo novamente
    pause
    exit /b 1
)

echo [2/4] Instalando Python...
echo IMPORTANTE: O instalador ira abrir. Marque "Add Python to PATH"!
echo.
pause

REM Instalar Python silenciosamente com PATH
python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

echo [3/4] Aguardando instalacao finalizar...
timeout /t 30 >nul

echo [4/4] Verificando instalacao...
REM Atualizar PATH para sessao atual
set PATH=%PATH%;C:\Program Files\Python311;C:\Program Files\Python311\Scripts
set PATH=%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\Scripts

REM Testar novamente
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCESSO] Python instalado com sucesso!
) else (
    echo [AVISO] Pode ser necessario reiniciar o computador.
    echo Execute este arquivo novamente apos reiniciar.
    pause
    exit /b 1
)

REM Limpar arquivos temporarios
cd ..
rmdir /s /q temp_install

:executar_sistema
echo.
echo ========================================
echo      INICIANDO SISTEMA LANCHONETE
echo ========================================
echo.

REM Instalar dependencias necessarias
echo [SETUP] Instalando bibliotecas necessarias...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install pandas openpyxl matplotlib pillow >nul 2>&1

REM Verificar se arquivo principal existe
if not exist "main_funcional.py" (
    echo [ERRO] Arquivo main_funcional.py nao encontrado!
    echo Certifique-se de estar na pasta correta do sistema.
    pause
    exit /b 1
)

REM Executar sistema
echo [INICIAR] Abrindo Sistema de Lanchonete...
echo.
echo ATALHOS RAPIDOS:
echo F1 = Ajuda    F2 = Venda a Vista    F3 = Venda Fiado
echo ESC = Fechar  Enter = Adicionar     F4 = Limpar
echo.

python main_funcional.py

echo.
echo Sistema finalizado. Pressione qualquer tecla para sair.
pause >nul