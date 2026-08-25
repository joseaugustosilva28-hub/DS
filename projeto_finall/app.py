from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "banco.db"


def conectar_banco():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def criar_banco():
    conn = conectar_banco()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            categoria_id INTEGER NOT NULL,
            FOREIGN KEY (categoria_id)
            REFERENCES categorias(id)
            ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


@app.route("/categorias", methods=["GET"])
def listar_categorias():
    conn = conectar_banco()

    categorias = conn.execute(
        "SELECT * FROM categorias"
    ).fetchall()

    conn.close()

    return jsonify([dict(c) for c in categorias])


@app.route("/categorias/<int:id>", methods=["GET"])
def buscar_categoria(id):
    conn = conectar_banco()

    categoria = conn.execute(
        "SELECT * FROM categorias WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if categoria is None:
        return jsonify({"erro": "Categoria não encontrada"}), 404

    return jsonify(dict(categoria))


@app.route("/categorias", methods=["POST"])
def criar_categoria():
    dados = request.get_json()

    if not dados or "nome" not in dados:
        return jsonify({"erro": "O campo nome é obrigatório"}), 400

    if not isinstance(dados["nome"], str) or dados["nome"].strip() == "":
        return jsonify({"erro": "Nome inválido"}), 400

    conn = conectar_banco()

    cursor = conn.execute(
        "INSERT INTO categorias (nome) VALUES (?)",
        (dados["nome"],)
    )

    conn.commit()

    categoria_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "id": categoria_id,
        "nome": dados["nome"]
    }), 201


@app.route("/categorias/<int:id>", methods=["PUT"])
def atualizar_categoria(id):
    dados = request.get_json()

    if not dados or "nome" not in dados:
        return jsonify({"erro": "O campo nome é obrigatório"}), 400

    if not isinstance(dados["nome"], str) or dados["nome"].strip() == "":
        return jsonify({"erro": "Nome inválido"}), 400

    conn = conectar_banco()

    categoria = conn.execute(
        "SELECT * FROM categorias WHERE id = ?",
        (id,)
    ).fetchone()

    if categoria is None:
        conn.close()
        return jsonify({"erro": "Categoria não encontrada"}), 404

    conn.execute(
        "UPDATE categorias SET nome = ? WHERE id = ?",
        (dados["nome"], id)
    )

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Categoria atualizada com sucesso"})


@app.route("/categorias/<int:id>", methods=["DELETE"])
def excluir_categoria(id):
    conn = conectar_banco()

    categoria = conn.execute(
        "SELECT * FROM categorias WHERE id = ?",
        (id,)
    ).fetchone()

    if categoria is None:
        conn.close()
        return jsonify({"erro": "Categoria não encontrada"}), 404

    conn.execute(
        "DELETE FROM categorias WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Categoria excluída com sucesso"})


@app.route("/produtos", methods=["GET"])
def listar_produtos():
    conn = conectar_banco()

    produtos = conn.execute(
        "SELECT * FROM produtos"
    ).fetchall()

    conn.close()

    return jsonify([dict(p) for p in produtos])


@app.route("/produtos/<int:id>", methods=["GET"])
def buscar_produto(id):
    conn = conectar_banco()

    produto = conn.execute(
        "SELECT * FROM produtos WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404

    return jsonify(dict(produto))


@app.route("/produtos", methods=["POST"])
def criar_produto():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Dados não enviados"}), 400

    if "nome" not in dados or "preco" not in dados or "categoria_id" not in dados:
        return jsonify({
            "erro": "nome, preco e categoria_id são obrigatórios"
        }), 400

    if not isinstance(dados["nome"], str) or dados["nome"].strip() == "":
        return jsonify({"erro": "Nome inválido"}), 400

    try:
        preco = float(dados["preco"])
        categoria_id = int(dados["categoria_id"])
    except (ValueError, TypeError):
        return jsonify({"erro": "Preço ou categoria_id inválido"}), 400

    if preco < 0:
        return jsonify({"erro": "O preço não pode ser negativo"}), 400

    conn = conectar_banco()

    categoria = conn.execute(
        "SELECT * FROM categorias WHERE id = ?",
        (categoria_id,)
    ).fetchone()

    if categoria is None:
        conn.close()
        return jsonify({"erro": "Categoria não encontrada"}), 404

    cursor = conn.execute(
        """
        INSERT INTO produtos (nome, preco, categoria_id)
        VALUES (?, ?, ?)
        """,
        (dados["nome"], preco, categoria_id)
    )

    conn.commit()

    produto_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "id": produto_id,
        "nome": dados["nome"],
        "preco": preco,
        "categoria_id": categoria_id
    }), 201


@app.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Dados não enviados"}), 400

    if "nome" not in dados or "preco" not in dados or "categoria_id" not in dados:
        return jsonify({
            "erro": "nome, preco e categoria_id são obrigatórios"
        }), 400

    if not isinstance(dados["nome"], str) or dados["nome"].strip() == "":
        return jsonify({"erro": "Nome inválido"}), 400

    try:
        preco = float(dados["preco"])
        categoria_id = int(dados["categoria_id"])
    except (ValueError, TypeError):
        return jsonify({"erro": "Preço ou categoria_id inválido"}), 400

    if preco < 0:
        return jsonify({"erro": "O preço não pode ser negativo"}), 400

    conn = conectar_banco()

    produto = conn.execute(
        "SELECT * FROM produtos WHERE id = ?",
        (id,)
    ).fetchone()

    if produto is None:
        conn.close()
        return jsonify({"erro": "Produto não encontrado"}), 404

    categoria = conn.execute(
        "SELECT * FROM categorias WHERE id = ?",
        (categoria_id,)
    ).fetchone()

    if categoria is None:
        conn.close()
        return jsonify({"erro": "Categoria não encontrada"}), 404

    conn.execute(
        """
        UPDATE produtos
        SET nome = ?, preco = ?, categoria_id = ?
        WHERE id = ?
        """,
        (dados["nome"], preco, categoria_id, id)
    )

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Produto atualizado com sucesso"})


@app.route("/produtos/<int:id>", methods=["DELETE"])
def excluir_produto(id):
    conn = conectar_banco()

    produto = conn.execute(
        "SELECT * FROM produtos WHERE id = ?",
        (id,)
    ).fetchone()

    if produto is None:
        conn.close()
        return jsonify({"erro": "Produto não encontrado"}), 404

    conn.execute(
        "DELETE FROM produtos WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Produto excluído com sucesso"})


@app.route("/produtos/detalhes", methods=["GET"])
def produtos_detalhes():
    conn = conectar_banco()

    produtos = conn.execute(
        """
        SELECT
            produtos.id,
            produtos.nome,
            produtos.preco,
            produtos.categoria_id,
            categorias.nome AS categoria
        FROM produtos
        JOIN categorias
        ON produtos.categoria_id = categorias.id
        """
    ).fetchall()

    conn.close()

    return jsonify([dict(p) for p in produtos])


@app.route("/categorias/<int:id>/produtos", methods=["GET"])
def produtos_da_categoria(id):
    conn = conectar_banco()

    categoria = conn.execute(
        "SELECT * FROM categorias WHERE id = ?",
        (id,)
    ).fetchone()

    if categoria is None:
        conn.close()
        return jsonify({"erro": "Categoria não encontrada"}), 404

    produtos = conn.execute(
        "SELECT * FROM produtos WHERE categoria_id = ?",
        (id,)
    ).fetchall()

    conn.close()

    return jsonify([dict(p) for p in produtos])


@app.route("/produtos/busca", methods=["GET"])
def buscar_produtos():
    nome = request.args.get("nome")

    if not nome or nome.strip() == "":
        return jsonify({"erro": "Informe o nome para realizar a busca"}), 400

    conn = conectar_banco()

    produtos = conn.execute(
        "SELECT * FROM produtos WHERE nome LIKE ?",
        (f"%{nome}%",)
    ).fetchall()

    conn.close()

    return jsonify([dict(p) for p in produtos])


if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)
