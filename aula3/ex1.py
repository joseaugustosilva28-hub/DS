class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco


p1 = Produto("Arroz", 25.90)
p2 = Produto("Feijão", 9.50)

print(p1.nome, "-", p1.preco)
print(p2.nome, "-", p2.preco)
