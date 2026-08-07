from flask import Flask, jsonify, request

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


@app.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):

    dados = request.get_json()

    for produto in produtos:
        if produto["id"] == id:
            produto["nome"] = dados["nome"]
            produto["preco"] = dados["preco"]

            return jsonify(produto)

    return jsonify({"erro": "Produto nao encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)
