# 🔄 INSTRUÇÕES DE SINCRONIZAÇÃO

## 📋 Conteúdo deste Pacote

### 📁 Estrutura das Pastas:
- `main_funcional.py` - Sistema principal COMPLETO
- `documentacao/` - Todos os manuais e guias
- `protecao_comercial/` - Sistema de licenças
- `ferramentas/` - Scripts de build e sync
- `codigo_fonte/` - Código modular e testes
- `assets/` - Recursos visuais

## 🚀 Como Sincronizar

### Passo 1: Backup
```bash
# Faça backup do seu projeto atual
cp -r seu_projeto/ backup_$(date +%Y%m%d)/ 
```

### Passo 2: Substituir Arquivos Principais
1. **CRÍTICO**: Substitua `main_funcional.py` 
2. Atualize `README.md`
3. Substitua `.gitignore`

### Passo 3: Adicionar Documentação
- Copie toda pasta `documentacao/` para seu projeto
- Especial atenção ao `MANUAL_TREINAMENTO_SISTEMA_LANCHONETE.md`

### Passo 4: Sistema Comercial (Opcional)
- Copie pasta `protecao_comercial/` se for vender
- Configure chaves de licença conforme necessário

### Passo 5: Dependências
```bash
pip install -r requirements.txt
```

### Passo 6: Testar
```bash
python main_funcional.py
```

## ✨ Principais Novidades

### Sistema de Caixa Avançado
- Abertura/fechamento com relatórios
- Sangria e reforço controlados
- Movimentações rastreadas

### Backup e Sincronização
- Backup completo automático
- Exportação Excel multi-abas
- Histórico de backups

### Contas em Aberto (Crediário)
- Vendas fiado com cliente
- Controle vencimentos
- Status pagamento

### Manual Completo
- 300+ linhas de treinamento
- Fluxo de trabalho diário
- Solução de problemas

### Sistema de Licenciamento
- Chaves únicas por cliente
- Validação automática
- Proteção comercial

## 🆘 Se Algo Der Errado

1. **Restaure backup**: `cp -r backup_*/ seu_projeto/`
2. **Compare arquivos**: Use diff para ver diferenças
3. **Teste individual**: Execute cada módulo separadamente
4. **Verifique deps**: `pip list` para conferir bibliotecas

## 📞 Suporte

- Documentação completa na pasta `documentacao/`
- Exemplos práticos em `protecao_comercial/`
- Scripts de build em `ferramentas/`

**Boa sincronização!** 🚀
