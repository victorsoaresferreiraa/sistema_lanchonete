# 📋 Instruções de Instalação - Sistema da Lanchonete

## 🚀 Opção 1: Executável (.exe) - RECOMENDADO

### Usando PyInstaller (Alternativa ao Nuitka)

**O problema do Nuitka:** O erro que você teve é comum - falha no download dos compiladores.

**Solução:** Use o PyInstaller que é mais estável:

```bash
# 1. Instalar PyInstaller
pip install pyinstaller

# 2. Executar o script alternativo
python build_pyinstaller.py
```

O script vai:
- ✅ Instalar PyInstaller automaticamente se necessário
- ✅ Criar um ícone para o sistema
- ✅ Empacotar tudo em um único arquivo .exe
- ✅ Incluir todas as dependências
- ✅ Funcionar offline sem Python instalado

---

## 🔧 Opção 2: Solução Imediata - Arquivo .bat

**Para usar HOJE na lanchonete:**

1. Copie todos os arquivos do sistema para o computador da lanchonete
2. Execute o arquivo `executar_lanchonete.bat`
3. O sistema inicia automaticamente!

O arquivo .bat:
- ✅ Verifica se Python está instalado
- ✅ Instala dependências automaticamente
- ✅ Executa o sistema
- ✅ Funciona imediatamente

---

## 🐍 Opção 3: Execução Direta

Se tiver Python instalado:

```bash
# Instalar dependências
pip install pandas matplotlib openpyxl pillow tabulate requests

# Executar sistema
python main.py
```

---

## 🛠️ Correção do Erro do Nuitka

Se quiser tentar o Nuitka novamente:

1. **Limpar cache:**
   ```
   # Windows
   rmdir /s "%LOCALAPPDATA%\Nuitka\Nuitka\Cache"
   
   # Ou manualmente apagar a pasta:
   C:\Users\[SEU_USUARIO]\AppData\Local\Nuitka\Nuitka\Cache
   ```

2. **Usar conexão estável:**
   - Conecte cabo de rede (não Wi-Fi)
   - Desative antivírus temporariamente
   - Execute como administrador

3. **Executar novamente:**
   ```bash
   python build_exe.py
   ```

---

## 📱 Instalação na Lanchonete

### Para usar profissionalmente:

1. **Copie a pasta completa do sistema** para o computador da lanchonete
2. **Execute `executar_lanchonete.bat`** - funciona imediatamente
3. **Ou execute `python build_pyinstaller.py`** para criar o .exe
4. **Crie atalho na área de trabalho** para facilitar o acesso

### Estrutura necessária:
```
📁 sistema_lanchonete/
├── 📄 main.py
├── 📄 executar_lanchonete.bat  ← Execute este!
├── 📄 build_pyinstaller.py     ← Ou este para criar .exe
├── 📁 src/
├── 📁 data/
├── 📁 assets/
└── 📄 requirements.txt
```

---

## ✅ Validação

Teste todas as funções:
1. ✅ Cadastrar produtos com preços
2. ✅ Registrar vendas
3. ✅ Consultar estoque
4. ✅ Ver histórico com valores
5. ✅ Exportar relatórios
6. ✅ Gerar gráficos financeiros

---

## 🆘 Suporte

**Se der qualquer erro:**
1. Execute `executar_lanchonete.bat` - é a opção mais estável
2. Verifique se todos os arquivos estão na pasta
3. Instale Python 3.8+ se necessário

**O sistema está pronto para uso profissional!** 🎉