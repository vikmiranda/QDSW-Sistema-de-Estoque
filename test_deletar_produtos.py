import unittest
import sqlite3
from main import deletar_produtos

def configurar_banco():
    """
    Configura um banco de dados SQLite em memória para testes.

    Returns:
        tuple: Conexão e cursor do banco de dados.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE Produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            qtde INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    """)
    # Inserir dados iniciais para os testes
    produtos_iniciais = [
        ('Produto Teste 1', 10, 20.0),
        ('Produto Teste 2', 5, 15.5),
        ('Produto Teste 3', 8, 30.0)
    ]
    cursor.executemany("INSERT INTO Produtos (nome, qtde, preco) VALUES (?, ?, ?)", produtos_iniciais)
    conn.commit()
    return conn, cursor

class TestDeletarProdutos(unittest.TestCase):
    def setUp(self):
        self.connection, self.cursor = configurar_banco()

    def tearDown(self):
        self.connection.close()

    def test_deletar_produtos_valido(self):
        """Testa a deleção válida de um produto."""
        itens_para_deletar = [(1, 'Produto Teste 1')]
        resultado = deletar_produtos(self.cursor, itens_para_deletar)
        self.assertTrue(resultado)
        self.cursor.execute("SELECT * FROM Produtos WHERE id=1")
        self.assertIsNone(self.cursor.fetchone())  # Verifica que o produto foi deletado

    def test_deletar_produtos_invalido(self):
        """Testa a deleção com valores inválidos."""
        itens_para_deletar = [('invalido', 'Produto Inexistente')]
        resultado = deletar_produtos(self.cursor, itens_para_deletar)
        self.assertFalse(resultado)  # A função deve retornar False

    def test_deletar_produto_nao_existente(self):
        """Testa a tentativa de deletar um produto que não existe no banco."""
        itens_para_deletar = [(999, 'Produto Inexistente')]
        resultado = deletar_produtos(self.cursor, itens_para_deletar)
        self.assertTrue(resultado)  # A deleção não gera erro, mas nada é deletado
        self.cursor.execute("SELECT COUNT(*) FROM Produtos")
        self.assertEqual(self.cursor.fetchone()[0], 3)  # Nenhum produto foi removido

if __name__ == "__main__":
    unittest.main()
