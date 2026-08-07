class Instrumento:
    def tocar(self):
        print("Som de instrumento")


class Violao(Instrumento):
    def tocar(self):
        print("Violão: Plim plim")


class Bateria(Instrumento):
    def tocar(self):
        print("Bateria: Tum tum")


class Piano(Instrumento):
    def tocar(self):
        print("Piano: Plim")


instrumentos = [
    Violao(),
    Bateria(),
    Piano()
]

for instrumento in instrumentos:
    instrumento.tocar()
