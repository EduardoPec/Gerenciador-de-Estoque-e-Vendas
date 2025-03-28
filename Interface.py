import flet as ft
from datetime import datetime
from Aplicacao import Banco_Dados, Produto, Venda, ExecutarProduto, ExecutarVenda

def main(page: ft.Page):
    page.title = "Sistema de Vendas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1100
    page.window_height = 700
    page.padding = 20
    page.fonts = {
        "Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap"
    }
    page.theme = ft.Theme(font_family="Poppins")

    colors = {
        "primary": "#4F46E5",
        "secondary": "#10B981",
        "background": "#F9FAFB",
        "card": "#FFFFFF",
        "text": "#374151",
        "error": "#EF4444"
    }

    executar_produto = ExecutarProduto()
    executar_venda = ExecutarVenda()

    def build_header(title, icon=None):
        return ft.Row(
            controls=[
                ft.Icon(icon, color=colors["primary"]) if icon else ft.Container(),
                ft.Text(title, size=22, weight="bold", color=colors["primary"])
            ],
            spacing=10
        )

    produto_id = ft.TextField(visible=False)
    produto_nome = ft.TextField(
        label="Nome do produto",
        border_color=colors["primary"],
        filled=True,
        bgcolor=colors["card"],
        width=400
    )
    produto_desc = ft.TextField(
        label="Descrição",
        multiline=True,
        border_color=colors["primary"],
        filled=True,
        bgcolor=colors["card"]
    )
    produto_qtd = ft.TextField(
        label="Quantidade",
        border_color=colors["primary"],
        filled=True,
        bgcolor=colors["card"],
        width=150,
        input_filter=ft.NumbersOnlyInputFilter()
    )
    produto_preco = ft.TextField(
        label="Preço",
        prefix_text="R$ ",
        border_color=colors["primary"],
        filled=True,
        bgcolor=colors["card"],
        width=150,
        input_filter=ft.NumbersOnlyInputFilter()
    )

    btn_salvar_produto = ft.ElevatedButton(
        "Salvar produto",
        icon=ft.icons.SAVE,
        color="white",
        bgcolor=colors["secondary"],
        height=45
    )
    
    btn_novo_produto = ft.ElevatedButton(
        "Novo produto",
        icon=ft.icons.ADD,
        color="white",
        bgcolor=colors["primary"],
        height=45
    )

    lista_produtos = ft.ListView(expand=True, spacing=10)

    pesquisa_produto_tipo = ft.Dropdown(
        label="Pesquisar por",
        options=[
            ft.dropdown.Option("todos", "Todos os produtos"),
            ft.dropdown.Option("id", "ID"),
            ft.dropdown.Option("nome", "Nome"),
            ft.dropdown.Option("descricao", "Descrição"),
            ft.dropdown.Option("quantidade", "Quantidade"),
            ft.dropdown.Option("preco", "Preço")
        ],
        value="todos",
        width=200
    )
    
    pesquisa_produto_valor = ft.TextField(
        label="Valor da pesquisa",
        width=300,
        visible=False
    )
    
    btn_pesquisar_produto = ft.ElevatedButton(
        "Pesquisar",
        icon=ft.icons.SEARCH,
        height=45
    )

    def atualizar_pesquisa_produto(e):
        pesquisa_produto_valor.visible = pesquisa_produto_tipo.value != "todos"
        page.update()

    pesquisa_produto_tipo.on_change = atualizar_pesquisa_produto

    def carregar_produtos(e=None):
        tipo = pesquisa_produto_tipo.value
        valor = pesquisa_produto_valor.value
        
        try:
            if tipo == "todos":
                produtos = executar_produto.PesquisarProduto_todos()
            elif tipo == "id":
                produtos = [executar_produto.PesquisarProduto_id(int(valor))] if valor else []
            elif tipo == "nome":
                produtos = executar_produto.PesquisarProduto_nome(valor) if valor else []
            elif tipo == "descricao":
                produtos = executar_produto.PesquisarProduto_descricao(valor) if valor else []
            elif tipo == "quantidade":
                produtos = executar_produto.PesquisarProduto_quantidade(int(valor)) if valor else []
            elif tipo == "preco":
                produtos = executar_produto.PesquisarProduto_preco(float(valor)) if valor else []
            
            lista_produtos.controls.clear()
            
            for produto in produtos:
                if produto: 
                    lista_produtos.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.ListTile(
                                        title=ft.Text(produto.nome, weight="bold"),
                                        subtitle=ft.Text(produto.descricao),
                                    ),
                                    ft.Divider(height=1),
                                    ft.Row([
                                        ft.Text(f"Estoque: {produto.quantidade}"),
                                        ft.Text(f"Preço: R${produto.preco:.2f}"),
                                        ft.Text(f"ID: {produto.id}", color=colors["text"], opacity=0.7)
                                    ], spacing=20),
                                    ft.Row([
                                        ft.IconButton(
                                            icon=ft.icons.EDIT,
                                            icon_color=colors["primary"],
                                            on_click=lambda e, p=produto: editar_produto(p)
                                        ),
                                        ft.IconButton(
                                            icon=ft.icons.DELETE,
                                            icon_color=colors["error"],
                                            on_click=lambda e, p=produto: confirmar_exclusao_produto(p)
                                        )
                                    ], alignment="end")
                                ]),
                                padding=10
                            ),
                            elevation=3,
                            margin=5
                        )
                    )
            
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar produtos: {str(e)}"))
            page.snack_bar.open = True
            page.update()

    btn_pesquisar_produto.on_click = carregar_produtos

    def salvar_produto(e):
        try:
            produto = Produto(
                idProduto=int(produto_id.value) if produto_id.value else None,
                nomeProduto=produto_nome.value,
                descricaoProduto=produto_desc.value,
                quantidadeProduto=int(produto_qtd.value),
                precoProduto=float(produto_preco.value)
            )
            
            if produto_id.value:
                executar_produto.ModificarProduto(produto)
                mensagem = "Produto atualizado com sucesso!"
            else:
                executar_produto.InserirProduto(produto)
                mensagem = "Produto cadastrado com sucesso!"
            
            page.snack_bar = ft.SnackBar(ft.Text(mensagem))
            page.snack_bar.open = True
            limpar_form_produto()
            carregar_produtos()
            carregar_produtos_dropdown()
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {str(e)}"))
            page.snack_bar.open = True
        page.update()

    def limpar_form_produto():
        produto_id.value = ""
        produto_nome.value = ""
        produto_desc.value = ""
        produto_qtd.value = ""
        produto_preco.value = ""
        page.update()

    def editar_produto(produto):
        produto_id.value = str(produto.id)
        produto_nome.value = produto.nome
        produto_desc.value = produto.descricao
        produto_qtd.value = str(produto.quantidade)
        produto_preco.value = str(produto.preco)
        page.update()

    def confirmar_exclusao_produto(produto):
        def excluir(e):
            try:
                executar_produto.ExcluirProduto(produto)
                page.dialog.open = False
                carregar_produtos()
                carregar_produtos_dropdown()
                page.snack_bar = ft.SnackBar(ft.Text("Produto excluído com sucesso!"))
                page.snack_bar.open = True
                page.update()
            except Exception as e:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao excluir: {str(e)}"))
                page.snack_bar.open = True
                page.update()
        
        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar exclusão"),
            content=ft.Text(f"Excluir produto {produto.nome} (ID: {produto.id})?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(page.dialog, "open", False)),
                ft.TextButton("Excluir", on_click=excluir)
            ]
        )
        page.dialog.open = True
        page.update()

    aba_produtos = ft.Column(
        controls=[
            ft.Row([
                build_header("Produtos", ft.icons.INVENTORY),
                btn_novo_produto
            ], alignment="spaceBetween"),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Cadastro de produtos", weight="bold"),
                        ft.Divider(),
                        produto_id,
                        produto_nome,
                        ft.Row([produto_qtd, produto_preco]),
                        produto_desc,
                        ft.Row([btn_salvar_produto], alignment="end")
                    ], spacing=10),
                    padding=15
                ),
                elevation=3,
                margin=5
            ),
            
            ft.Text("Pesquisar produtos", size=18, weight="bold"),
            ft.Divider(),
            ft.Row([
                pesquisa_produto_tipo,
                pesquisa_produto_valor,
                btn_pesquisar_produto
            ], spacing=10),
            
            ft.Text("Lista de produtos", size=18, weight="bold"),
            ft.Divider(),
            lista_produtos
        ],
        scroll="auto",
        expand=True
    )

    venda_id = ft.TextField(visible=False)
    dropdown_produtos = ft.Dropdown(
        label="Selecione o produto",
        options=[],
        border_color=colors["primary"],
        filled=True,
        bgcolor=colors["card"],
        width=400
    )
    venda_quantidade = ft.TextField(
        label="Quantidade",
        border_color=colors["primary"],
        filled=True,
        bgcolor=colors["card"],
        width=150,
        input_filter=ft.NumbersOnlyInputFilter()
    )
    venda_data = ft.TextField(
        label="Data",
        value=datetime.now().strftime("%d/%m/%Y %H:%M"),
        border_color=colors["primary"],
        filled=True,
        bgcolor=colors["card"],
        width=200
    )
    venda_total = ft.TextField(
        label="Total",
        prefix_text="R$ ",
        read_only=True,
        border_color=colors["primary"],
        filled=True,
        bgcolor=colors["card"],
        width=150
    )

    btn_salvar_venda = ft.ElevatedButton(
        "Registrar venda",
        icon=ft.icons.SAVE,
        color="white",
        bgcolor=colors["secondary"],
        height=45
    )
    
    btn_nova_venda = ft.ElevatedButton(
        "Nova venda",
        icon=ft.icons.ADD,
        color="white",
        bgcolor=colors["primary"],
        height=45
    )

    lista_vendas = ft.ListView(expand=True, spacing=10)

    pesquisa_venda_tipo = ft.Dropdown(
        label="Pesquisar por",
        options=[
            ft.dropdown.Option("todos", "Todas as vendas"),
            ft.dropdown.Option("id", "ID Venda"),
            ft.dropdown.Option("idproduto", "ID Produto"),
            ft.dropdown.Option("quantidade", "Quantidade"),
            ft.dropdown.Option("data", "Data")
        ],
        value="todos",
        width=200
    )
    
    pesquisa_venda_valor = ft.TextField(
        label="Valor da pesquisa",
        width=300,
        visible=False
    )
    
    btn_pesquisar_venda = ft.ElevatedButton(
        "Pesquisar",
        icon=ft.icons.SEARCH,
        height=45
    )

    def atualizar_pesquisa_venda(e):
        pesquisa_venda_valor.visible = pesquisa_venda_tipo.value != "todos"
        page.update()

    pesquisa_venda_tipo.on_change = atualizar_pesquisa_venda

    def carregar_produtos_dropdown():
        dropdown_produtos.options = []
        produtos = executar_produto.PesquisarProduto_todos()
        for produto in produtos:
            dropdown_produtos.options.append(
                ft.dropdown.Option(
                    key=str(produto.id),
                    text=f"{produto.nome} (Estoque: {produto.quantidade})",
                    disabled=produto.quantidade <= 0
                )
            )
        page.update()

    def calcular_total(e):
        try:
            produto_id = int(dropdown_produtos.value)
            quantidade = int(venda_quantidade.value)
            produto = executar_produto.PesquisarProduto_id(produto_id)
            if produto:
                venda_total.value = f"{produto.preco * quantidade:.2f}"
            else:
                venda_total.value = "0.00"
        except:
            venda_total.value = "0.00"
        page.update()

    def carregar_vendas(e=None):
        tipo = pesquisa_venda_tipo.value
        valor = pesquisa_venda_valor.value
        
        try:
            if tipo == "todos":
                vendas = executar_venda.PesquisarVenda_todos()
            elif tipo == "id":
                venda = executar_venda.PesquisarVenda_id(int(valor)) if valor else None
                vendas = [venda] if venda else []
            elif tipo == "idproduto":
                vendas = executar_venda.PesquisarVenda_idproduto(int(valor)) if valor else []
            elif tipo == "quantidade":
                vendas = executar_venda.PesquisarVenda_quantidade(int(valor)) if valor else []
            elif tipo == "data":
                vendas = executar_venda.PesquisarVenda_data(valor) if valor else []
            
            lista_vendas.controls.clear()
            
            for venda in vendas:
                if venda:
                    produto = executar_produto.PesquisarProduto_id(venda.idproduto)
                    produto_nome = produto.nome if produto else "Produto não encontrado"
                    preco_unitario = produto.preco if produto else 0
                    total = preco_unitario * venda.quantidade
                    
                    lista_vendas.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.ListTile(
                                        title=ft.Text(produto_nome, weight="bold"),
                                        subtitle=ft.Text(f"{venda.quantidade} x R${preco_unitario:.2f}"),
                                    ),
                                    ft.Divider(height=1),
                                    ft.Row([
                                        ft.Text(f"Total: R${total:.2f}", weight="bold"),
                                        ft.Text(f"Data: {venda.data}"),
                                        ft.Text(f"ID: {venda.id}", color=colors["text"], opacity=0.7)
                                    ], spacing=20),
                                    ft.Row([
                                        ft.IconButton(
                                            icon=ft.icons.EDIT,
                                            icon_color=colors["primary"],
                                            on_click=lambda e, v=venda: editar_venda(v)
                                        ),
                                        ft.IconButton(
                                            icon=ft.icons.DELETE,
                                            icon_color=colors["error"],
                                            on_click=lambda e, v=venda: confirmar_exclusao_venda(v)
                                        )
                                    ], alignment="end")
                                ]),
                                padding=10
                            ),
                            elevation=3,
                            margin=5
                        )
                    )
            
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar vendas: {str(e)}"))
            page.snack_bar.open = True
            page.update()

    btn_pesquisar_venda.on_click = carregar_vendas

    def registrar_venda(e):
        try:
            produto_id = int(dropdown_produtos.value)
            quantidade = int(venda_quantidade.value)
            data = venda_data.value
            
            venda = Venda(
                idVenda=int(venda_id.value) if venda_id.value else None,
                idProduto=produto_id,
                dataVenda=data,
                quantidadeVendida=quantidade
            )
            
            if venda_id.value:
                executar_venda.ModificarVenda(venda)
                mensagem = "Venda atualizada com sucesso!"
            else:
                executar_venda.InserirVenda(venda)
                mensagem = "Venda registrada com sucesso!"
            
            page.snack_bar = ft.SnackBar(ft.Text(mensagem))
            page.snack_bar.open = True
            nova_venda()
            carregar_vendas()
            carregar_produtos_dropdown()
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {str(e)}"))
            page.snack_bar.open = True
        page.update()

    def nova_venda(e=None):
        venda_id.value = ""
        dropdown_produtos.value = None
        venda_quantidade.value = ""
        venda_data.value = datetime.now().strftime("%d/%m/%Y %H:%M")
        venda_total.value = "0.00"
        page.update()

    def editar_venda(venda):
        venda_id.value = str(venda.id)
        dropdown_produtos.value = str(venda.idproduto)
        venda_quantidade.value = str(venda.quantidade)
        venda_data.value = venda.data
        
        produto = executar_produto.PesquisarProduto_id(venda.idproduto)
        if produto:
            venda_total.value = f"{produto.preco * venda.quantidade:.2f}"
        else:
            venda_total.value = "0.00"
        
        page.update()

    def confirmar_exclusao_venda(venda):
        def excluir(e):
            try:
                executar_venda.ExcluirVenda(venda)
                page.dialog.open = False
                carregar_vendas()
                page.snack_bar = ft.SnackBar(ft.Text("Venda excluída com sucesso!"))
                page.snack_bar.open = True
                page.update()
            except Exception as e:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao excluir: {str(e)}"))
                page.snack_bar.open = True
                page.update()
        
        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar exclusão"),
            content=ft.Text(f"Excluir venda ID: {venda.id}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(page.dialog, "open", False)),
                ft.TextButton("Excluir", on_click=excluir)
            ]
        )
        page.dialog.open = True
        page.update()

    aba_vendas = ft.Column(
        controls=[
            ft.Row([
                build_header("Vendas", ft.icons.POINT_OF_SALE),
                btn_nova_venda
            ], alignment="spaceBetween"),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Registro de venda", weight="bold"),
                        ft.Divider(),
                        venda_id,
                        dropdown_produtos,
                        ft.Row([venda_quantidade, venda_data, venda_total]),
                        ft.Row([btn_salvar_venda], alignment="end")
                    ], spacing=10),
                    padding=15
                ),
                elevation=3,
                margin=5
            ),
            
            ft.Text("Pesquisar vendas", size=18, weight="bold"),
            ft.Divider(),
            ft.Row([
                pesquisa_venda_tipo,
                pesquisa_venda_valor,
                btn_pesquisar_venda
            ], spacing=10),
            
            ft.Text("Histórico de vendas", size=18, weight="bold"),
            ft.Divider(),
            lista_vendas
        ],
        scroll="auto",
        expand=True
    )

    btn_salvar_produto.on_click = salvar_produto
    btn_novo_produto.on_click = limpar_form_produto
    btn_salvar_venda.on_click = registrar_venda
    btn_nova_venda.on_click = nova_venda
    dropdown_produtos.on_change = calcular_total
    venda_quantidade.on_change = calcular_total

    page.add(
        ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="Produtos", content=aba_produtos),
                ft.Tab(text="Vendas", content=aba_vendas),
            ],
            expand=True
        )
    )

    carregar_produtos()
    carregar_produtos_dropdown()
    carregar_vendas()

ft.app(target=main)