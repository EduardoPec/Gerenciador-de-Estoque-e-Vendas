from BancoDados import Banco_Dados

class Produto:
    def __init__(self,idProduto,nomeProduto,descricaoProduto,quantidadeProduto = 0,precoProduto = 0):
        if quantidadeProduto < 0:
            raise ValueError("Quantidade não pode ser negativa!")
        if precoProduto < 0:
            raise ValueError("Preço não pode ser negativo!")
        
        self.id = idProduto
        self.nome = nomeProduto
        self.descricao = descricaoProduto
        self.quantidade = quantidadeProduto
        self.preco = precoProduto

class Venda:
    def __init__(self,idVenda,idProduto,dataVenda,quantidadeVendida = 0):
        self.id = idVenda
        self.idproduto = idProduto
        self.data = dataVenda
        self.quantidade = quantidadeVendida

class ExecutarProduto:
    def __init__(self):
        self.bd = Banco_Dados("DadosProdutos.sqlite")
        self.bd.criar_tabelas()

    def InserirProduto(self, produtoNovo):
        self.bd.adicionar_produto(produtoNovo.nome,produtoNovo.descricao,produtoNovo.quantidade,produtoNovo.preco)

    def ExcluirProduto(self, produtoEliminado):
        self.bd.remover_produto(produtoEliminado.id)

    def PesquisarProduto_id(self, idPesquisaProduto):
        resposta = False
        dados = self.bd.consultar_produto("id",idPesquisaProduto)
        if len(dados) > 0:
            id,nome,descricao,quantidade,preco = dados[0]
            resposta = Produto(id,nome,descricao,quantidade,preco)
        return resposta
    
    def PesquisarProduto_nome(self, nomePesquisaProduto):
        resposta = []
        dados = self.bd.consultar_produto("nome", nomePesquisaProduto)
        for prod in dados:
            id,nome,descricao,quantidade,preco = prod
            produto = Produto(id,nome,descricao,quantidade,preco)
            resposta.append(produto)
        return resposta
    
    def PesquisarProduto_descricao(self, descricaoPesquisaProduto):
        resposta = []
        dados = self.bd.consultar_produto("descricao", descricaoPesquisaProduto)
        for prod in dados:
            id,nome,descricao,quantidade,preco = prod
            produto = Produto(id,nome,descricao,quantidade,preco)
            resposta.append(produto)
        return resposta
    
    def PesquisarProduto_quantidade(self, quantidadePesquisaProduto):
        resposta = []
        dados = self.bd.consultar_produto("quantidade disponivel", quantidadePesquisaProduto)
        for prod in dados:
            id,nome,descricao,quantidade,preco = prod
            produto = Produto(id,nome,descricao,quantidade,preco)
            resposta.append(produto)
        return resposta
    
    def PesquisarProduto_preco(self, precoPesquisaProduto):
        resposta = []
        dados = self.bd.consultar_produto("preco", precoPesquisaProduto)
        for prod in dados:
            id,nome,descricao,quantidade,preco = prod
            produto = Produto(id,nome,descricao,quantidade,preco)
            resposta.append(produto)
        return resposta
    
    def PesquisarProduto_todos(self):
        resposta = []
        dados = self.bd.consultar_produto("todos")
        for prod in dados:
            id,nome,descricao,quantidade,preco = prod
            produto = Produto(id,nome,descricao,quantidade,preco)
            resposta.append(produto)
        return resposta
    
    def ModificarProduto(self, produtoModificado):
        self.bd.atualizar_produto(produtoModificado.id,produtoModificado.nome,produtoModificado.descricao,produtoModificado.quantidade,produtoModificado.preco)

class ExecutarVenda:
    def __init__(self):
        self.bd = Banco_Dados("DadosProdutos.sqlite")
        self.bd.criar_tabelas()

    def InserirVenda(self, vendaNova):
        produto = ExecutarProduto().PesquisarProduto_id(vendaNova.idproduto)
        if not produto:
            raise ValueError("Produto não encontrado!")
        if produto.quantidade < vendaNova.quantidade:
            raise ValueError("Quantidade em estoque insuficiente!")
        
        self.bd.adicionar_venda(vendaNova.idproduto,vendaNova.quantidade,vendaNova.data)

        produto.quantidade -= vendaNova.quantidade
        ExecutarProduto().ModificarProduto(produto)

    def ExcluirVenda(self, vendaEliminada):
        self.bd.remover_venda(vendaEliminada.id)

    def PesquisarVenda_id(self, idPesquisaVenda):
        resposta = False
        dados = self.bd.consultar_venda("id venda",idPesquisaVenda)
        if len(dados) > 0:
            id,idproduto,quantidade,data = dados[0]
            resposta = Venda(id,idproduto,data,quantidade)
        return resposta
    
    def PesquisarVenda_idproduto(self, idprodutoPesquisaVenda):
        resposta = []
        dados = self.bd.consultar_venda("id produto", idprodutoPesquisaVenda)
        for vend in dados:
            id,idproduto,quantidade,data = vend
            venda = Venda(id,idproduto,data,quantidade)
            resposta.append(venda)
        return resposta
    
    def PesquisarVenda_quantidade(self, quantidadePesquisaVenda):
        resposta = []
        dados = self.bd.consultar_venda("quantidade vendida", quantidadePesquisaVenda)
        for vend in dados:
            id,idproduto,quantidade,data = vend
            venda = Venda(id,idproduto,data,quantidade)
            resposta.append(venda)
        return resposta
    
    def PesquisarVenda_data(self, dataPesquisaVenda):
        resposta = []
        dados = self.bd.consultar_venda("data", dataPesquisaVenda)
        for vend in dados:
            id,idproduto,quantidade,data = vend
            venda = Venda(id,idproduto,data,quantidade)
            resposta.append(venda)
        return resposta
    
    def PesquisarVenda_todos(self):
        resposta = []
        dados = self.bd.consultar_venda("todos")
        for vend in dados:
            id,idproduto,quantidade,data = vend
            venda = Venda(id,idproduto,data,quantidade)
            resposta.append(venda)
        return resposta
    
    def ModificarVenda(self, vendaModificada):
        self.bd.atualizar_venda(vendaModificada.id,vendaModificada.idproduto,vendaModificada.quantidade,vendaModificada.data)