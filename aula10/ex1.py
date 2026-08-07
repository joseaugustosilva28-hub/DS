from flask import Flask, jsonify, request

app = Flask(__name__)

produtos = [
    {
        "id": 1,
        "nome": "Mouse",
        "preco": 50
    }
]


@app.route("/produtos", methods=["GET"])
def listar_produtos():
    return jsonify(produtos)


@app.route("/produtos", methods=["POST"])
def criar_produto():

    novo = request.get_json()

    produtos.append(novo)

    return jsonify(novo), 201


if __name__ == "__main__":
    app.run(debug=True)

#json
{
  "id": 2,
  "nome": "Teclado",
  "preco": 100
}
