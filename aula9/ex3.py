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

@app.route("/produtos/<int:id>")
def buscar_produto(id):

    for produto in produtos:
        if produto["id"] == id:
            return jsonify(produto)

    return jsonify({"erro": "Produto nao encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)
