# 📚 MANUAL DE TREINAMENTO - SISTEMA DE LANCHONETE

## 🎯 INTRODUÇÃO

Este manual foi desenvolvido para capacitar você no uso completo do Sistema de Gestão de Lanchonete. O sistema foi projetado para ser intuitivo e eficiente, permitindo o controle total do seu negócio em uma única aplicação.

### O que você aprenderá:
- Operação básica e avançada de todas as funcionalidades
- Fluxo de trabalho diário recomendado
- Dicas e boas práticas
- Solução de problemas comuns
- Aproveitamento máximo do sistema

---

## 🚀 INICIANDO O SISTEMA

### Primeira execução:
1. Execute o arquivo `main_funcional.py` ou use o atalho `.bat`
2. O sistema criará automaticamente o banco de dados
3. A tela principal será exibida com 8 opções principais

### Interface Principal:
A tela inicial apresenta botões organizados para cada função:
- **📦 Gerenciar Estoque**: Controle completo do inventário
- **➕ Cadastrar Produto**: Adição rápida de novos itens
- **💰 Registrar Venda**: Vendas à vista e fiado
- **📋 Contas em Aberto**: Gestão de crediário
- **💳 Controle de Caixa**: Movimentações financeiras
- **📊 Dashboard Financeiro**: Análises e gráficos
- **💾 Backup/Sincronização**: Proteção dos dados
- **📄 Relatórios**: Exportações e consultas

---

## 📦 GESTÃO DE ESTOQUE

### Cadastrando Produtos (Primeiro Passo Essencial)

#### Método 1: Cadastro Rápido
1. Clique em **"➕ Cadastrar Produto"**
2. Preencha os campos obrigatórios:
   - **Nome do Produto**: Use nomes descritivos (ex: "Coca-Cola 350ml")
   - **Categoria**: Organize por tipo (Bebidas, Lanches, Doces, etc.)
   - **Quantidade Inicial**: Estoque atual
   - **Preço**: Valor de venda (use . ou , para decimais)
3. Clique **"💾 Salvar Produto"**
4. Escolha se deseja cadastrar outro produto

#### Método 2: Gerenciamento Completo
1. Clique em **"📦 Gerenciar Estoque"**
2. Use o formulário superior para adicionar produtos
3. A lista mostra todos os produtos em tempo real
4. Funções disponíveis:
   - **➕ Adicionar**: Novo produto
   - **✏️ Atualizar**: Modificar produto selecionado
   - **🗑️ Remover**: Excluir produto
   - **🔄 Limpar**: Limpar formulário

### Dicas de Cadastro:
- **Nomes Descritivos**: "Hambúrguer X-Bacon" ao invés de só "Hambúrguer"
- **Categorias Consistentes**: Use sempre as mesmas categorias
- **Preços Precisos**: Defina preços corretos desde o início
- **Estoque Zero**: Para produtos feitos na hora, use quantidade 0

### Produtos de Exemplo:
O sistema inclui uma função **"📦 Produtos Exemplo"** que adiciona:
- Bebidas (Coca-Cola, Água, Suco)
- Lanches (X-Burger, Misto Quente, Pastel)
- Doces (Brigadeiro, Pudim)

---

## 💰 SISTEMA DE VENDAS

### Tipos de Venda

#### Venda à Vista (Pagamento Imediato)
1. Clique em **"💰 Registrar Venda"**
2. Selecione o produto no menu suspenso
3. Digite a quantidade
4. O preço é preenchido automaticamente
5. Verifique o total calculado
6. Clique **"💾 Venda à Vista"**
7. Confirme a venda

#### Venda Fiado (Crediário)
1. Na tela de vendas, clique **"📋 Venda Fiado"**
2. Uma nova janela abrirá para dados do cliente:
   - **Nome do Cliente**: Obrigatório
   - **Telefone**: Opcional mas recomendado
   - **Vencimento**: Padrão 30 dias (modificável)
   - **Observações**: Informações extras
3. Clique **"📋 Registrar Fiado"**
4. A conta ficará em aberto para pagamento posterior

### Fluxo Recomendado de Vendas:
1. **Sempre verificar estoque** antes de confirmar
2. **Confirmar dados** com o cliente
3. **Registrar imediatamente** após a venda
4. **Verificar total** antes de finalizar

---

## 📋 GESTÃO DE CONTAS EM ABERTO

### Acessando o Sistema:
1. Clique em **"📋 Contas em Aberto"**
2. A tela mostra todas as contas por cliente

### Filtros Disponíveis:
- **Apenas Pendentes**: Contas não pagas
- **Apenas Pagas**: Histórico de pagamentos
- **Todas**: Visão completa

### Informações Exibidas:
- Cliente e telefone
- Produto vendido
- Quantidade e valor total
- Data da venda e vencimento
- Status (Pendente/Pago/Vencido)

### Operações:
- **💰 Marcar como Pago**: Registra pagamento
- **✏️ Editar**: Modificar dados (em desenvolvimento)
- **🗑️ Excluir**: Remover conta
- **🔄 Atualizar**: Recarregar dados

### Controle de Vencimentos:
- Contas vencidas aparecem com **🔴 VENCIDO**
- Estatísticas mostram total pendente e pago
- Use filtros para acompanhar cobranças

---

## 💳 CONTROLE DE CAIXA AVANÇADO

### Conceito Fundamental:
O sistema de caixa controla todo o dinheiro que entra e sai durante o dia de trabalho.

### Abrindo o Caixa (Início do Dia):
1. Clique em **"💳 Controle de Caixa"**
2. Se o caixa estiver fechado, clique **"🔓 Abrir Caixa"**
3. Preencha:
   - **Valor Inicial**: Dinheiro no caixa (troco)
   - **Funcionário**: Nome do responsável
   - **Observações**: Notas importantes
4. Clique **"🔓 Abrir"**

### Operações Durante o Dia:

#### Sangria (Retirar Dinheiro):
1. Com caixa aberto, clique **"💰 Sangria"**
2. Digite o valor retirado
3. Adicione descrição (ex: "Pagamento fornecedor")
4. Informe funcionário responsável
5. Confirme a operação

#### Reforço (Adicionar Dinheiro):
1. Clique **"➕ Reforço"**
2. Digite o valor adicionado
3. Descrição (ex: "Troco adicional")
4. Confirme a operação

### Fechando o Caixa (Final do Dia):
1. Clique **"🔒 Fechar Caixa"**
2. O sistema mostra o resumo do dia:
   - Valor inicial
   - Total de vendas
   - Sangrias realizadas
   - Reforços feitos
   - **Valor teórico** (quanto deveria ter)
3. Conte o dinheiro real no caixa
4. Digite o **"Valor Real em Caixa"**
5. O sistema calcula automaticamente a diferença
6. Adicione observações sobre diferenças
7. Confirme o fechamento

### Relatórios de Caixa:
- **📊 Relatório**: Mostra situação atual em tempo real
- **Movimentações**: Lista todas as operações do dia
- **Resumo**: Estatísticas de vendas e movimentações

---

## 💾 BACKUP E PROTEÇÃO DOS DADOS

### Importância do Backup:
- **Proteção contra perda**: Hardware, software ou erro humano
- **Histórico preservado**: Todas as vendas e estoque
- **Tranquilidade**: Trabalhe sem medo de perder dados

### Tipos de Backup:

#### Backup Completo:
1. Clique em **"💾 Backup/Sincronização"**
2. Clique **"💾 Backup Completo"**
3. Sistema cria cópia completa do banco de dados
4. Arquivo salvo na pasta de backups

#### Backup de Dados:
1. Clique **"📊 Backup Dados"**
2. Salva apenas informações essenciais (estoque, vendas, contas)
3. Arquivo menor, mais rápido

#### Exportar para Excel:
1. Clique **"📤 Exportar Excel"**
2. Gera arquivo .xlsx com múltiplas abas:
   - Estoque
   - Vendas
   - Contas em Aberto
3. Ideal para análises externas

### Configurações de Backup:
- **Pasta de Backup**: Escolha onde salvar (recomendado: pasta na nuvem)
- **Frequência**: Execute backup diário (manual)
- **Verificação**: Use **"📋 Verificar Integridade"** semanalmente

### Histórico de Backups:
- Lista todos os backups realizados
- Mostra data, tamanho e tipo
- Permite excluir backups antigos

---

## 📊 DASHBOARD FINANCEIRO

### Métricas Principais:
- **Vendas do Dia**: Total de receita
- **Produtos Vendidos**: Quantidade de itens
- **Ticket Médio**: Valor médio por venda
- **Contas em Aberto**: Valor total em crediário

### Gráficos Disponíveis:
- **Vendas por Período**: Evolução temporal
- **Produtos Mais Vendidos**: Ranking de itens
- **Vendas por Categoria**: Distribuição por tipo
- **Receita Acumulada**: Crescimento mensal

### Filtros e Períodos:
- Visualize por dia, semana, mês
- Compare períodos diferentes
- Análise de tendências

---

## 🏆 FLUXO DE TRABALHO DIÁRIO RECOMENDADO

### 🌅 ABERTURA (Início do Dia):
1. **Iniciar o sistema**
2. **Abrir caixa** com valor inicial
3. **Verificar estoque** de produtos principais
4. **Conferir contas em aberto** (cobranças do dia)

### 🏃‍♂️ OPERAÇÃO (Durante o Dia):
1. **Registrar vendas** imediatamente após cada atendimento
2. **Verificar estoque** antes de confirmar vendas
3. **Anotar observações** em vendas especiais
4. **Fazer sangrias** quando necessário
5. **Acompanhar contas em aberto** (pagamentos recebidos)

### 🌙 FECHAMENTO (Final do Dia):
1. **Conferir vendas** do dia no dashboard
2. **Marcar contas pagas** que foram quitadas
3. **Fazer backup** dos dados
4. **Fechar caixa** conferindo valores
5. **Analisar relatórios** para decisões futuras

---

## 💡 DICAS E BOAS PRÁTICAS

### Organização:
- **Use categorias consistentes** para produtos
- **Nomes padronizados** facilitam busca
- **Atualize preços** regularmente
- **Organize contas por vencimento**

### Segurança:
- **Backup diário** obrigatório
- **Pasta de backup na nuvem** (Google Drive, Dropbox)
- **Não modificar arquivos** do sistema manualmente
- **Treinar funcionários** nas operações básicas

### Produtividade:
- **Cadastre produtos antes** de abrir para vendas
- **Use produtos exemplo** para testar o sistema
- **Atalhos de teclado**: Enter para confirmar operações
- **Monitore dashboard** para insights de negócio

### Controle Financeiro:
- **Sangria apenas quando necessário**
- **Justifique todas as movimentações**
- **Confira caixa diariamente**
- **Acompanhe contas em aberto** semanalmente

---

## 🔧 SOLUÇÃO DE PROBLEMAS COMUNS

### Problema: "Produto não encontrado"
**Solução**: Cadastre o produto antes de registrar a venda

### Problema: "Estoque insuficiente"
**Solução**: 
- Atualize quantidade no estoque OU
- Continue mesmo assim (para produtos feitos na hora)

### Problema: "Erro ao conectar banco"
**Solução**: 
- Verifique se arquivo `banco.db` existe na pasta `data/`
- Reinicie o sistema

### Problema: "Caixa não abre"
**Solução**: 
- Verifique se há caixa já aberto
- Feche caixa anterior se necessário

### Problema: "Backup falhou"
**Solução**: 
- Verifique permissões da pasta
- Escolha pasta diferente
- Libere espaço em disco

---

## 📈 ANÁLISES E RELATÓRIOS

### Usando o Dashboard:
1. **Acesse regularmente** (diário/semanal)
2. **Compare períodos** para identificar tendências
3. **Identifique produtos campeões** de venda
4. **Monitore ticket médio** para estratégias de preço

### Exportações Excel:
- **Use para análises externas** (contador, sócio)
- **Compartilhe com fornecedores** (volume de vendas)
- **Archive mensalmente** para histórico

### Relatórios de Caixa:
- **Confira diariamente** antes do fechamento
- **Investigue diferenças** sempre
- **Mantenha histórico** para auditoria

---

## 🎓 TREINAMENTO PRÁTICO

### Para Novos Funcionários:

#### Semana 1: Básico
- Navegação na interface
- Cadastro de produtos
- Vendas à vista simples
- Consulta de estoque

#### Semana 2: Intermediário
- Vendas fiado
- Gestão de contas em aberto
- Operações básicas de caixa
- Backup de dados

#### Semana 3: Avançado
- Controle completo de caixa
- Análise de relatórios
- Resolução de problemas
- Otimização do fluxo

### Exercícios Práticos:
1. **Cadastre 10 produtos** diferentes
2. **Faça 5 vendas à vista** e 3 fiado
3. **Abra e feche caixa** com movimentações
4. **Gere backup** completo
5. **Analise dashboard** do período

---

## 🆘 SUPORTE E MANUTENÇÃO

### Manutenção Preventiva:
- **Backup semanal** obrigatório
- **Verificação de integridade** mensal
- **Limpeza de backups antigos** trimestral
- **Atualização de preços** conforme necessário

### Quando Buscar Ajuda:
- Erros persistentes no sistema
- Perda de dados
- Necessidade de funcionalidades novas
- Treinamento de equipe

### Contatos de Suporte:
- Documentação técnica em `DOCUMENTACAO_COMPLETA.md`
- Instruções de instalação em `INSTRUCOES_INSTALACAO.md`
- Guia de sincronização em `INSTRUCOES_SINCRONIZACAO.md`

---

## 🏁 CONSIDERAÇÕES FINAIS

Este sistema foi desenvolvido para crescer com seu negócio. Use todas as funcionalidades disponíveis para ter controle total da sua lanchonete.

**Lembre-se:**
- **Consistência** no uso diário
- **Backup regular** dos dados
- **Análise constante** dos relatórios
- **Treinamento contínuo** da equipe

**O sucesso do sistema depende do seu uso correto e constante.**

---

### 📞 RESUMO DE EMERGÊNCIA

**Não consegue abrir o sistema?**
1. Verifique se Python está instalado
2. Execute `python main_funcional.py`
3. Verifique pasta `data/` existe

**Perdeu dados?**
1. Procure arquivo de backup mais recente
2. Substitua `banco.db` na pasta `data/`
3. Reinicie o sistema

**Caixa não fecha?**
1. Verifique se há vendas não registradas
2. Confira movimentações pendentes
3. Digite valor real em caixa

**Sistema está lento?**
1. Feche outros programas
2. Faça backup e restart
3. Verifique espaço em disco

---

*Manual criado para maximizar o aproveitamento do Sistema de Gestão de Lanchonete*  
*Versão 1.0 - Agosto 2025*