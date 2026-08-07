from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Bem-vindo"

@app.route("/curso")
def curso():
    return "Curso de Programacao"

@app.route("/escola")
def escola():
    return "Escola Estadual Exemplo"

if __name__ == "__main__":
    app.run(debug=True)
