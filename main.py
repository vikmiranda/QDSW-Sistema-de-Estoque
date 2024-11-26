"""
Este é o módulo principal do projeto.

"""
import sqlite3
import tkinter
from tkinter import messagebox as mb, Label, PhotoImage, ttk
from time import strftime
import datetime
from PIL import Image, ImageTk

app_state = {
    "tela_inicio": None,
    "janela_vendas": None,
    "janela_add": None
}

connection = sqlite3.connect("Database.db")
cursor = connection.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Produtos (
        iD INTEGER PRIMARY KEY,
        nome TEXT,
        qtde INTEGER,
        preco REAL
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Vendas (
        iD INTEGER PRIMARY KEY,
        nomeVenda TEXT,
        qtde INTEGER,
        precoTotal REAL,
        data TEXT
    )
    """
)


def criar_janela_inicial():
    """Cria a janela inicial."""
    tela_inicio = tkinter.Tk()
    tela_inicio.title("Inicio")
    tela_inicio.resizable(False, False)
    tela_inicio.focus_force()
    return tela_inicio

def configurar_background(tela_inicio, caminho_imagem):
    """Configura o fundo da tela."""
    bg = PhotoImage(file=caminho_imagem)
    label_bg = Label(tela_inicio, image=bg)
    label_bg.image = bg
    label_bg.place(x=0, y=0)

def adicionar_logo(tela_inicio, caminho_logo):
    """Adiciona o logotipo à tela."""
    image = Image.open(caminho_logo)
    image.thumbnail((400, 300))
    test = ImageTk.PhotoImage(image)
    label_logo = tkinter.Label(tela_inicio, image=test)
    label_logo.image = test
    label_logo.grid(row=1, column=1, pady=10, padx=47)

def criar_botao(tela, texto, comando, cor_fundo="#FFFFFF", row=0, **kwargs):
    """
    Cria e posiciona um botão.

    Parâmetros:
    - tela: Widget pai onde o botão será inserido.
    - texto: Texto exibido no botão.
    - comando: Função executada ao clicar no botão.
    - cor_fundo: Cor de fundo do botão.
    - row: Posição (linha) do botão.
    - kwargs: Configurações opcionais adicionais, como padx, pady, column, sticky.
    """
    padrao_kwargs = {
        "font": "Consolas 10",
        "bg": cor_fundo,
        "fg": "white",
        "command": comando,
        "row": row,
        "column": 1,
        "padx": 20,
        "pady": 10,
        "sticky": 'ew'
    }
    padrao_kwargs.update(kwargs)

    botao = tkinter.Button(
        tela,
        text=texto,
        font=padrao_kwargs["font"],
        bg=padrao_kwargs["bg"],
        fg=padrao_kwargs["fg"],
        command=padrao_kwargs["command"]
    )
    botao.grid(
        row=padrao_kwargs["row"],
        column=padrao_kwargs["column"],
        padx=padrao_kwargs["padx"],
        pady=padrao_kwargs["pady"],
        sticky=padrao_kwargs["sticky"]
    )
    return botao

def criar_label(tela_inicio, texto, column, row):
    """Cria um label."""
    label = tkinter.Label(
        tela_inicio,
        text=texto,
        font="Consolas 13 bold",
        bg="#FFFFFF"
    )
    label.grid(row=row, column=column, pady=10, sticky='ew')
    return label

def exibir_estoque_botao(tela_inicio, baixo_estoque_count):
    """Cria o botão para exibir estoque com ou sem alerta."""
    exibir_texto = "Exibir Estoque ⚠️" if baixo_estoque_count > 0 else "Exibir Estoque"
    cor_texto = "#75163F" if baixo_estoque_count > 0 else "white"
    criar_botao(
        tela_inicio,
        exibir_texto,
        select_produto,
        cor_fundo="#0AB4B5",
        row=5
    ).config(fg=cor_texto)

def atualizar_hora(label_hora, tela_inicio):
    """Atualiza a hora no label."""
    def tick():
        hora_atual = strftime("%H:%M:%S")
        label_hora.config(text=hora_atual, bg="#FFFFFF")
        tela_inicio.after(1000, tick)

    tick()

def tela_inicial():
    """Tela inicial do sistema."""
    tela_inicio = criar_janela_inicial()
    app_state["tela_inicio"] = tela_inicio  # Salva no estado global

    configurar_background(tela_inicio, r"wallpaper.png")
    criar_label(tela_inicio, "Bem vindo ao Sistema de Estoque!", row=0, column=1)
    adicionar_logo(tela_inicio, r"logo.png")

    criar_botao(tela_inicio, "Área de Vendas", tela_financeiro, cor_fundo="#6B58FF", row=2)
    criar_botao(tela_inicio, "Adicionar Novo Produto", tela_add_produto, cor_fundo="#3D8EF0", row=3)
    criar_botao(tela_inicio, "Editar Produtos", tela_edit_produto, cor_fundo="#1CB9E4", row=4)

    cursor.execute("SELECT COUNT(*) FROM Produtos WHERE qtde < 5")
    baixo_estoque_count = cursor.fetchone()[0]
    exibir_estoque_botao(tela_inicio, baixo_estoque_count)

    criar_botao(tela_inicio, "Sair do Programa",
                tela_inicio.destroy, cor_fundo="#4A2ED1", row=6, padx=170, pady=50)

    label_hora = tkinter.Label(tela_inicio, font="Consolas 10")
    label_hora.grid(row=7, column=1, padx=10, sticky='e')
    atualizar_hora(label_hora, tela_inicio)

    tela_inicio.mainloop()


def tela_financeiro():
    """
    Tela de vendas do sistema.
    """
    app_state["tela_inicio"].withdraw()
    janela_vendas = tkinter.Toplevel()
    janela_vendas.resizable(False, False)
    janela_vendas.geometry("325x520")
    janela_vendas.title("Área de Vendas")
    app_state["janela_vendas"] = janela_vendas

    label = tkinter.Label(
        janela_vendas, text="Área Financeira", font="Consolas 13 bold")
    label.grid(row=0, column=0, pady=10, sticky='ew')

    imagem = Image.open(r"logo2.png")
    width, height = 400, 300
    imagem.thumbnail((width, height))
    imagem = ImageTk.PhotoImage(imagem)
    label_imagem = tkinter.Label(janela_vendas, image=imagem)
    label_imagem.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
    label_imagem.image = imagem

    botao_vender = tkinter.Button(
    janela_vendas, text="Realizar uma Venda", bg="#6B58FF", fg="white", command=tela_vender_prod)
    botao_vender.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

    botao_consulta = tkinter.Button(
        janela_vendas, text="Consultar Vendas", bg="#3D8EF0", fg="white", command=exibir_vendas)
    botao_consulta.grid(row=3, column=0, padx=10, pady=10, sticky='ew')

    botao_voltar = tkinter.Button(
        janela_vendas,
        text="Voltar para Tela Inicial",
        bg="#1CB9E4",
        fg="white",
        command=lambda: [janela_vendas.destroy(),
        app_state["tela_inicio"].withdraw().deiconify()]
    )
    botao_voltar.grid(row=4, column=0, padx=100, pady=10, sticky='ew')

def verificar_estoque(tela_produtos):
    """
    busca produto no banco de dados e verifica quantidade.
    retorna uma tela tkinter com informação da quantidade.
    """
    cursor.execute("SELECT * FROM Produtos")
    dados = cursor.fetchall()

    for linha in dados:
        preco = linha[3]
        if preco:
            preco_formatado = f'R$ {float(preco):.2f}'
        else:
            preco_formatado = ''
        quantidade = linha[2]

        if quantidade <= 5:
            tela_produtos.insert('', 'end', values=(
                linha[0], linha[1], preco_formatado, linha[2]), tags=("baixo_estoque",))
        else:
            tela_produtos.insert('', 'end', values=(
                linha[0], linha[1], preco_formatado, linha[2]))
    return tela_produtos

def vender_produto(tela_venda, tela_produto):
    """
    Inicia o processo de venda de um produto selecionado na interface de produtos.

    Args:
        tela_venda (tkinter.Widget): A janela atual de vendas.
        tela_produto (tkinter.Widget): A interface com a lista de produtos.

    Returns:
        None
    """
    item_selecionado = tela_produto.selection()
    if not item_selecionado:
        mb.showerror("Erro", "Nenhum produto selecionado.")
        return

    id_produto = tela_produto.item(item_selecionado)['values'][0]
    produto = buscar_produtos(id_produto)

    if not produto:
        mb.showerror("Erro", "Produto não encontrado.")
        return

    vender_janela = tkinter.Toplevel()
    vender_janela.title("Vender Produto")
    vender_janela.resizable(False, False)
    vender_janela.geometry("400x300")

    criar_label(vender_janela, "Preencha os campos a seguir", column=1, row=0)

    criar_entrada_com_label(
        vender_janela, "Nome:", produto[1], row=1
    )

    texto_qtde = criar_entrada_com_label(
        vender_janela, "Qtde:", "1", row=2
    )

    label_preco_total = criar_label(vender_janela, "", row=3, column=1)

    calcular_label_preco_total(produto, texto_qtde, label_preco_total)

    botao_aumentar = tkinter.Button(
        vender_janela, text="+", bg="#6B58FF", fg="white",
        command=lambda: aumentar_quantidade(texto_qtde, produto, label_preco_total)
    )
    botao_aumentar.grid(row=2, column=2, padx=5, pady=15, sticky='w')

    criar_label(vender_janela, "Preço Total:", row=3, column=0)

    botao_salvar = tkinter.Button(
        vender_janela, text="Salvar", bg="#6B58FF", fg="white",
        command=lambda: salvar_venda(
            produto, texto_qtde, label_preco_total, tela_venda, vender_janela
        )
    )
    botao_salvar.grid(row=4, column=1, padx=5, pady=10, sticky='ew')

    botao_voltar = tkinter.Button(
        vender_janela, text="Voltar", bg="#3D8EF0", fg="white",
        command=vender_janela.destroy
    )
    botao_voltar.grid(row=5, column=1, padx=20, pady=10, sticky='ew')


def buscar_produtos(id_produto=None):
    """
    Busca produtos no banco de dados.
    Args:
        id_produto: O ID do produto a ser buscado. 
        Se não fornecido, retorna todos os produtos.
    Returns:
        list/tuple: Lista com os dados dos produtos ou uma tupla com o produto encontrado, 
                    ou None se não encontrado.
    """
    if id_produto:
        return cursor.execute(
            "SELECT * FROM Produtos WHERE iD=?", (id_produto,)
        ).fetchone()

    cursor.execute("SELECT * FROM Produtos")
    return cursor.fetchall()


def aumentar_quantidade(texto_qtde, produto, label_preco_total):
    """
    Incrementa a quantidade selecionada e recalcula o preço total.

    Args:
        texto_qtde (tkinter.StringVar): A variável vinculada ao campo de quantidade.
        produto (tuple): Os dados do produto.
        label_preco_total (tkinter.Label): O rótulo onde o preço total é exibido.

    Returns:
        None
    """
    try:
        nova_quantidade = int(texto_qtde.get()) + 1
        texto_qtde.set(nova_quantidade)
        calcular_label_preco_total(produto, texto_qtde, label_preco_total)
    except ValueError:
        texto_qtde.set("1")
        calcular_label_preco_total(produto, texto_qtde, label_preco_total)


def calcular_label_preco_total(produto, texto_qtde, label_preco_total):
    """
    Recalcula e atualiza o preço total com base na quantidade selecionada.

    Args:
        produto (tuple): Os dados do produto.
        texto_qtde (tkinter.StringVar): A variável vinculada ao campo de quantidade.
        label_preco_total (tkinter.Label): O rótulo onde o preço total é exibido.

    Returns:
        None
    """
    try:
        nova_qtde = int(texto_qtde.get())
        label_preco_total.config(
            text=f"R$ {produto[3] * nova_qtde:.2f}"
        )
    except ValueError:
        label_preco_total.config(text="R$ 0.00")


def salvar_venda(produto, texto_qtde, label_preco_total, tela_venda, vender_janela):
    """
    Salva a venda no banco de dados, atualiza o estoque e exibe mensagens de sucesso ou erro.

    Args:
        produto (tuple): Os dados do produto.
        texto_qtde (tkinter.StringVar): A variável vinculada ao campo de quantidade.
        label_preco_total (tkinter.Label): O rótulo onde o preço total é exibido.
        tela_venda (tkinter.Widget): A janela atual de vendas.
        vender_janela (tkinter.Toplevel): A janela atual de venda do produto.

    Returns:
        None
    """
    try:
        nova_qtde = int(texto_qtde.get())
    except ValueError:
        mb.showerror("Erro", "Quantidade inválida.")
        return

    if nova_qtde > produto[2]:
        mb.showerror("Erro", "Quantidade insuficiente em estoque.")
        return

    if not mb.askyesno(
        "Vender Produto",
        f"Vender produto '{produto[1]}' por '{label_preco_total.cget('text')}'?",
    ):
        return

    data_atual = datetime.datetime.now().strftime('%H:%M:%S, %d-%m-%Y')

    cursor.execute(
        "UPDATE Produtos SET qtde=qtde-? WHERE iD=?", (nova_qtde, produto[0])
    )
    cursor.execute(
        """
        INSERT INTO Vendas (nomeVenda, qtde, precoTotal, data)
        VALUES (?, ?, ?, ?)
        """,
        (produto[1], nova_qtde, label_preco_total.cget('text'), data_atual),
    )

    connection.commit()

    mb.showinfo(
        "Sucesso",
        f"Venda realizada!! Preço total: {label_preco_total.cget('text')}",
    )
    vender_janela.destroy()
    tela_venda.destroy()
    app_state["tela_inicio"].withdraw().destroy()
    tela_inicial()


def criar_entrada_com_label(janela, texto_label, valor_inicial, row):
    """
    Cria um campo de entrada com rótulo associado.

    Args:
        janela (tkinter.Widget): A janela onde o campo será criado.
        texto_label (str): O texto do rótulo.
        valor_inicial (str): O valor inicial do campo de entrada.
        row (int): A linha onde o campo será posicionado.

    Returns:
        tkinter.StringVar: A variável vinculada ao campo de entrada.
    """
    criar_label(janela, texto_label, row=row, column=0)
    texto_var = tkinter.StringVar(value=valor_inicial)
    entrada = tkinter.Entry(janela, textvariable=texto_var)
    entrada.grid(row=row, column=1, padx=8, pady=15, sticky='ew')
    return texto_var

def tela_vender_prod():
    """
     Tela de venda de produtos.
    """
    app_state["janela_vendas"].withdraw()
    root_vender = tkinter.Tk()
    root_vender.resizable(False, False)
    root_vender.title("Vender Produto")
    root_vender.geometry("445x440")

    criar_label(root_vender,"Selecione o Produto que deseja Vender",0,0)
    tabela = tkinter.Frame(root_vender)
    tabela.grid(row=1, column=0, padx=10, pady=10)

    tv = ttk.Treeview(tabela, columns=(
        'id', 'nome', 'preco', 'qtde'), show='headings')
    tv.heading("id", text='ID')
    tv.column("id", width=50)
    tv.heading("nome", text='Nome')
    tv.heading('preco', text='Preço')
    tv.column("preco", width=120)
    tv.heading('qtde', text='Qtde')
    tv.column("qtde", width=50)

    tv = verificar_estoque(tela_produtos=tv)
    tv.tag_configure("baixo_estoque", foreground="#EB3324")
    tv.pack()
    vender_produto(root_vender, tv)

    botao_vender = tkinter.Button(
        root_vender, text="Vender Produto", bg="#6B58FF", fg="white", command=vender_produto)
    botao_vender.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    botao_voltar = tkinter.Button(
                     root_vender,
                     text="Voltar",
                     bg="#3D8EF0",
                     fg="white",
                     command=lambda: [root_vender.destroy(),
                     app_state["janela_vendas"].deiconify()]
    )
    botao_voltar.grid(row=3, column=0, padx=20, pady=10, sticky='ew')

def exibir_vendas():
    """
    Tela de consulta - Histórico de Vendas.
    """
    root_consulta = tkinter.Tk()
    root_consulta.resizable(False, False)
    root_consulta.title("Vendas")
    root_consulta.geometry("562x400")

    label = tkinter.Label(
        root_consulta, text="Histórico de Vendas", font="Consolas 13 bold")
    label.grid(row=0, column=0, pady=10, sticky='ew')

    cursor.execute("SELECT * FROM Vendas")
    vendas_data = cursor.fetchall()

    tabela = tkinter.Frame(root_consulta)
    tabela.grid(row=1, column=0, padx=10, pady=10)

    tv = ttk.Treeview(tabela, columns=(
        'ID', 'Nome', 'Quantidade', 'Preço Total', 'Data'), show='headings')
    tv.heading("ID", text='ID')
    tv.column("ID", width=50)
    tv.heading('Nome', text='Nome do Produto')
    tv.heading('Quantidade', text='Qtde')
    tv.column("Quantidade", width=50)
    tv.heading('Preço Total', text='Preço Total')
    tv.column("Preço Total", width=120)
    tv.heading('Data', text='Data')
    tv.column("Data", width=120)

    for venda in vendas_data:
        tv.insert('', 'end', values=venda)

    tv.pack()
    botao_fechar = tkinter.Button(
        root_consulta, text="Voltar", bg="#6B58FF", fg="white", command=root_consulta.destroy)
    botao_fechar.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

def tela_add_produto():
    """
    Tela para cadastramento de produtos
    """

    janela_add = tkinter.Tk()
    janela_add.resizable(False, False)
    janela_add.geometry("435x320")
    janela_add.title("Cadastro de Produtos")
    centralizar_janela(janela_add)
    app_state["janela_add"] = janela_add
    label = tkinter.Label(
        janela_add, text="Preencha os campos a seguir", font="Consolas 13 bold")
    label.grid(row=0, column=1, pady=10, sticky='ew')

    label_nome = tkinter.Label(janela_add, text="Nome:", font="Consolas 10")
    label_nome.grid(row=1, column=0, padx=10, pady=15, sticky='ew')
    texto_nome = tkinter.StringVar()
    nome = tkinter.Entry(janela_add, textvariable=texto_nome)
    nome.grid(row=1, column=1, padx=8, pady=15, sticky='ew')

    label_qtde = tkinter.Label(janela_add, text="Qtde:", font="Consolas 10")
    label_qtde.grid(row=2, column=0, padx=10, pady=15, sticky='ew')
    texto_qtde = tkinter.StringVar()
    qtde = tkinter.Entry(janela_add, textvariable=texto_qtde)
    qtde.grid(row=2, column=1, padx=8, pady=15, sticky='ew')

    label_preco = tkinter.Label(janela_add, text="Preço:", font="Consolas 10")
    label_preco.grid(row=3, column=0, padx=10, pady=15, sticky='ew')
    texto_preco = tkinter.StringVar()
    preco = tkinter.Entry(janela_add, textvariable=texto_preco)
    preco.grid(row=3, column=1, padx=8, pady=15, sticky='ew')

    botao_add = tkinter.Button(
                    janela_add,
                    text="Concluir",
                    bg="#6B58FF",
                    fg="white",
                    command=lambda: add_produto(nome.get(),
                    qtde.get(),
                    preco.get())
    )
    botao_add.grid(row=4, column=1, padx=10, pady=10, sticky='ew')

    botao_voltar = tkinter.Button(
                        janela_add,
                        text="Voltar para Tela Inicial",
                        bg="#3D8EF0",
                        fg="white",
                        command=lambda: [janela_add.destroy(),
                        app_state["tela_inicio"].withdraw().destroy(),
                        tela_inicial()]
    )
    botao_voltar.grid(row=5, column=1, padx=100, pady=10, sticky='ew')

    def add_produto(nome, qtde, preco):
        janela_add.destroy()

        try:
            qtde = int(qtde)
            preco = float(preco.replace(',', '.').replace('R$', ''))
            cursor.execute(
                "INSERT INTO Produtos (nome, qtde, preco) VALUES (?, ?, ?)", (nome, qtde, preco))
            connection.commit()
        except ValueError:
            mb.showerror(
                "Erro", "Por favor, insira uma quantidade e preço válidos.")
            tela_add_produto()
            return

        mb.showinfo(
            "Sucesso", f"'{nome}'({qtde}) Adicionado ao Estoque .")

        if mb.askyesno("Adicionar outro produto", "Deseja adicionar outro produto?"):
            tela_add_produto()

def salvar_edicao(id_produto, nome, qtde, preco):
    """
    Salva as edições feitas no produto no banco de dados.

    Args:
        id_produto (int): ID do produto a ser atualizado.
        nome (str): Novo nome do produto.
        qtde (int): Nova quantidade do produto.
        preco (float): Novo preço do produto.

    Returns:
        bool: True se a atualização foi bem-sucedida, False caso contrário.
    """
    try:
        qtde = int(qtde)
        preco = float(preco.replace(',', '.').replace('R$', ''))
        cursor.execute(
            "UPDATE Produtos SET nome=?, qtde=?, preco=? WHERE iD=?",
            (nome, qtde, preco, id_produto)
        )
        connection.commit()
        return True
    except ValueError:
        return False

def deletar_produtos(itens_para_deletar):
    """
    Deleta produtos do banco de dados.

    Args:
        itens_para_deletar (list): Lista de tuplas contendo ID e nome do produto a ser deletado.

    Returns:
        None
    """
    for id_produto, _ in itens_para_deletar:
        cursor.execute("DELETE FROM Produtos WHERE iD=?", (id_produto,))
    connection.commit()

def criar_campos_edicao(editar_janela, produto):
    """
    Cria os campos de edição para o produto.

    Args:
        editar_janela (Tk): A janela onde os campos serão criados.
        produto (tuple): Os dados do produto a ser editado.

    Returns:
        tuple: Os campos de nome, quantidade e preço.
    """
    texto_nome = tkinter.StringVar(value=produto[1])
    nome = tkinter.Entry(editar_janela, textvariable=texto_nome)
    nome.grid(row=1, column=1, padx=8, pady=15, sticky='ew')

    texto_qtde = tkinter.StringVar(value=produto[2])
    qtde = tkinter.Entry(editar_janela, textvariable=texto_qtde)
    qtde.grid(row=2, column=1, padx=8, pady=15, sticky='ew')

    texto_preco = tkinter.StringVar(value=produto[3])
    preco = tkinter.Entry(editar_janela, textvariable=texto_preco)
    preco.grid(row=3, column=1, padx=8, pady=15, sticky='ew')

    return nome, qtde, preco

# Função para editar um produto
def editar_produto(tv):
    """
    Permite editar um produto selecionado na tabela.

    Args:
        tv (Treeview): A tabela de produtos onde o item será selecionado para edição.

    Returns:
        None
    """
    item_selecionado = tv.selection()
    if item_selecionado:
        item = tv.item(item_selecionado)
        id_produto = item['values'][0]

        # Buscando o produto no banco de dados
        produto = buscar_produtos(id_produto)

        if produto:
            editar_janela = tkinter.Tk()
            editar_janela.title("Editar Produto")
            editar_janela.resizable(False, False)
            editar_janela.geometry("360x300")
            centralizar_janela(editar_janela)

            # Criando o título diretamente na função principal
            label = tkinter.Label(
                editar_janela, text="Preencha os campos a seguir", font="Consolas 13 bold"
            )
            label.grid(row=0, column=1, pady=10, sticky='ew')

            # Criando campos de edição
            nome, qtde, preco = criar_campos_edicao(editar_janela, produto)

            # Botão para salvar a edição
            botao_salvar = tkinter.Button(
                editar_janela, text="Salvar", bg="#6B58FF", fg="white",
                command=lambda: salvar_edicao(id_produto, nome.get(), qtde.get(), preco.get())
            )
            botao_salvar.grid(row=4, column=1, padx=5, pady=10, sticky='ew')

            # Botão para voltar
            botao_voltar = tkinter.Button(
                editar_janela, text="Voltar", bg="#3D8EF0", fg="white",
                command=editar_janela.destroy
            )
            botao_voltar.grid(row=5, column=1, padx=20, pady=10, sticky='ew')

def deletar_produto(tv):
    """
    Deleta os produtos selecionados na tabela.

    Args:
        tv (Treeview): A tabela de produtos onde os itens serão selecionados para exclusão.

    Returns:
        None
    """
    itens_selecionados = tv.selection()
    if itens_selecionados:
        itens_para_deletar = [(tv.item(item)['values'][0],
                                tv.item(item)['values'][1])
                                for item in itens_selecionados]

        logica_confirmacao_deletar = mb.askyesno("Deletar Produtos",
                       "Deseja mesmo deletar os produtos selecionados?",
                       icon='warning')
        if logica_confirmacao_deletar:
            deletar_produtos(itens_para_deletar)
            app_state["tela_inicio"].withdraw().destroy()
            tela_inicial()

def tela_edit_produto():
    """
    Tela de edição e atualização de produtos.
    """
    root_edit = tkinter.Tk()
    root_edit.resizable(False, False)
    root_edit.title("Editar Produto")
    root_edit.geometry("445x440")

    label = tkinter.Label(
        root_edit, text="Selecione o Produto que deseja Editar", font="Consolas 13 bold"
    )
    label.grid(row=0, column=0, pady=10, sticky='ew')

    dados = buscar_produtos()

    tabela = tkinter.Frame(root_edit)
    tabela.grid(row=1, column=0, padx=10, pady=10)

    tv = ttk.Treeview(tabela, columns=('id', 'nome', 'preco', 'qtde'), show='headings')
    tv.heading("id", text='ID')
    tv.column("id", width=50)
    tv.heading("nome", text='Nome')
    tv.heading('preco', text='Preço')
    tv.column("preco", width=120)
    tv.heading('qtde', text='Qtde')
    tv.column("qtde", width=50)

    for linha in dados:
        preco = linha[3]
        preco_formatado = f'R$ {float(preco):.2f}' if preco else ''
        quantidade = linha[2]
        tag = "baixo_estoque" if quantidade <= 5 else ""
        tv.insert('', 'end', values=(linha[0], linha[1], preco_formatado, linha[2]), tags=(tag,))

    tv.tag_configure("baixo_estoque", foreground="#EB3324")
    tv.pack()


    botao_editar = tkinter.Button(
        root_edit, text="Editar", bg="#6B58FF", fg="white", command=lambda: editar_produto(tv)
    )
    botao_editar.grid(row=2, column=0, padx=10, pady=10, sticky="ew")


    botao_deletar = tkinter.Button(
        root_edit, text="Deletar", bg="#3D8EF0", fg="white", command=lambda: deletar_produto(tv)
    )
    botao_deletar.grid(row=3, column=0, padx=10, pady=10, sticky="ew")


    botao_fechar = tkinter.Button(
        root_edit, text="Voltar", bg="#1CB9E4", fg="white", command=root_edit.destroy
    )
    botao_fechar.grid(row=4, column=0, padx=50, pady=10, sticky="ew")


def select_produto():
    """
    Tela tabela de produtos.
    """
    root_select = tkinter.Tk()
    root_select.resizable(False, False)
    root_select.title("Tabela de Produtos")
    root_select.geometry("622x400")

    label = tkinter.Label(
        root_select, text="Estoque dos Produtos", font="Consolas 13 bold")
    label.grid(row=0, column=0, pady=10, sticky='ew')

    cursor.execute("SELECT * FROM Produtos")
    dados = cursor.fetchall()

    tabela = tkinter.Frame(root_select)
    tabela.grid(row=1, column=0, padx=10, pady=10)

    tv = ttk.Treeview(tabela, columns=(
        'nome', 'preco', 'qtde'), show='headings')
    tv.heading("nome", text='Nome')
    tv.heading('preco', text='Preço')
    tv.heading('qtde', text='Quantidade')

    for linha in dados:
        preco = linha[3]

        if preco:
            preco_formatado = f'R$ {float(preco):.2f}'
        else:
            preco_formatado = ''

        quantidade = linha[2]

        if quantidade < 10:
            tv.insert('', 'end', values=(
                linha[1], preco_formatado, linha[2]), tags=("baixo_estoque",))
        else:
            tv.insert('', 'end', values=(linha[1], preco_formatado, linha[2]))

    tv.tag_configure("baixo_estoque", foreground="#EB3324")

    tv.pack()
    botao_fechar = tkinter.Button(
        root_select, text="Voltar", bg="#6B58FF", fg="white", command=root_select.destroy)
    botao_fechar.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

def centralizar_janela(janela):
    """
    Ajuiste de janela - Centralização.
    """
    largura_janela = janela.winfo_reqwidth()
    altura_janela = janela.winfo_reqheight()

    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    posicao_x = (largura_tela // 2) - (largura_janela // 2)
    posicao_y = (altura_tela // 2) - (altura_janela // 2)

    janela.geometry(f"+{posicao_x}+{posicao_y}")

tela_inicial()
cursor.execute("SELECT * FROM Vendas")
connection.commit()
