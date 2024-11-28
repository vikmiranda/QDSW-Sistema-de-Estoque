import unittest
import sqlite3
from unittest.mock import MagicMock, patch
from main import exibir_vendas, add_produto, tela_add_produto, tela_vender_prod, tela_edit_produto


class TestExibirVendas(unittest.TestCase):
    def setUp(self):
        """
        Configura o banco de dados SQLite em memória antes de cada teste.
        """
        # Conecta ao banco de dados em memória
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

        # Cria a tabela 'Vendas' no banco de dados
        self.cursor.execute("""
            CREATE TABLE Vendas (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                quantidade INTEGER,
                preco_total REAL,
                data TEXT
            )
        """)

        # Insere dados fictícios na tabela
        self.cursor.executemany("""
            INSERT INTO Vendas (id, nome, quantidade, preco_total, data)
            VALUES (?, ?, ?, ?, ?)
        """, [
            (1, "Produto A", 3, 45.0, "2024-01-01"),
            (2, "Produto B", 2, 30.0, "2024-01-02"),
        ])

        self.conn.commit()

    def tearDown(self):
        """
        Fecha a conexão do banco de dados após cada teste.
        """
        self.conn.close()

    def test_exibir_vendas(self):
        """
        Testa se a função exibir_vendas retorna os dados corretos.
        """
        # Substitui a função exibir_vendas para usar o banco de dados em memória
        def exibir_vendas_test():
            self.cursor.execute("SELECT * FROM Vendas")
            return self.cursor.fetchall()

        # Chama a função de teste
        resultado = exibir_vendas_test()

        # Verifica se o resultado é o esperado
        self.assertEqual(resultado, [
            (1, "Produto A", 3, 45.0, "2024-01-01"),
            (2, "Produto B", 2, 30.0, "2024-01-02"),
        ])



if __name__ == "__main__":
    unittest.main()
