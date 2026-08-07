class Forma:
    def area(self):
        return 0


class Triangulo(Forma):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        return (self.base * self.altura) / 2


class Quadrado(Forma):
    def __init__(self, lado):
        self.lado = lado

    def area(self):
        return self.lado * self.lado


formas = [
    Triangulo(5, 4),
    Quadrado(6),
    Triangulo(3, 8)
]

for forma in formas:
    print("Área:", forma.area())
