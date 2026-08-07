class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco


produto1 = Produto("Arroz", 25)
produto2 = Produto("Feijão", 10)

print(produto1.nome, produto1.preco)
print(produto2.nome, produto2.preco)
