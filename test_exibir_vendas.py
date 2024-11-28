import unittest
import sqlite3
from unittest.mock import MagicMock, patch
from main import buscar_vendas, add_produto, tela_add_produto, tela_vender_prod, tela_edit_produto


class TestBuscarVendas(unittest.TestCase):

    def setUp(self):
        """
        Setup inicial para configurar o ambiente de testes.
        Criação de um cursor mockado.
        """
        self.connection = sqlite3.connect(":memory:")  # Usando banco em memória para teste
        self.cursor = self.connection.cursor()

        # Criação de uma tabela fictícia 'Vendas' para o teste
        self.cursor.execute("""
            CREATE TABLE Vendas (
                id INTEGER PRIMARY KEY,
                produto TEXT,
                quantidade INTEGER,
                preco REAL
            )
        """)
        self.connection.commit()

    def test_buscar_vendas_sucesso(self):
        """
        Testa a função buscar_vendas para garantir que os dados são retornados corretamente.
        """
        # Inserindo dados na tabela Vendas
        self.cursor.execute("INSERT INTO Vendas (produto, quantidade, preco) VALUES ('Produto A', 10, 100.0)")
        self.cursor.execute("INSERT INTO Vendas (produto, quantidade, preco) VALUES ('Produto B', 5, 50.0)")
        self.connection.commit()

        # Chama a função buscar_vendas
        vendas = buscar_vendas(self.cursor)

        # Verifica se as vendas retornadas são as esperadas
        self.assertGreater(len(vendas), 0)  # Verifica se a lista não está vazia
        self.assertEqual(len(vendas), 2)  # Deve retornar 2 vendas inseridas
        self.assertEqual(vendas[0], (1, 'Produto A', 10, 100.0))  # Verifica o primeiro item
        self.assertEqual(vendas[1], (2, 'Produto B', 5, 50.0))  # Verifica o segundo item

    def test_buscar_vendas_sem_dados(self):
        """
        Testa a função buscar_vendas quando não houver dados na tabela.
        """
        vendas = buscar_vendas(self.cursor)

        self.assertEqual(len(vendas), 0)

    @patch('sqlite3.connect') 
    def test_buscar_vendas_com_erro(self, mock_connect):
        """
        Testa a função buscar_vendas se ocorrer um erro de banco de dados.
        """
        mock_cursor = MagicMock()
        
        mock_cursor.execute.side_effect = sqlite3.DatabaseError("Erro no banco de dados")
        
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        vendas = buscar_vendas(mock_cursor)

        self.assertIsNone(vendas)

    def tearDown(self):
        """
        Limpeza após os testes, fechando a conexão do banco de dados.
        """
        self.connection.close()


if __name__ == "__main__":
    unittest.main()
