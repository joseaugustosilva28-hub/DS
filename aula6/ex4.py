class Pagamento:
    def processar(self, valor):
        return valor


class Dinheiro(Pagamento):
    def processar(self, valor):
        return valor - (valor * 5 / 100)


class Cartao(Pagamento):
    def processar(self, valor):
        return valor + (valor * 2 / 100)


class Pix(Pagamento):
    def processar(self, valor):
        return valor


pagamentos = [
    Dinheiro(),
    Cartao(),
    Pix()
]

valor = 100

for pagamento in pagamentos:
    print("Valor final:", pagamento.processar(valor))
