class ContaBancaria:
    def __init__(self, titular, saldo):
        self.titular = titular
        self.saldo = saldo

    def depositar(self, valor):
        self.saldo += valor

    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
        else:
            print("Saldo insuficiente")

    def extrato(self):
        print("Titular:", self.titular)
        print("Saldo:", self.saldo)


conta = ContaBancaria("João", 500)

conta.depositar(200)
conta.sacar(100)
conta.sacar(700)

conta.extrato()
