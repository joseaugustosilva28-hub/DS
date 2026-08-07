class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    def desconto(self, porcentagem):
        novo_preco = self.preco - (self.preco * porcentagem / 100)
        return novo_preco


p = Produto("Tênis", 200)

print("Preço original:", p.preco)
print("Com desconto:", p.desconto(10))
