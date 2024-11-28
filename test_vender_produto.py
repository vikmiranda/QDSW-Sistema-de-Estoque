import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from tkinter import messagebox as mb
import datetime

from main import vender_produto, salvar_venda, buscar_produtos  # Importar suas funções

class TestVendas(unittest.TestCase):

    @patch('main.cursor')
    @patch('main.mb.showerror')
    @patch('main.mb.showinfo')
    @patch('main.mb.askyesno')  # Mockando a confirmação de "askyesno"
    @patch('main.tkinter.Toplevel')  # Mockando a criação de novas janelas
    @patch('main.tkinter.Tk')  # Mockando a janela Tk principal
    @patch('main.app_state')  # Mockando o app_state
    @patch('main.PhotoImage')  # Mockando a criação da imagem
    @patch('main.ImageTk.PhotoImage')  # Mockando a criação de imagem do PIL (ImageTk)
    def test_vender_produto(self, mock_image_tk, mock_photoimage, mock_app_state, mock_tk, mock_toplevel, mock_askyesno, mock_showinfo, mock_showerror, mock_cursor):
        # Mock do retorno do banco de dados com fetchone
        mock_cursor.fetchone.return_value = (1, 'Produto A', 10, 20.0)  # Produto com preço de 20.0

        # Mock da janela de produto selecionado
        tela_produto = MagicMock()
        tela_produto.selection.return_value = [1]  # Simulando seleção do produto
        tela_produto.item.return_value = {'values': [1, 'Produto A', 20.0, 10]}

        # Mock da janela de venda
        tela_venda = MagicMock()

        # Mock para o campo de quantidade (digamos que a quantidade seja 2)
        mock_texto_qtde = MagicMock()
        mock_texto_qtde.get.return_value = '2'  # Simulando que o usuário inseriu a quantidade 2

        # Mock da label de preço total
        mock_label_preco_total = MagicMock()
        mock_label_preco_total.cget.return_value = "R$ 40.00"  # Simulando o valor do preço total

        # Mock da janela de venda (usando Toplevel)
        mock_vender_janela = MagicMock()
        mock_toplevel.return_value = mock_vender_janela  # Simula a janela que seria aberta

        # Mockando o método destroy para que não haja destruição real das janelas
        mock_vender_janela.destroy = MagicMock()
        mock_tk.return_value.destroy = MagicMock()

        # Mockando a resposta de askyesno para simular a confirmação positiva do usuário
        mock_askyesno.return_value = True  # Simula que o usuário clicou em "Sim"

        # Mock para a criação da imagem (evita o erro de criação de PhotoImage)
        mock_image_tk.return_value = MagicMock()

        # Mockando a função de janela inicial
        mock_tela_inicio = MagicMock()
        mock_app_state["tela_inicio"] = mock_tela_inicio  # Garantindo que tela_inicio esteja mockada

        # Executando a função de salvar a venda
        salvar_venda(
            (1, 'Produto A', 10, 20.0),  # Dados do produto
            mock_texto_qtde,
            mock_label_preco_total,  # A label de preço total
            tela_venda,
            mock_vender_janela  # Passando a janela mockada
        )

        # Verificar se o método de showinfo foi chamado
        mock_showinfo.assert_called_with("Sucesso", "Venda realizada!! Preço total: R$ 40.00")

        # Verificar se a função destroy foi chamada para a janela de venda
        mock_vender_janela.destroy.assert_called()

        # Verificar se a janela principal foi destruída (tela_inicio)
        mock_tk.return_value.destroy.assert_called()

        # Verificar se a janela inicial foi retirada (withdraw)
        mock_tela_inicio.withdraw.assert_called()

if __name__ == "__main__":
    unittest.main()
