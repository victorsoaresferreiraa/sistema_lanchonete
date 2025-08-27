"""
Sistema de versionamento e atualizações
"""

import os
import json
import requests
from datetime import datetime
from src.estoque.database import DatabaseManager

class VersionManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.versao_atual = "1.0.0"
        self.config_file = "data/config.json"
        
    def obter_versao_atual(self):
        """Obtém a versão atual do sistema"""
        versao = self.db.obter_configuracao('versao_sistema')
        return versao if versao else self.versao_atual
        
    def atualizar_versao(self, nova_versao):
        """Atualiza a versão do sistema"""
        return self.db.atualizar_configuracao('versao_sistema', nova_versao)
        
    def verificar_atualizacoes(self, url_servidor=None):
        """Verifica se há atualizações disponíveis"""
        if not url_servidor:
            # Para futuras implementações com servidor de atualizações
            return False, "Servidor de atualizações não configurado"
            
        try:
            response = requests.get(f"{url_servidor}/versao", timeout=10)
            if response.status_code == 200:
                dados = response.json()
                versao_servidor = dados.get('versao')
                
                if self._comparar_versoes(versao_servidor, self.obter_versao_atual()):
                    return True, {
                        'versao': versao_servidor,
                        'descricao': dados.get('descricao', ''),
                        'url_download': dados.get('url_download', ''),
                        'obrigatoria': dados.get('obrigatoria', False)
                    }
                else:
                    return False, "Sistema está atualizado"
                    
        except Exception as e:
            return False, f"Erro ao verificar atualizações: {str(e)}"
            
        return False, "Nenhuma atualização disponível"
        
    def _comparar_versoes(self, versao1, versao2):
        """Compara duas versões e retorna True se versao1 > versao2"""
        def versao_para_tupla(v):
            return tuple(map(int, v.split('.')))
            
        return versao_para_tupla(versao1) > versao_para_tupla(versao2)
        
    def fazer_backup(self):
        """Cria backup do banco de dados antes de atualizar"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = "backup"
        os.makedirs(backup_dir, exist_ok=True)
        
        # Backup do banco
        if os.path.exists("data/banco.db"):
            backup_path = f"{backup_dir}/banco_backup_{timestamp}.db"
            import shutil
            shutil.copy2("data/banco.db", backup_path)
            return backup_path
            
        return None
        
    def carregar_configuracoes(self):
        """Carrega configurações do arquivo JSON"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
        
    def salvar_configuracoes(self, config):
        """Salva configurações no arquivo JSON"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
            
    def migrar_banco(self, versao_origem, versao_destino):
        """Executa migrações do banco de dados"""
        migrações = {
            "1.0.0_to_1.1.0": self._migrar_1_0_0_para_1_1_0,
            "1.1.0_to_1.2.0": self._migrar_1_1_0_para_1_2_0,
        }
        
        chave_migracao = f"{versao_origem}_to_{versao_destino}"
        if chave_migracao in migrações:
            try:
                migrações[chave_migracao]()
                return True
            except Exception as e:
                print(f"Erro na migração: {e}")
                return False
        return True
        
    def _migrar_1_0_0_para_1_1_0(self):
        """Migração da versão 1.0.0 para 1.1.0"""
        # Adicionar colunas de preço se não existirem
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Verificar se coluna preco existe na tabela estoque
            cursor.execute("PRAGMA table_info(estoque)")
            colunas = [col[1] for col in cursor.fetchall()]
            
            if 'preco' not in colunas:
                cursor.execute("ALTER TABLE estoque ADD COLUMN preco REAL DEFAULT 0.0")
                cursor.execute("ALTER TABLE estoque ADD COLUMN categoria TEXT DEFAULT 'Geral'")
                cursor.execute("ALTER TABLE estoque ADD COLUMN codigo_barras TEXT DEFAULT ''")
                cursor.execute("ALTER TABLE estoque ADD COLUMN data_cadastro TEXT DEFAULT ''")
                cursor.execute("ALTER TABLE estoque ADD COLUMN data_atualizacao TEXT DEFAULT ''")
                
            # Verificar se colunas financeiras existem no histórico
            cursor.execute("PRAGMA table_info(historico_vendas)")
            colunas = [col[1] for col in cursor.fetchall()]
            
            if 'preco_unitario' not in colunas:
                cursor.execute("ALTER TABLE historico_vendas ADD COLUMN preco_unitario REAL DEFAULT 0.0")
                cursor.execute("ALTER TABLE historico_vendas ADD COLUMN valor_total REAL DEFAULT 0.0")
                cursor.execute("ALTER TABLE historico_vendas ADD COLUMN vendedor TEXT DEFAULT ''")
                cursor.execute("ALTER TABLE historico_vendas ADD COLUMN observacoes TEXT DEFAULT ''")
                
            conn.commit()
            
    def _migrar_1_1_0_para_1_2_0(self):
        """Migração da versão 1.1.0 para 1.2.0"""
        # Futuras migrações
        pass

class UpdateChecker:
    def __init__(self):
        self.version_manager = VersionManager()
        
    def verificar_ao_iniciar(self):
        """Verifica atualizações na inicialização do sistema"""
        config = self.version_manager.carregar_configuracoes()
        
        # Verificar apenas se configurado pelo usuário
        if config.get('verificar_atualizacoes_automaticamente', False):
            servidor = config.get('servidor_atualizacoes')
            if servidor:
                return self.version_manager.verificar_atualizacoes(servidor)
                
        return False, "Verificação automática desabilitada"
        
    def configurar_atualizacoes(self, servidor_url, verificar_automaticamente=True):
        """Configura servidor de atualizações"""
        config = self.version_manager.carregar_configuracoes()
        config['servidor_atualizacoes'] = servidor_url
        config['verificar_atualizacoes_automaticamente'] = verificar_automaticamente
        
        return self.version_manager.salvar_configuracoes(config)