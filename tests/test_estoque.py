"""
Testes unitários para o módulo de estoque
"""

import unittest
import os
import tempfile
import sys

# Adicionar src ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.estoque.database import DatabaseManager
from src.estoque.controller import EstoqueController


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        """Configurar teste com banco temporário"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_banco.db")
        self.db = DatabaseManager(self.db_path)
        
    def tearDown(self):
        """Limpeza após teste"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)
        
    def test_init_database(self):
        """Testa inicialização do banco de dados"""
        self.assertTrue(os.path.exists(self.db_path))
        
        # Verificar se as tabelas foram criadas
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Verificar tabela estoque
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='estoque'")
            self.assertIsNotNone(cursor.fetchone())
            
            # Verificar tabela historico_vendas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='historico_vendas'")
            self.assertIsNotNone(cursor.fetchone())
            
    def test_inserir_produto(self):
        """Testa inserção de produto"""
        resultado = self.db.inserir_produto("Hambúrguer", 10)
        self.assertTrue(resultado)
        
        # Verificar se foi inserido
        quantidade = self.db.consultar_produto("Hambúrguer")
        self.assertEqual(quantidade, 10)
        
    def test_inserir_produto_duplicado(self):
        """Testa inserção de produto duplicado"""
        self.db.inserir_produto("Pizza", 5)
        resultado = self.db.inserir_produto("Pizza", 3)
        self.assertFalse(resultado)
        
    def test_atualizar_quantidade(self):
        """Testa atualização de quantidade"""
        self.db.inserir_produto("Refrigerante", 20)
        resultado = self.db.atualizar_quantidade("Refrigerante", 15)
        self.assertTrue(resultado)
        
        quantidade = self.db.consultar_produto("Refrigerante")
        self.assertEqual(quantidade, 15)
        
    def test_consultar_produto_inexistente(self):
        """Testa consulta de produto que não existe"""
        quantidade = self.db.consultar_produto("Produto Inexistente")
        self.assertIsNone(quantidade)
        
    def test_listar_estoque(self):
        """Testa listagem do estoque"""
        self.db.inserir_produto("Produto A", 5)
        self.db.inserir_produto("Produto B", 10)
        
        estoque = self.db.listar_estoque()
        self.assertEqual(len(estoque), 2)
        
        # Verificar se está ordenado
        produtos = [item[0] for item in estoque]
        self.assertEqual(produtos, sorted(produtos))
        
    def test_remover_produto(self):
        """Testa remoção de produto"""
        self.db.inserir_produto("Produto Temp", 1)
        resultado = self.db.remover_produto("Produto Temp")
        self.assertTrue(resultado)
        
        quantidade = self.db.consultar_produto("Produto Temp")
        self.assertIsNone(quantidade)
        
    def test_registrar_venda(self):
        """Testa registro de venda"""
        resultado = self.db.registrar_venda("Hambúrguer", 2)
        self.assertTrue(resultado)
        
        historico = self.db.listar_historico()
        self.assertEqual(len(historico), 1)
        
        venda = historico[0]
        self.assertEqual(venda[1], "Hambúrguer")  # produto
        self.assertEqual(venda[2], 2)             # quantidade
        
    def test_listar_historico(self):
        """Testa listagem do histórico"""
        self.db.registrar_venda("Produto 1", 1)
        self.db.registrar_venda("Produto 2", 2)
        
        historico = self.db.listar_historico()
        self.assertEqual(len(historico), 2)
        
        # Verificar se está ordenado por ID descendente
        ids = [venda[0] for venda in historico]
        self.assertEqual(ids, sorted(ids, reverse=True))


class TestEstoqueController(unittest.TestCase):
    def setUp(self):
        """Configurar teste com controller"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_banco.db")
        
        # Monkey patch para usar banco temporário
        self.original_init = DatabaseManager.__init__
        DatabaseManager.__init__ = lambda self, db_path=self.db_path: self.original_init(db_path)
        
        self.controller = EstoqueController()
        
    def tearDown(self):
        """Limpeza após teste"""
        # Restaurar método original
        DatabaseManager.__init__ = self.original_init
        
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)
        
    def test_adicionar_produto_valido(self):
        """Testa adição de produto válido"""
        resultado = self.controller.adicionar_produto("hambúrguer", 5)
        self.assertTrue(resultado)
        
        # Verificar se foi capitalizado
        quantidade = self.controller.consultar_produto("Hambúrguer")
        self.assertEqual(quantidade, 5)
        
    def test_adicionar_produto_nome_vazio(self):
        """Testa adição com nome vazio"""
        with self.assertRaises(ValueError):
            self.controller.adicionar_produto("", 5)
            
        with self.assertRaises(ValueError):
            self.controller.adicionar_produto("   ", 5)
            
    def test_adicionar_produto_quantidade_negativa(self):
        """Testa adição com quantidade negativa"""
        with self.assertRaises(ValueError):
            self.controller.adicionar_produto("Produto", -1)
            
    def test_atualizar_produto(self):
        """Testa atualização de produto"""
        self.controller.adicionar_produto("Pizza", 10)
        resultado = self.controller.atualizar_produto("pizza", 15)
        self.assertTrue(resultado)
        
        quantidade = self.controller.consultar_produto("Pizza")
        self.assertEqual(quantidade, 15)
        
    def test_verificar_estoque_baixo(self):
        """Testa verificação de estoque baixo"""
        self.controller.adicionar_produto("Produto A", 3)
        self.controller.adicionar_produto("Produto B", 10)
        self.controller.adicionar_produto("Produto C", 1)
        
        produtos_baixo = self.controller.verificar_estoque_baixo(5)
        self.assertEqual(len(produtos_baixo), 2)
        
        nomes_baixo = [produto[0] for produto in produtos_baixo]
        self.assertIn("Produto A", nomes_baixo)
        self.assertIn("Produto C", nomes_baixo)
        self.assertNotIn("Produto B", nomes_baixo)
        
    def test_buscar_produtos(self):
        """Testa busca de produtos"""
        self.controller.adicionar_produto("Hambúrguer Tradicional", 5)
        self.controller.adicionar_produto("Hambúrguer Especial", 3)
        self.controller.adicionar_produto("Pizza Margherita", 8)
        
        # Buscar por "hambúrguer"
        resultado = self.controller.buscar_produtos("hambúrguer")
        self.assertEqual(len(resultado), 2)
        
        # Buscar por "pizza"
        resultado = self.controller.buscar_produtos("pizza")
        self.assertEqual(len(resultado), 1)
        
        # Buscar termo que não existe
        resultado = self.controller.buscar_produtos("refrigerante")
        self.assertEqual(len(resultado), 0)


if __name__ == '__main__':
    unittest.main()
