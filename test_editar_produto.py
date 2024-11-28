import unittest
import sqlite3
from main import salvar_edicao

# Configuração inicial do banco de dados em memória para os testes
def configurar_banco():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE Produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            qtde INTEGER,
            preco REAL
        )
    """)
    cursor.execute("INSERT INTO Produtos (nome, qtde, preco) VALUES ('Produto Teste', 10, 20.0)")
    conn.commit()
    return conn, cursor

# Classe de teste
class TestSalvarEdicao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global connection, cursor
        connection, cursor = configurar_banco()
    
    @classmethod
    def tearDownClass(cls):
        connection.close()

    def test_atualizacao_valida(self):
        """Testa uma atualização válida de produto."""
        resultado = salvar_edicao(cursor, 1, 'Produto Atualizado', 5, '30.50')
        self.assertTrue(resultado)
        cursor.execute("SELECT nome, qtde, preco FROM Produtos WHERE id=1")
        produto = cursor.fetchone()
        self.assertEqual(produto, ('Produto Atualizado', 5, 30.5))

    def test_valor_invalido_em_qtde(self):
        """Testa a falha ao passar um valor inválido em quantidade."""
        resultado = salvar_edicao(cursor, 1, 'Produto Atualizado', 'invalido', '30.50')
        self.assertFalse(resultado)

    def test_valor_invalido_em_preco(self):
        """Testa a falha ao passar um valor inválido em preço."""
        resultado = salvar_edicao(cursor, 1, 'Produto Atualizado', 5, 'invalido')
        self.assertFalse(resultado)

    def test_id_produto_nao_existente(self):
        """Testa a atualização em um ID de produto inexistente."""
        resultado = salvar_edicao(cursor, 999, 'Produto Atualizado', 5, '30.50')
        self.assertTrue(resultado)
        cursor.execute("SELECT COUNT(*) FROM Produtos WHERE id=999")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 0)

if __name__ == "__main__":
    unittest.main()
