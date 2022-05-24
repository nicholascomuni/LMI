import pandas as pd
from math import ceil

class Lista_materiais:
    def __init__(self,nome=""):
        self.lista = {}
        self.nome = nome


    def add_item(self,*args):
        item = Item(*args)
        self.add(item)


    def add(self,item):
        if item.nome in self.lista.keys():
            atual = self.lista[item.nome]
            self.lista[item.nome] = atual + item
        else:
            self.lista[item.nome] = item


    def add_list(self,lista):
        for item in lista:
            self.add(item)

    def dtf(self):
        dtf = pd.DataFrame(columns=["Produto","Quantidade","Codigo","Valor"])
        dtf.Codigo = dtf.Codigo.astype(int)
        for item in self.lista.keys():
            it = self.lista[item]
            row = pd.Series({"Produto":it.nome,"Quantidade":it.quantidade,"Codigo":it.codigo,"Valor":it.valor})
            dtf = dtf.append(row,ignore_index=True)
        return dtf

    def __str__(self):
        represent = ""
        for item in self.lista.keys():
            represent  = represent + str(self.lista[item])+"\n"
        return represent

    def __add__(self,other):

        if type(other) == Lista_materiais:
            lista = Lista_materiais()
            lista.add_list(other)

            for key in self.lista.keys():
                item = self.lista[key]
                lista.add(item)

            return lista

        elif type(other) == Item:
            nova = Lista_materiais()
            nova.add_list(self)
            nova.add(other)
            return nova

    def __mul__(self,other):
        if type(other) == int:
            lista = Lista_materiais()
            for key in self.lista.keys():
                item = self.lista[key]
                lista.add(item*other)
            return lista

    def __len__(self):
        return len(self.lista)

    def __getitem__(self, position):
        keys = list(self.lista.keys())
        return self.lista[keys[position]]

    def __repr__(self):
        represent = "Lista: \n"
        for item in self.lista.keys():
            represent  = represent + " - " + str(self.lista[item].nome) +" - "+ str(self.lista[item].quantidade) +" - "+ str(self.lista[item].codigo) +" - R$ "+ str(self.lista[item].valor) + "\n"
        return represent


    def get_item(self,qtd=1,nome=""):

        name = ""
        if nome == "":
            name = self.nome
        else:
            name = nome

        return Item(name, qtd, 0, itens=self*qtd)



    def open_list(self, black_list = []):

        lista_itens = Lista_materiais()
        def search_item(lista):
            for key in lista.lista.keys():
                item = lista.lista[key]

                if len(item.composition) > 0 and item.nome not in black_list:
                    search_item(item.composition)
                else:
                    lista_itens.add(item)


        search_item(self)
        return lista_itens

    def valor_total(self):
        return self.dtf().Valor.sum()



class Item:
    def __init__(self,nome,quantidade,codigo=None,valor = 0,itens = Lista_materiais()):
        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor
        self.codigo = codigo
        self.composition = itens

        if len(self.composition) > 0:
            self.valor = (sum(self.composition.dtf()["Valor"]))


    def __add__(self,other):
        if self.nome == other.nome:
            if len(self.composition.lista):
                return Item(self.nome,self.quantidade+other.quantidade,self.codigo,round(self.valor + other.valor,2),self.composition + other.composition)
            else:
                return Item(self.nome,self.quantidade+other.quantidade,self.codigo,round(self.valor + other.valor,2))
        else:

            lista_soma = Lista_materiais()
            lista_soma.add(self)
            lista_soma.add(other)
            return lista_soma

    def __mul__(self,other):
        if type(other) == int:
            if len(self.composition.lista):
                return Item(self.nome,self.quantidade*other,self.codigo,round(self.valor*other),self.composition*other)
            else:
                return Item(self.nome,self.quantidade*other,self.codigo,round(self.valor*other))


    def __eq__(self,other):
        return self.nome in other

    def __str__(self):
        return f"{self.nome} - {self.quantidade}"

    def __repr__(self):
        return f"Item: {self.nome} - {self.quantidade} - {self.codigo} - R$ {self.valor}"
