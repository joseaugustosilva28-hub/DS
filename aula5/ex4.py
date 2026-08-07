class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade


class Aluno(Pessoa):
    def __init__(self, nome, idade, matricula):
        super().__init__(nome, idade)
        self.matricula = matricula

    def apresentar(self):
        print("Aluno:", self.nome)
        print("Idade:", self.idade)
        print("Matrícula:", self.matricula)


class Professor(Pessoa):
    def __init__(self, nome, idade, salario):
        super().__init__(nome, idade)
        self.salario = salario

    def apresentar(self):
        print("Professor:", self.nome)
        print("Idade:", self.idade)
        print("Salário:", self.salario)


lista = [
    Aluno("Ana", 17, "1234"),
    Professor("João", 40, 4500)
]

for pessoa in lista:
    pessoa.apresentar()
    print()
