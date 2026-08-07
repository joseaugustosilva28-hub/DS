from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


def conectar():
    conexao = sqlite3.connect("loja.db")
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela():
    conexao = conectar()

    conexao.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        preco REAL
    )
    """)

    conexao.commit()
    conexao.close()


@app.route("/produtos", methods=["GET"])
def listar_produtos():

    conexao = conectar()

    produtos = conexao.execute(
        "SELECT * FROM produtos"
    ).fetchall()

    lista = [dict(produto) for produto in produtos]

    conexao.close()

    return jsonify(lista)



@app.route("/produtos", methods=["POST"])
def criar_produto():

    novo = request.get_json()


    if "preco" not in novo:
        return jsonify(
            {"erro": "O campo preco e obrigatorio"}
        ), 400


    conexao = conectar()

    cursor = conexao.execute(
        "INSERT INTO produtos (nome, preco) VALUES (?, ?)",
        (
            novo["nome"],
            novo["preco"]
        )
    )


    conexao.commit()

    id_produto = cursor.lastrowid

    conexao.close()


    return jsonify({
        "id": id_produto,
        **novo
    }), 201



if __name__ == "__main__":
    criar_tabela()
    app.run(debug=True)
