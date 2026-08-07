class Funcionario:
    def calcular_salario(self):
        return 0


class Vendedor(Funcionario):
    def __init__(self, salario, comissao):
        self.salario = salario
        self.comissao = comissao

    def calcular_salario(self):
        return self.salario + self.comissao


class Gerente(Funcionario):
    def __init__(self, salario, bonus):
        self.salario = salario
        self.bonus = bonus

    def calcular_salario(self):
        return self.salario + self.bonus


vendedor = Vendedor(2000, 500)
gerente = Gerente(4000, 1000)

print("Salário vendedor:", vendedor.calcular_salario())
print("Salário gerente:", gerente.calcular_salario())
