"""
Este é o módulo principal do projeto.

"""
import sqlite3
import tkinter
from time import strftime
import datetime
from tkinter import messagebox as mb
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

def tela_inicial():
    """
    Tela inicial do sistema.
    """
    tela_inicio = tkinter.Tk()
    tela_inicio.title("Inicio")
    tela_inicio.resizable(False, False)
    tela_inicio.focus_force()
    app_state["tela_inicio"] = tela_inicio
    path = r"Projetos\Sistema de Estoque\wallpaper.png"
    bg = PhotoImage(path)
    label1 = Label(tela_inicio, image = bg)
    label1.place(x = 0,y = 0)

    label = tkinter.Label(
        tela_inicio, text="Bem vindo ao Sistema de Estoque!", font="Consolas 13 bold", bg="#FFFFFF")
    label.grid(row=0, column=1, pady=10, sticky='ew')

    image1 = Image.open(r"Projetos\Sistema de Estoque\logo.png")
    width, height = 400, 300
    image1.thumbnail((width, height))
    test = ImageTk.PhotoImage(image1)
    label1 = tkinter.Label(tela_inicio, image=test)
    label1.image = test
    label1.grid(row=1, column=1, pady=10, padx=47)

    button_vender = tkinter.Button(
        tela_inicio, text="Área de Vendas",
        font="Consolas 10",
        bg="#6B58FF",
        fg="white",
        command=tela_financeiro
    )
    button_vender.grid(row=2, column=1, padx=20, pady=10, sticky='ew')

    button = tkinter.Button(
        tela_inicio,
        text="Adicionar Novo Produto",
        font="Consolas 10",
        bg="#3D8EF0",
        fg="white",
        ommand=tela_add_produto
   )
    button.grid(row=3, column=1, padx=20, pady=10, sticky='ew')

    botao_prova = tkinter.Button(
        tela_inicio, text="Editar Produtos",
        font="Consolas 10",
        bg="#1CB9E4",
        fg="white",
        command=tela_edit_produto
    )
    botao_prova.grid(row=4, column=1, padx=20, pady=10, sticky='ew')

    cursor.execute("SELECT COUNT(*) FROM Produtos WHERE qtde < 5")
    baixo_estoque_count = cursor.fetchone()[0]

    if baixo_estoque_count > 0:
        botao_tabela = tkinter.Button(
            tela_inicio,
            text="Exibir Estoque ⚠️",
            font="Consolas 10 bold",
            bg="#0AB4B5",
            fg="#75163F",
            command=select_produto
        )
    else:
        botao_tabela = tkinter.Button(
            tela_inicio,
            text="Exibir Estoque",
            font="Consolas 10",
            bg="#0AB4B5",
            fg="white",
            command=select_produto
        )

    botao_tabela.grid(row=5, column=1, padx=20, pady=10, sticky='ew')

    button = tkinter.Button(
        tela_inicio,
        text="Sair do Programa",
        font="Consolas 10",
        bg="#4A2ED1",
        fg="white",
        command=tela_inicio.destroy
    )
    button.grid(row=6, column=1, padx=170, pady=50)

    label_hora = tkinter.Label(tela_inicio, font="Consolas 10")
    label_hora.grid(row=7, column=1, padx=10, sticky='e')

    def atualizar_hora():
        hora_atual = strftime("%H:%M:%S")
        label_hora.config(text=hora_atual , bg="#FFFFFF")
        tela_inicio.after(1000, atualizar_hora)

    atualizar_hora()

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

    imagem = Image.open(r"Projetos\Sistema de Estoque\logo2.png")
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

def tela_vender_prod():
    """
     Tela de venda de produtos.
    """
    app_state["janela_vendas"].withdraw()
    root_vender = tkinter.Tk()
    root_vender.resizable(False, False)
    root_vender.title("Vender Produto")
    root_vender.geometry("445x440")

    label = tkinter.Label(
    root_vender, text="Selecione o Produto que deseja Vender", font="Consolas 13 bold")
    label.grid(row=0, column=0, pady=10, sticky='ew')

    cursor.execute("SELECT * FROM Produtos")
    dados = cursor.fetchall()

    tabela = tkinter.Frame(root_vender)
    tabela.grid(row=1, column=0, padx=10, pady=10)

    tv = tkinter.ttk.Treeview(tabela, columns=(
        'id', 'nome', 'preco', 'qtde'), show='headings')
    tv.heading("id", text='ID')
    tv.column("id", width=50)
    tv.heading("nome", text='Nome')
    tv.heading('preco', text='Preço')
    tv.column("preco", width=120)
    tv.heading('qtde', text='Qtde')
    tv.column("qtde", width=50)

    for linha in dados:
        preco = linha[3]
        if preco:
            preco_formatado = f'R$ {float(preco):.2f}'
        else:
            preco_formatado = ''
        quantidade = linha[2]

        if quantidade <= 5:
            tv.insert('', 'end', values=(
                linha[0], linha[1], preco_formatado, linha[2]), tags=("baixo_estoque",))
        else:
            tv.insert('', 'end', values=(
                linha[0], linha[1], preco_formatado, linha[2]))

    tv.tag_configure("baixo_estoque", foreground="#EB3324")
    tv.pack()

    def vender_produto():
        item_selecionado = tv.selection()
        if item_selecionado:
            item = tv.item(item_selecionado)
            id_produto = item['values'][0]
            produto = cursor.execute(
                "SELECT * FROM Produtos WHERE iD=?", (id_produto,)).fetchone()
            if produto:
                vender_janela = tkinter.Toplevel()
                vender_janela.title("Vender Produto")
                vender_janela.resizable(False, False)
                vender_janela.geometry("400x300")

                label = tkinter.Label(
                    vender_janela, text="Preencha os campos a seguir", font="Consolas 13 bold")
                label.grid(row=0, column=1, pady=10, sticky='ew')

                label_nome = tkinter.Label(
                    vender_janela, text="Nome:", font="Consolas 10")
                label_nome.grid(row=1, column=0, padx=10, pady=15, sticky='ew')
                texto_nome = tkinter.StringVar(value=produto[1])
                nome = tkinter.Entry(vender_janela, textvariable=texto_nome)
                nome.grid(row=1, column=1, padx=8, pady=15, sticky='ew')
                label_qtde = tkinter.Label(
                    vender_janela, text="Qtde:", font="Consolas 10")
                label_qtde.grid(row=2, column=0, padx=10, pady=15, sticky='ew')
                texto_qtde = tkinter.StringVar(value=1)
                qtde = tkinter.Entry(vender_janela, textvariable=texto_qtde)
                qtde.grid(row=2, column=1, padx=8, pady=15, sticky='ew')

                def calcular_preco_total():
                    nova_qtde = int(qtde.get())
                    preco_total.config(
                        text=f"R$ {produto[3] * nova_qtde:.2f}"
                    )
                def aumentar_quantidade():
                    nova_quantidade = int(texto_qtde.get()) + 1
                    texto_qtde.set(nova_quantidade)
                    calcular_preco_total()

                botao_aumentar = tkinter.Button(
                    vender_janela, text="+", bg="#6B58FF", fg="white", command=aumentar_quantidade)
                botao_aumentar.grid(row=2, column=2, padx=5,
                                    pady=15, sticky='w')

                label_preco_total = tkinter.Label(
                    vender_janela, text="Preço Total:", font="Consolas 10")
                label_preco_total.grid(
                    row=3, column=0, padx=10, pady=15, sticky='ew')

                preco_total = tkinter.Label(
                    vender_janela, text="", font="Consolas 10 bold")
                preco_total.grid(row=3, column=1, padx=8, pady=15, sticky='ew')

                calcular_preco_total()

                def salvar_venda():
                    nova_qtde = int(qtde.get())

                    data_atual = datetime.datetime.now()

                    data_formatada = data_atual.strftime('%H:%M:%S, %d-%m-%Y')

                    if nova_qtde <= produto[2]:

                        calcular_preco_total()

                        if mb.askyesno(
                                 "Vender Produto",
                                 f"Vender produto '{produto[1]}' por '{preco_total.cget('text')}'?"
                        ):
                            cursor.execute(
                                "UPDATE Produtos SET qtde=qtde-? WHERE iD=?", 
                                (nova_qtde, id_produto)
                            )

                            cursor.execute(
                             """
                            INSERT INTO Vendas (nomeVenda, qtde, precoTotal, data)
                            VALUES (?, ?, ?, ?)
                             """,
                              (
                                produto[1],
                                nova_qtde,
                                preco_total.cget('text'),
                                data_formatada
                              )
                           )

                            connection.commit()

                            mb.showinfo(
                                "Sucesso",
                                f"Venda realizada!! Preço total: {preco_total.cget('text')}")
                            vender_janela.destroy()
                            root_vender.destroy()
                            app_state["tela_inicio"].withdraw().destroy()
                            tela_inicial()
                    else:
                        mb.showerror(
                            "Erro", "Quantidade insuficiente em estoque.")

                botao_salvar = tkinter.Button(
                    vender_janela, text="Salvar", bg="#6B58FF", fg="white", command=salvar_venda)
                botao_salvar.grid(row=4, column=1, padx=5,
                                  pady=10, sticky='ew')

                botao_voltar = tkinter.Button(
                                vender_janela,
                                text="Voltar",
                                bg="#3D8EF0",
                                fg="white",
                                command=vender_janela.destroy
                )
                botao_voltar.grid(row=5, column=1, padx=20,
                                  pady=10, sticky='ew')

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

    tv = tkinter.ttk.Treeview(tabela, columns=(
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

def tela_edit_produto():
    """
    Tela edição/atualização de produtos.
    """
    root_edit = tkinter.Tk()
    root_edit.resizable(False, False)
    root_edit.title("Editar Produto")
    root_edit.geometry("445x440")

    label = tkinter.Label(
        root_edit, text="Selecione o Produto que deseja Editar", font="Consolas 13 bold")
    label.grid(row=0, column=0, pady=10, sticky='ew')

    cursor.execute("SELECT * FROM Produtos")
    dados = cursor.fetchall()

    tabela = tkinter.Frame(root_edit)
    tabela.grid(row=1, column=0, padx=10, pady=10)

    tv = tkinter.ttk.Treeview(tabela, columns=(
        'id', 'nome', 'preco', 'qtde'), show='headings')
    tv.heading("id", text='ID')
    tv.column("id", width=50)
    tv.heading("nome", text='Nome')
    tv.heading('preco', text='Preço')
    tv.column("preco", width=120)
    tv.heading('qtde', text='Qtde')
    tv.column("qtde", width=50)

    for linha in dados:
        preco = linha[3]
        if preco:
            preco_formatado = f'R$ {float(preco):.2f}'
        else:
            preco_formatado = ''
        quantidade = linha[2]

        if quantidade <= 5:
            tv.insert('', 'end', values=(
                linha[0], linha[1], preco_formatado, linha[2]), tags=("baixo_estoque",))
        else:
            tv.insert('', 'end', values=(
                linha[0], linha[1], preco_formatado, linha[2]))

    tv.tag_configure("baixo_estoque", foreground="#EB3324")

    tv.pack()

    def editar_produto():
        item_selecionado = tv.selection()
        if item_selecionado:
            item = tv.item(item_selecionado)
            id_produto = item['values'][0]
            produto = cursor.execute(
                "SELECT * FROM Produtos WHERE iD=?", (id_produto,)).fetchone()
            if produto:
                editar_janela = tkinter.Tk()
                editar_janela.title("Editar Produto")
                editar_janela.resizable(False, False)
                editar_janela.geometry("360x300")

                centralizar_janela(editar_janela)

                label = tkinter.Label(
                    editar_janela, text="Preencha os campos a seguir", font="Consolas 13 bold")
                label.grid(row=0, column=1, pady=10, sticky='ew')

                label_nome = tkinter.Label(
                    editar_janela, text="Nome:", font="Consolas 10")
                label_nome.grid(row=1, column=0, padx=10, pady=15, sticky='ew')
                texto_nome = tkinter.StringVar(value=produto[1])
                nome = tkinter.Entry(editar_janela, textvariable=texto_nome)
                nome.grid(row=1, column=1, padx=8, pady=15, sticky='ew')

                label_qtde = tkinter.Label(
                    editar_janela, text="Qtde:", font="Consolas 10")
                label_qtde.grid(row=2, column=0, padx=10, pady=15, sticky='ew')
                texto_qtde = tkinter.StringVar(value=produto[2])
                qtde = tkinter.Entry(editar_janela, textvariable=texto_qtde)
                qtde.grid(row=2, column=1, padx=8, pady=15, sticky='ew')

                label_preco = tkinter.Label(
                    editar_janela, text="Preço:", font="Consolas 10")
                label_preco.grid(row=3, column=0, padx=10,
                                 pady=15, sticky='ew')
                texto_preco = tkinter.StringVar(value=produto[3])
                preco = tkinter.Entry(editar_janela, textvariable=texto_preco)
                preco.grid(row=3, column=1, padx=8, pady=15, sticky='ew')

                def salvar_edicao():
                    novo_nome = nome.get()
                    nova_qtde = qtde.get()
                    novo_preco = preco.get()

                    try:
                        nova_qtde = int(nova_qtde)
                        novo_preco = float(novo_preco.replace(
                            ',', '.').replace('R$', ''))
                        cursor.execute("UPDATE Produtos SET nome=?, qtde=?, preco=? WHERE iD=?",
                                       (novo_nome, nova_qtde, novo_preco, id_produto))
                        connection.commit()
                        mb.showinfo(
                            "Sucesso", "Produto atualizado com sucesso!")
                        editar_janela.destroy()
                        root_edit.destroy()

                        app_state["tela_inicio"].withdraw().destroy()
                        tela_inicial()
                    except ValueError:
                        mb.showerror(
                            "Erro", "Por favor, insira uma quantidade e preço válidos.")

                botao_salvar = tkinter.Button(
                    editar_janela, text="Salvar", bg="#6B58FF", fg="white", command=salvar_edicao)
                botao_salvar.grid(row=4, column=1, padx=5,
                                  pady=10, sticky='ew')

                botao_voltar = tkinter.Button(
                                    editar_janela,
                                    text="Voltar",
                                    bg="#3D8EF0",
                                    fg="white",
                                    command=editar_janela.destroy
                )
                botao_voltar.grid(row=5, column=1, padx=20,
                                  pady=10, sticky='ew')

    def deletar_produto():

        itens_selecionados = tv.selection()

        if itens_selecionados:
            itens_para_deletar = []

            for item_selecionado in itens_selecionados:

                item = tv.item(item_selecionado)
                nome_produto = item['values'][1]
                itens_para_deletar.append((item['values'][0], nome_produto))

            if mb.askyesno(
                "Deletar Produtos",
                "Deseja mesmo deletar os produtos selecionados?",
                icon='warning'
                ):
                for id_produto, _ in itens_para_deletar:
                    cursor.execute(
                        "DELETE FROM Produtos WHERE iD=?", (id_produto,))

                connection.commit()
                root_edit.destroy()
                app_state["tela_inicio"].withdraw().destroy()
                tela_inicial()

    botao_editar = tkinter.Button(
        root_edit, text="Editar", bg="#6B58FF", fg="white", command=editar_produto)
    botao_editar.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    botao_deletar = tkinter.Button(
        root_edit, text="Deletar", bg="#3D8EF0", fg="white", command=deletar_produto)
    botao_deletar.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    botao_fechar = tkinter.Button(
        root_edit, text="Voltar", bg="#1CB9E4", fg="white", command=root_edit.destroy)
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

    tv = tkinter.ttk.Treeview(tabela, columns=(
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
