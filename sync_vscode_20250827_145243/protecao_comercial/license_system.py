
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
            print(f"⚠️  Licença expira em {days_left} dias")
            
    except:
        print("❌ Licença corrompida!")
        sys.exit(1)

# Chamada obrigatória no início
validate_license()
