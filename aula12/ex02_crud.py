from flask import Flask, jsonify

app = Flask(__name__)

produtos = [
    {
        "id": 1,
        "nome": "Mouse",
        "preco": 50
    },
    {
        "id": 2,
        "nome": "Teclado",
        "preco": 100
    }
]


@app.route("/produtos", methods=["GET"])
def listar_produtos():
    return jsonify(produtos)


@app.route("/produtos/<int:id>", methods=["DELETE"])
def apagar_produto(id):

    for produto in produtos:
        if produto["id"] == id:
            produtos.remove(produto)

            return jsonify({
                "mensagem": "Produto apagado com sucesso"
            })

    return jsonify({
        "erro": "Produto nao encontrado"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)
