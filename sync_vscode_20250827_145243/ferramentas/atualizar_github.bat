@echo off
echo ================================
echo   Atualizando Sistema GitHub
echo ================================
echo.

REM Verificar se Git está configurado
git --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Git não está instalado!
    echo Baixe de: https://git-scm.com/downloads
    pause
    exit /b 1
)

REM Verificar se há mudanças
echo Verificando mudanças...
git status --porcelain > temp_status.txt
set /p changes=<temp_status.txt
del temp_status.txt

if "%changes%"=="" (
    echo ✅ Nenhuma mudança para enviar.
    echo Seu código já está atualizado no GitHub!
    pause
    exit /b 0
)

echo 📋 Mudanças encontradas:
git status --short

echo.
REM Adicionar mudanças
echo ➕ Adicionando mudanças...
git add .

REM Commit com timestamp
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "MIN=%dt:~10,2%" & set "SS=%dt:~12,2%"
set "timestamp=%DD%/%MM%/%YYYY% %HH%:%MIN%"

echo.
set /p "mensagem=💬 Digite a mensagem do commit (ou Enter para automática): "
if "%mensagem%"=="" set "mensagem=🔄 Atualização sistema lanchonete - %timestamp%"

echo.
echo 💾 Fazendo commit...
git commit -m "%mensagem%"

if errorlevel 1 (
    echo ❌ Erro no commit
    pause
    exit /b 1
)

REM Enviar para GitHub
echo 📤 Enviando para GitHub...
git push

if %errorlevel% equ 0 (
    echo.
    echo ✅ Atualização enviada para GitHub com sucesso!
    echo 🌐 Acesse seu repositório para ver as mudanças
) else (
    echo.
    echo ❌ Erro ao enviar para GitHub
    echo 💡 Possíveis soluções:
    echo    1. Verificar conexão com internet
    echo    2. Verificar se está logado no GitHub
    echo    3. Executar: git config --global credential.helper manager
)

echo.
echo 📊 Status atual:
git log --oneline -3

echo.
pause