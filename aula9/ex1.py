from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/produto")
def produto():
    dados = {
        "id": 1,
        "nome": "Mouse",
        "preco": 50,
        "disponivel": True
    }

    return jsonify(dados)

if __name__ == "__main__":
    app.run(debug=True)
