class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    def desconto(self, porcentagem):
        novo_preco = self.preco - (self.preco * porcentagem / 100)
        return novo_preco


produto = Produto("Camiseta", 100)

print("Preço:", produto.preco)
print("Com desconto:", produto.desconto(10))
