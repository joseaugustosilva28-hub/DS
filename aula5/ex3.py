class Funcionario:
    def __init__(self, nome, salario):
        self.nome = nome
        self.salario = salario

    def exibir(self):
        print("Nome:", self.nome)
        print("Salário:", self.salario)


class Gerente(Funcionario):
    def __init__(self, nome, salario, bonus):
        super().__init__(nome, salario)
        self.bonus = bonus

    def salario_total(self):
        return self.salario + self.bonus


gerente = Gerente("Carlos", 5000, 1500)

gerente.exibir()
print("Salário total:", gerente.salario_total())
