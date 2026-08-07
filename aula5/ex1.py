class Animal:
    def __init__(self, nome):
        self.nome = nome

    def comer(self):
        print(self.nome, "está comendo")


class Cachorro(Animal):
    def latir(self):
        print(self.nome, "está latindo")


cachorro = Cachorro("Rex")

cachorro.comer()
cachorro.latir()
