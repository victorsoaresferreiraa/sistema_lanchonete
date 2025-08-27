"""
Testes unitários para o módulo de pedidos
"""

import unittest
import os
import tempfile
import sys
from datetime import datetime

# Adicionar src ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.estoque.database import DatabaseManager
from src.pedidos.historico import HistoricoController
from src.pedidos.export import ExportController


class TestHistoricoController(unittest.TestCase):
    def setUp(self):
        """Configurar teste com controller"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_banco.db")
        
        # Monkey patch para usar banco temporário
        self.original_init = DatabaseManager.__init__
        DatabaseManager.__init__ = lambda self, db_path=self.db_path: self.original_init(db_path)
        
        self.controller = HistoricoController()
        
    def tearDown(self):
        """Limpeza após teste"""
        # Restaurar método original
        DatabaseManager.__init__ = self.original_init
        
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)
        
    def test_registrar_venda_valida(self):
        """Testa registro de venda válida"""
        resultado = self.controller.registrar_venda("hambúrguer", 2)
        self.assertTrue(resultado)
        
        historico = self.controller.listar_historico()
        self.assertEqual(len(historico), 1)
        
        venda = historico[0]
        self.assertEqual(venda[1], "Hambúrguer")  # Nome capitalizado
        self.assertEqual(venda[2], 2)             # Quantidade
        
    def test_registrar_venda_nome_vazio(self):
        """Testa registro com nome vazio"""
        with self.assertRaises(ValueError):
            self.controller.registrar_venda("", 1)
            
        with self.assertRaises(ValueError):
            self.controller.registrar_venda("   ", 1)
            
    def test_registrar_venda_quantidade_invalida(self):
        """Testa registro com quantidade inválida"""
        with self.assertRaises(ValueError):
            self.controller.registrar_venda("Produto", 0)
            
        with self.assertRaises(ValueError):
            self.controller.registrar_venda("Produto", -1)
            
    def test_buscar_vendas_produto(self):
        """Testa busca de vendas por produto"""
        self.controller.registrar_venda("Pizza", 1)
        self.controller.registrar_venda("Hambúrguer", 2)
        self.controller.registrar_venda("Pizza", 3)
        
        vendas_pizza = self.controller.buscar_vendas_produto("pizza")
        self.assertEqual(len(vendas_pizza), 2)
        
        # Verificar se todas as vendas são de pizza
        for venda in vendas_pizza:
            self.assertIn("Pizza", venda[1])
            
    def test_obter_estatisticas(self):
        """Testa obtenção de estatísticas"""
        self.controller.registrar_venda("Pizza", 2)
        self.controller.registrar_venda("Hambúrguer", 1)
        self.controller.registrar_venda("Pizza", 3)
        
        estatisticas = self.controller.obter_estatisticas()
        self.assertEqual(len(estatisticas), 2)
        
        # Pizza deve ser o primeiro (mais vendido)
        produto_mais_vendido = estatisticas[0]
        self.assertEqual(produto_mais_vendido[0], "Pizza")
        self.assertEqual(produto_mais_vendido[1], 5)  # Total vendido
        self.assertEqual(produto_mais_vendido[2], 2)  # Número de vendas
        
    def test_produto_mais_vendido(self):
        """Testa identificação do produto mais vendido"""
        self.controller.registrar_venda("Refrigerante", 10)
        self.controller.registrar_venda("Pizza", 3)
        self.controller.registrar_venda("Refrigerante", 5)
        
        mais_vendido = self.controller.produto_mais_vendido()
        self.assertIsNotNone(mais_vendido)
        self.assertEqual(mais_vendido['produto'], "Refrigerante")
        self.assertEqual(mais_vendido['total_vendido'], 15)
        self.assertEqual(mais_vendido['num_vendas'], 2)
        
    def test_produto_mais_vendido_sem_vendas(self):
        """Testa produto mais vendido sem vendas"""
        mais_vendido = self.controller.produto_mais_vendido()
        self.assertIsNone(mais_vendido)
        
    def test_relatorio_vendas(self):
        """Testa geração de relatório de vendas"""
        self.controller.registrar_venda("Produto A", 2)
        self.controller.registrar_venda("Produto B", 3)
        
        relatorio = self.controller.relatorio_vendas()
        
        self.assertEqual(relatorio['total_vendas'], 2)
        self.assertEqual(relatorio['total_itens'], 5)
        self.assertIsNotNone(relatorio['produto_mais_vendido'])
        self.assertIsInstance(relatorio['estatisticas_produtos'], list)


class TestExportController(unittest.TestCase):
    def setUp(self):
        """Configurar teste com controller"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_banco.db")
        
        # Monkey patch para usar banco temporário
        self.original_init = DatabaseManager.__init__
        DatabaseManager.__init__ = lambda self, db_path=self.db_path: self.original_init(db_path)
        
        self.controller = ExportController()
        
        # Adicionar alguns dados de teste
        self.controller.db.inserir_produto("Pizza", 10)
        self.controller.db.inserir_produto("Hambúrguer", 5)
        self.controller.db.registrar_venda("Pizza", 2)
        
    def tearDown(self):
        """Limpeza após teste"""
        # Restaurar método original
        DatabaseManager.__init__ = self.original_init
        
        # Limpar arquivos temporários
        import glob
        for arquivo in glob.glob(os.path.join(self.temp_dir, "*")):
            try:
                os.remove(arquivo)
            except OSError:
                pass
                
        try:
            os.rmdir(self.temp_dir)
        except OSError:
            pass
            
    def test_exportar_estoque(self):
        """Testa exportação do estoque"""
        arquivo_teste = os.path.join(self.temp_dir, "teste_estoque.xlsx")
        resultado = self.controller.exportar_estoque(arquivo_teste)
        
        self.assertEqual(resultado, arquivo_teste)
        self.assertTrue(os.path.exists(arquivo_teste))
        
    def test_exportar_historico(self):
        """Testa exportação do histórico"""
        arquivo_teste = os.path.join(self.temp_dir, "teste_historico.xlsx")
        resultado = self.controller.exportar_historico(arquivo_teste)
        
        self.assertEqual(resultado, arquivo_teste)
        self.assertTrue(os.path.exists(arquivo_teste))
        
    def test_exportar_estatisticas(self):
        """Testa exportação de estatísticas"""
        arquivo_teste = os.path.join(self.temp_dir, "teste_stats.xlsx")
        resultado = self.controller.exportar_estatisticas(arquivo_teste)
        
        self.assertEqual(resultado, arquivo_teste)
        self.assertTrue(os.path.exists(arquivo_teste))
        
    def test_exportar_estoque_vazio(self):
        """Testa exportação com estoque vazio"""
        # Limpar estoque
        self.controller.db.execute_update("DELETE FROM estoque")
        
        resultado = self.controller.exportar_estoque()
        self.assertIsNone(resultado)
        
    def test_exportar_relatorio_completo(self):
        """Testa exportação de relatório completo"""
        arquivo_teste = os.path.join(self.temp_dir, "teste_completo.xlsx")
        resultado = self.controller.exportar_relatorio_completo(arquivo_teste)
        
        self.assertEqual(resultado, arquivo_teste)
        self.assertTrue(os.path.exists(arquivo_teste))


if __name__ == '__main__':
    # Configurar para ignorar warnings do pandas/openpyxl durante os testes
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    
    unittest.main()
