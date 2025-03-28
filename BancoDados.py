import sqlite3

class Banco_Dados:
    def __init__(self, nomeBD):
        self.nomeBD = nomeBD
        self.conexaoBD = None
        self.cursorBD = None
        
    def conectar_BD(self):
        self.conexaoBD = sqlite3.connect(self.nomeBD)
        self.cursorBD = self.conexaoBD.cursor()

    def desconectar_BD(self):
        self.conexaoBD.close()
        self.conexaoBD = None
        self.cursorBD = None

    def criar_tabelas(self):
        self.conectar_BD()
        comando = '''
                create table if not exists produto (
                id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_produto varchar(60) not null,
                descricao varchar(100) not null,
                quantidade_disp int not null,
                preco real not null
                );

                create table if not exists venda (
                id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                id_produto int not null,
                quantidade_vendida int check(quantidade_vendida > 0),
                data_venda datetime not null,
                foreign key (id_produto) references produto(id_produto)
                );
                '''
        self.cursorBD.executescript(comando)
        self.desconectar_BD()

    def adicionar_produto(self,nome,descricao,quantidade,preco):
        self.conectar_BD()
        comando = '''
                insert into produto (nome_produto,descricao,quantidade_disp,preco)
                values(?,?,?,?)
                '''
        self.cursorBD.execute(comando,(nome,descricao,quantidade,preco))
        self.conexaoBD.commit()
        self.desconectar_BD()
    
    def atualizar_produto(self,id,nome,descricao,quantidade,preco):
        self.conectar_BD()
        comando = '''
                update produto
                set nome_produto = ?, descricao = ?, quantidade_disp = ?, preco = ?
                where id_produto = ?
                '''
        self.cursorBD.execute(comando,(nome,descricao,quantidade,preco,id))
        self.conexaoBD.commit()
        self.desconectar_BD()

    def remover_produto(self,id):
        self.conectar_BD()
        comando = '''
                delete from produto
                where id_produto = ?
                '''
        self.cursorBD.execute(comando,(id,))
        self.conexaoBD.commit()
        self.desconectar_BD()

    def consultar_produto(self,criterio="todos", valor=None):
        self.conectar_BD()
        comando = '''select id_produto,nome_produto,descricao,quantidade_disp,preco from produto'''
        if criterio == "id":
            comando += ''' where id_produto = ?'''
        elif criterio == "nome":
            comando += ''' where nome_produto = ?'''
        elif criterio == "descricao":
            comando += ''' where descricao = ?'''
        elif criterio == "quantidade disponivel":
            comando += ''' where quantidade_disp = ?'''
        elif criterio == "preco":
            comando += ''' where preco = ?'''

        if criterio == "todos":
            self.cursorBD.execute(comando)
        else:
            self.cursorBD.execute(comando,(valor,))   

        dados = self.cursorBD.fetchall()
        self.desconectar_BD()
        return dados

    def adicionar_venda(self,idproduto,quantidade,data):
        self.conectar_BD()
        comando = '''
                insert into venda (id_produto,quantidade_vendida,data_venda)
                values(?,?,?)
                '''
        self.cursorBD.execute(comando,(idproduto,quantidade,data))
        self.conexaoBD.commit()
        self.desconectar_BD()
    
    def atualizar_venda(self,id,idproduto,quantidade,data):
        self.conectar_BD()
        comando = '''
                update venda
                set id_produto = ?, quantidade_vendida = ?, data_venda = ?
                where id_venda = ?
                '''
        self.cursorBD.execute(comando,(idproduto,quantidade,data,id))
        self.conexaoBD.commit()
        self.desconectar_BD()

    def remover_venda(self,id):
        self.conectar_BD()
        comando = '''
                delete from venda
                where id_venda = ?
                '''
        self.cursorBD.execute(comando,(id,))
        self.conexaoBD.commit()
        self.desconectar_BD()

    def consultar_venda(self,criterio="todos", valor=None):
        self.conectar_BD()
        comando = '''select id_venda,id_produto,quantidade_vendida,data_venda from venda'''
        if criterio == "id venda":
            comando += ''' where id_venda = ?'''
        elif criterio == "id produto":
            comando += ''' where id_produto = ?'''
        elif criterio == "quantidade vendida":
            comando += ''' where quantidade_vendida = ?'''
        elif criterio == "data":
            comando += ''' where data_venda = ?'''

        if criterio == "todos":
            self.cursorBD.execute(comando)
        else:
            self.cursorBD.execute(comando,(valor,))   

        dados = self.cursorBD.fetchall()
        self.desconectar_BD()
        return dados