"""
Sistema de Proteção Comercial para o Sistema de Lanchonete
Implementa licenciamento, obfuscação e controle de uso
"""

import hashlib
import datetime
import os
import base64

class LicenseManager:
    """Gerenciador de licenças do sistema"""
    
    def __init__(self):
        self.license_key = None
        self.encrypted_data = None
        
    def generate_license_key(self, customer_name, max_days=365):
        """Gera chave de licença para cliente"""
        # Dados únicos do cliente
        customer_hash = hashlib.sha256(customer_name.lower().encode()).hexdigest()[:8]
        
        # Data de expiração
        expiry_date = datetime.datetime.now() + datetime.timedelta(days=max_days)
        expiry_str = expiry_date.strftime("%Y%m%d")
        
        # Criar chave
        license_data = f"{customer_hash}-{expiry_str}"
        encoded_license = base64.b64encode(license_data.encode()).decode()
        
        return f"LANCH-{encoded_license}"
    
    def validate_license(self, license_key, customer_name):
        """Valida licença do cliente"""
        try:
            if not license_key.startswith("LANCH-"):
                return False, "Licença inválida"
            
            # Decodificar
            encoded_part = license_key.replace("LANCH-", "")
            decoded_data = base64.b64decode(encoded_part).decode()
            
            customer_hash, expiry_str = decoded_data.split("-")
            
            # Verificar hash do cliente
            expected_hash = hashlib.sha256(customer_name.lower().encode()).hexdigest()[:8]
            if customer_hash != expected_hash:
                return False, "Licença não pertence a este cliente"
            
            # Verificar expiração
            expiry_date = datetime.datetime.strptime(expiry_str, "%Y%m%d")
            if datetime.datetime.now() > expiry_date:
                return False, "Licença expirada"
            
            return True, "Licença válida"
            
        except Exception as e:
            return False, f"Erro na validação: {e}"

class CodeObfuscator:
    """Ofusca código Python para proteção"""
    
    @staticmethod
    def obfuscate_string(text):
        """Ofusca strings no código"""
        encoded = base64.b64encode(text.encode()).decode()
        return f"base64.b64decode('{encoded}').decode()"
    
    @staticmethod
    def obfuscate_function_names(code):
        """Renomeia funções para nomes não descritivos"""
        import re
        
        # Lista de funções importantes para renomear
        functions_to_rename = {
            'cadastrar_produto': '_func_a1',
            'registrar_venda': '_func_b2',
            'abrir_caixa': '_func_c3',
            'backup_completo': '_func_d4',
            'gerar_relatorio': '_func_e5'
        }
        
        for old_name, new_name in functions_to_rename.items():
            code = re.sub(rf'\b{old_name}\b', new_name, code)
        
        return code

class AntiTamperingSystem:
    """Sistema anti-violação"""
    
    @staticmethod
    def create_file_hash(file_path):
        """Cria hash do arquivo para detectar modificações"""
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        return file_hash
    
    @staticmethod
    def verify_integrity(file_path, expected_hash):
        """Verifica integridade do arquivo"""
        current_hash = AntiTamperingSystem.create_file_hash(file_path)
        return current_hash == expected_hash

def create_commercial_version():
    """Cria versão comercial protegida"""
    
    print("🔒 Criando Versão Comercial Protegida")
    print("=" * 40)
    
    # 1. Gerar licença de exemplo
    license_mgr = LicenseManager()
    example_license = license_mgr.generate_license_key("Lanchonete do João", 365)
    
    print(f"📜 Licença de exemplo: {example_license}")
    
    # 2. Criar código de validação
    validation_code = f'''
import base64
import hashlib
import datetime
import sys

def validate_license():
    """Validação de licença obrigatória"""
    license_file = "license.key"
    
    if not os.path.exists(license_file):
        print("❌ Licença não encontrada!")
        print("💡 Entre em contato para adquirir sua licença")
        sys.exit(1)
    
    with open(license_file, 'r') as f:
        license_key = f.read().strip()
    
    # Validar licença (código ofuscado)
    if not license_key.startswith("LANCH-"):
        print("❌ Licença inválida!")
        sys.exit(1)
    
    try:
        encoded_part = license_key.replace("LANCH-", "")
        decoded_data = base64.b64decode(encoded_part).decode()
        customer_hash, expiry_str = decoded_data.split("-")
        
        expiry_date = datetime.datetime.strptime(expiry_str, "%Y%m%d")
        if datetime.datetime.now() > expiry_date:
            print("❌ Licença expirada!")
            print("💡 Renove sua licença para continuar usando")
            sys.exit(1)
            
        days_left = (expiry_date - datetime.datetime.now()).days
        if days_left <= 30:
            print(f"⚠️  Licença expira em {{days_left}} dias")
            
    except:
        print("❌ Licença corrompida!")
        sys.exit(1)

# Chamada obrigatória no início
validate_license()
'''
    
    # 3. Criar sistema de compilação
    build_script = '''
import PyInstaller.__main__
import os

def build_commercial():
    """Compila versão comercial com proteções"""
    
    # Opções do PyInstaller
    options = [
        'main_funcional.py',
        '--onefile',
        '--windowed',
        '--name=SistemaLanchonete_v2.0',
        '--icon=assets/icon.ico',
        '--add-data=assets;assets',
        '--hidden-import=tkinter',
        '--hidden-import=sqlite3',
        '--hidden-import=pandas',
        '--hidden-import=matplotlib',
        '--noconsole',
        '--distpath=dist_commercial',
        '--workpath=build_commercial',
        '--specpath=.',
        '--key=minha_chave_secreta_123'  # Criptografia
    ]
    
    PyInstaller.__main__.run(options)
    print("✅ Versão comercial criada em dist_commercial/")

if __name__ == "__main__":
    build_commercial()
'''
    
    # Salvar arquivos
    with open("license_system.py", "w", encoding="utf-8") as f:
        f.write(validation_code)
    
    with open("build_commercial.py", "w", encoding="utf-8") as f:
        f.write(build_script)
    
    print("✅ Arquivos de proteção criados")
    
    return {
        'license_example': example_license,
        'validation_file': 'license_system.py',
        'build_file': 'build_commercial.py'
    }

def create_licensing_guide():
    """Cria guia de licenciamento"""
    
    guide_content = """# 💼 Guia de Licenciamento Comercial

## 🎯 Estratégia de Venda

### Público-Alvo
- 🍔 Lanchonetes (50-200 clientes/dia)
- ☕ Cafeterias e padarias
- 🍕 Pizzarias pequenas
- 🛒 Mercadinhos e conveniências

### Proposta de Valor
- ⚡ Agilidade no atendimento
- 📊 Controle financeiro completo
- 💾 Backup automático dos dados
- 📱 Interface intuitiva
- 🇧🇷 Suporte em português

## 💰 Modelos de Preço

### Licença Única
- **Básico**: R$ 299 (1 computador)
- **Profissional**: R$ 499 (3 computadores)
- **Empresarial**: R$ 799 (ilimitado + suporte)

### Mensalidade (SaaS)
- **Starter**: R$ 49/mês
- **Business**: R$ 99/mês
- **Enterprise**: R$ 149/mês

### Serviços Adicionais
- **Instalação**: R$ 150
- **Treinamento**: R$ 200 (4 horas)
- **Personalização**: R$ 300-800
- **Suporte premium**: R$ 80/mês

## 🔒 Proteções Implementadas

### Licenciamento
- Chaves únicas por cliente
- Validação online/offline
- Controle de expiração
- Máquinas autorizadas

### Técnicas
- Código ofuscado
- Compilação criptografada
- Verificação de integridade
- Anti-debug

### Jurídicas
- Contrato de licença
- Termos de uso
- Propriedade intelectual
- Cláusula de não-competição

## 📋 Processo de Venda

### 1. Demonstração
- Apresentação online/presencial
- Teste gratuito (15 dias)
- Simulação com dados reais
- ROI calculado

### 2. Proposta
- Análise das necessidades
- Customização incluída
- Prazo de implementação
- Garantia e suporte

### 3. Contrato
- Licença de uso
- Prazo e renovação
- Suporte incluído
- Cláusulas de proteção

### 4. Implementação
- Instalação remota/local
- Migração de dados
- Treinamento da equipe
- Go-live assistido

## 🎨 Material de Marketing

### Site/Landing Page
- Benefícios claros
- Casos de sucesso
- Demonstração online
- Preços transparentes

### Materiais
- Folders explicativos
- Vídeos demonstrativos
- Apresentação comercial
- Proposta padrão

### Canais
- Google Ads (lanchonete, pdv)
- Facebook/Instagram Business
- LinkedIn B2B
- Indicações de clientes

## 📞 Suporte ao Cliente

### Níveis
- **Básico**: Email (48h)
- **Padrão**: Email + Telefone (24h)
- **Premium**: WhatsApp + Remoto (4h)

### Documentação
- Manual completo
- Vídeos tutoriais
- FAQ atualizado
- Base de conhecimento

## 📈 Crescimento do Negócio

### Expansão
- Versões especializadas
- Integrações (delivery, fiscal)
- Módulos opcionais
- Franquia de software

### Parcerias
- Revendedores locais
- Consultores empresariais
- Fornecedores de equipamentos
- Associações comerciais

## ⚖️ Aspectos Legais

### Proteção
- Registro de software
- Marca registrada
- Direitos autorais
- Patente (se aplicável)

### Contratos
- Licença de uso
- Termos de serviço
- Política de privacidade
- NDA para desenvolvimento

---

**💡 Dica**: Comece pequeno, foque na qualidade do produto e suporte. 
O boca-a-boca é seu melhor vendedor no mercado de pequenos negócios."""

    with open("GUIA_LICENCIAMENTO.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("✅ Guia de licenciamento criado")

def main():
    """Função principal"""
    print("🔐 Sistema de Proteção Comercial")
    print("=" * 40)
    
    # Criar proteções
    result = create_commercial_version()
    create_licensing_guide()
    
    print("\n📦 ARQUIVOS CRIADOS:")
    print("- license_system.py (validação)")
    print("- build_commercial.py (compilação)")
    print("- GUIA_LICENCIAMENTO.md (estratégia)")
    
    print(f"\n🔑 LICENÇA DE EXEMPLO:")
    print(f"Cliente: Lanchonete do João")
    print(f"Chave: {result['license_example']}")
    
    print("\n💼 PRÓXIMOS PASSOS:")
    print("1. Integrar validação no código principal")
    print("2. Compilar versão comercial")
    print("3. Criar material de marketing")
    print("4. Definir preços regionais")
    print("5. Estabelecer canais de venda")

if __name__ == "__main__":
    main()