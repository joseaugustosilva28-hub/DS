from flask import Flask, jsonify

app = Flask(__name__)

produtos = [
    {
        "id": 1,
        "nome": "Teclado",
        "preco": 100,
        "disponivel": True
    },
    {
        "id": 2,
        "nome": "Mouse",
        "preco": 50,
        "disponivel": True
    },
    {
        "id": 3,
        "nome": "Monitor",
        "preco": 800,
        "disponivel": False
    },
    {
        "id": 4,
        "nome": "Fone",
        "preco": 120,
        "disponivel": True
    }
]


@app.route("/produtos/disponiveis")
def produtos_disponiveis():

    lista = []

    for produto in produtos:
        if produto["disponivel"] == True:
            lista.append(produto)

    return jsonify(lista)


if __name__ == "__main__":
    app.run(debug=True)
