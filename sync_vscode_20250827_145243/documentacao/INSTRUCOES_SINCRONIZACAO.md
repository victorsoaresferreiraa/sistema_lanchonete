# 🔄 Instruções de Sincronização - Replit ↔ GitHub

## 🎯 Objetivo
Manter seu código sincronizado entre:
- **Replit** (onde você trabalha comigo)
- **GitHub** (seu repositório principal)
- **Computador local** (quando você trabalha sozinho)

---

## 🚀 Como Sincronizar (3 Métodos)

### Método 1: Script Python (Recomendado)
```bash
python sincronizar_github.py
```
**Interface amigável com menu:**
- 🔄 Sincronização completa (baixar + enviar)
- 📤 Apenas enviar mudanças
- 📥 Apenas baixar mudanças

### Método 2: Script Shell (Rápido)
```bash
./sync_github.sh
```
**Sincronização automática em um comando**

### Método 3: Comandos Git Manuais
```bash
# Baixar mudanças do GitHub
git pull origin main

# Enviar mudanças para GitHub
git add .
git commit -m "Suas mudanças"
git push origin main
```

---

## 🔄 Fluxo de Trabalho Recomendado

### Quando Começar a Trabalhar no Replit:
1. **Execute:** `python sincronizar_github.py`
2. **Escolha:** Opção 1 (sincronização completa)
3. **Trabalhe** normalmente no código

### Quando Terminar de Trabalhar:
1. **Execute:** `python sincronizar_github.py`
2. **Escolha:** Opção 2 (enviar mudanças)
3. **Confirme** que código está no GitHub

### Quando Trabalhar no Computador Local:
1. **Clone ou pull** do GitHub
2. **Faça suas mudanças**
3. **Commit e push** para GitHub
4. **Na próxima vez no Replit:** execute sincronização

---

## 📁 O que é Sincronizado

### ✅ Enviado para GitHub:
- Todo código fonte (`src/`, `main.py`, etc.)
- Documentação (`*.md`)
- Scripts de build (`build_*.py`)
- Configurações (`requirements.txt`, etc.)
- Estrutura de pastas

### ❌ NÃO enviado (protegido):
- Banco de dados com dados reais (`data/*.db`)
- Arquivos temporários (`__pycache__/`, `*.tmp`)
- Configurações do Replit (`.replit`, `.config/`)
- Relatórios gerados (`data/*.xlsx`)
- Builds (`build/`, `dist/`)

---

## 🛠️ Configuração Automática

O sistema configura automaticamente:
- ✅ Repositório Git local
- ✅ Conexão com seu GitHub
- ✅ Arquivo `.gitignore` apropriado
- ✅ Estrutura de pastas
- ✅ Proteção de dados sensíveis

**Não precisa configurar manualmente!**

---

## 🚨 Resolução de Conflitos

### Se aparecer "merge conflict":
```bash
# 1. Baixar mudanças
git pull origin main

# 2. Editar arquivos conflitantes
# (procure por <<<<<<< e >>>>>>>)

# 3. Adicionar e commitar
git add .
git commit -m "Resolve conflicts"

# 4. Enviar
git push origin main
```

### Se der erro de autenticação:
1. Verificar se tem acesso ao repositório
2. Usar token de acesso pessoal do GitHub
3. Configurar credenciais: `git config --global credential.helper cache`

---

## 📊 Monitoramento de Mudanças

### Ver status atual:
```bash
git status          # Mudanças locais
git log --oneline -5 # Últimos commits
```

### Ver diferenças:
```bash
git diff            # Mudanças não commitadas
git diff HEAD~1     # Diferença com commit anterior
```

### Ver histórico:
```bash
git log --graph --oneline --all  # Histórico visual
```

---

## 🎯 Cenários Práticos

### Cenário 1: "Trabalhei no Replit, quero atualizar GitHub"
```bash
python sincronizar_github.py
# Escolher opção 2 (enviar)
```

### Cenário 2: "Trabalhei em casa, quero baixar no Replit"
```bash
python sincronizar_github.py
# Escolher opção 3 (baixar)
```

### Cenário 3: "Não sei o que mudou, quero sincronizar tudo"
```bash
python sincronizar_github.py
# Escolher opção 1 (completa)
```

### Cenário 4: "Quero ver se há mudanças sem sincronizar"
```bash
git fetch origin
git log HEAD..origin/main --oneline
```

---

## 🔧 Troubleshooting

### Problema: "Repository not found"
**Solução:** Verificar URL do repositório
```bash
git remote set-url origin https://github.com/victorsoaresferreiraa/sistema_lanchonete.git
```

### Problema: "Permission denied"
**Solução:** Verificar acesso ao repositório no GitHub

### Problema: "Your branch is behind"
**Solução:** Executar pull primeiro
```bash
git pull origin main
```

### Problema: Arquivos grandes
**Solução:** Adicionar ao `.gitignore`
```bash
echo "arquivo_grande.db" >> .gitignore
```

---

## 📱 Integração com Desenvolvimento

### Workflow de Desenvolvimento:
1. **Início do dia:** Sincronizar (baixar)
2. **Durante trabalho:** Commits locais frequentes
3. **Fim do dia:** Sincronizar (enviar)
4. **Branches:** Para funcionalidades grandes

### Branching para funcionalidades:
```bash
# Criar branch para nova funcionalidade
git checkout -b nova-funcionalidade

# Trabalhar na funcionalidade
# ... código ...

# Commit na branch
git add .
git commit -m "Nova funcionalidade implementada"

# Voltar para main e fazer merge
git checkout main
git merge nova-funcionalidade

# Enviar para GitHub
git push origin main
```

---

## ✅ Checklist de Sincronização

Antes de cada sessão:
- [ ] ✅ Executar sincronização para baixar mudanças
- [ ] ✅ Verificar se não há conflitos
- [ ] ✅ Testar código após sincronização

Depois de cada sessão:
- [ ] ✅ Salvar todo o trabalho
- [ ] ✅ Executar sincronização para enviar mudanças
- [ ] ✅ Verificar se push foi bem-sucedido
- [ ] ✅ Confirmar no GitHub que mudanças estão lá

---

## 🎉 Benefícios da Sincronização

### Para Você:
- 🔄 **Trabalhar de qualquer lugar** (Replit, casa, escritório)
- 💾 **Backup automático** no GitHub
- 📱 **Histórico completo** de mudanças
- 👥 **Colaboração** futura com outros desenvolvedores

### Para o Sistema:
- 🔒 **Código sempre seguro** na nuvem
- 📊 **Controle de versão** profissional
- 🚀 **Deploy automático** futuro
- 📈 **Evolução controlada** do sistema

**Agora você pode trabalhar com tranquilidade sabendo que seu código está sempre sincronizado!** 🎯