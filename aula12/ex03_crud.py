from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


def conectar():
    conexao = sqlite3.connect("tarefas.db")
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela():

    conexao = conectar()

    conexao.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        feita INTEGER
    )
    """)

    conexao.commit()
    conexao.close()


# GET
@app.route("/tarefas", methods=["GET"])
def listar():

    conexao = conectar()

    tarefas = conexao.execute(
        "SELECT * FROM tarefas"
    ).fetchall()

    lista = [dict(tarefa) for tarefa in tarefas]

    conexao.close()

    return jsonify(lista)


# POST
@app.route("/tarefas", methods=["POST"])
def criar():

    nova = request.get_json()

    conexao = conectar()

    cursor = conexao.execute(
        "INSERT INTO tarefas (titulo, feita) VALUES (?, ?)",
        (
            nova["titulo"],
            nova["feita"]
        )
    )

    conexao.commit()

    id_tarefa = cursor.lastrowid

    conexao.close()

    return jsonify({
        "id": id_tarefa,
        **nova
    }), 201


# PUT
@app.route("/tarefas/<int:id>", methods=["PUT"])
def atualizar(id):

    dados = request.get_json()

    conexao = conectar()

    cursor = conexao.execute(
        "UPDATE tarefas SET titulo = ?, feita = ? WHERE id = ?",
        (
            dados["titulo"],
            dados["feita"],
            id
        )
    )

    conexao.commit()

    if cursor.rowcount == 0:
        return jsonify({
            "erro": "Tarefa nao encontrada"
        }), 404

    conexao.close()

    return jsonify({
        "id": id,
        **dados
    })


# DELETE
@app.route("/tarefas/<int:id>", methods=["DELETE"])
def apagar(id):

    conexao = conectar()

    cursor = conexao.execute(
        "DELETE FROM tarefas WHERE id = ?",
        (id,)
    )

    conexao.commit()

    if cursor.rowcount == 0:
        return jsonify({
            "erro": "Tarefa nao encontrada"
        }), 404

    conexao.close()

    return jsonify({
        "mensagem": "Tarefa apagada com sucesso"
    })


if __name__ == "__main__":
    criar_tabela()
    app.run(debug=True)
