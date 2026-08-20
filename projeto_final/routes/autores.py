"""Rotas da tabela PAI: autores.

CRUD completo + filtro por caminho (/autores/<id>/livros)
+ LEFT JOIN (/autores/sem-livros).
"""

from flask import Blueprint, jsonify, request

import database as db
import validacao as v

autores_bp = Blueprint("autores", __name__)


# ------------------------------------------------------------------
# GET /autores  -> lista todos os autores
# Filtros opcionais por query string (podem ser combinados):
#   ?nome=machado&nacionalidade=brasil
# LEFT JOIN para trazer tambem quantos livros cada autor tem.
# ------------------------------------------------------------------
@autores_bp.route("/autores", methods=["GET"])
def listar_autores():
    nome = request.args.get("nome", "").strip()
    nacionalidade = request.args.get("nacionalidade", "").strip()

    sql = """
        SELECT a.id,
               a.nome,
               a.nacionalidade,
               a.ano_nascimento,
               COUNT(l.id) AS total_livros
          FROM autores a
          LEFT JOIN livros l ON l.autor_id = a.id
         WHERE 1 = 1
    """
    parametros = []

    if nome:
        sql += " AND a.nome LIKE ?"
        parametros.append(f"%{nome}%")
    if nacionalidade:
        sql += " AND a.nacionalidade LIKE ?"
        parametros.append(f"%{nacionalidade}%")

    sql += " GROUP BY a.id ORDER BY a.nome"

    return jsonify(db.query_all(sql, parametros)), 200


# ------------------------------------------------------------------
# GET /autores/sem-livros -> LEFT JOIN: autores que nao possuem livros
# (declarada antes de /autores/<int:id> por clareza)
# ------------------------------------------------------------------
@autores_bp.route("/autores/sem-livros", methods=["GET"])
def autores_sem_livros():
    sql = """
        SELECT a.id, a.nome, a.nacionalidade, a.ano_nascimento
          FROM autores a
          LEFT JOIN livros l ON l.autor_id = a.id
         WHERE l.id IS NULL
         ORDER BY a.nome
    """
    return jsonify(db.query_all(sql)), 200


# ------------------------------------------------------------------
# GET /autores/<id> -> um autor especifico
# ------------------------------------------------------------------
@autores_bp.route("/autores/<int:autor_id>", methods=["GET"])
def obter_autor(autor_id):
    autor = db.query_one(
        "SELECT id, nome, nacionalidade, ano_nascimento FROM autores WHERE id = ?",
        (autor_id,),
    )
    if autor is None:
        return jsonify({"erro": "Autor nao encontrado."}), 404
    return jsonify(autor), 200


# ------------------------------------------------------------------
# GET /autores/<id>/livros -> FILTRO POR CAMINHO
# Lista os "filhos" (livros) de um "pai" (autor).
# ------------------------------------------------------------------
@autores_bp.route("/autores/<int:autor_id>/livros", methods=["GET"])
def livros_do_autor(autor_id):
    autor = db.query_one("SELECT id, nome FROM autores WHERE id = ?", (autor_id,))
    if autor is None:
        return jsonify({"erro": "Autor nao encontrado."}), 404

    livros = db.query_all(
        """
        SELECT id, titulo, ano, preco, autor_id
          FROM livros
         WHERE autor_id = ?
         ORDER BY titulo
        """,
        (autor_id,),
    )
    return jsonify({
        "autor_id": autor["id"],
        "autor": autor["nome"],
        "total": len(livros),
        "livros": livros,
    }), 200


# ------------------------------------------------------------------
# POST /autores -> cria um autor (201 Created)
# ------------------------------------------------------------------
@autores_bp.route("/autores", methods=["POST"])
def criar_autor():
    dados, erro = v.pegar_json(request)
    if erro:
        return jsonify({"erro": erro}), 400

    nome, erro = v.texto_obrigatorio(dados, "nome")
    if erro:
        return jsonify({"erro": erro}), 400

    nacionalidade, erro = v.texto_opcional(dados, "nacionalidade", padrao="Desconhecida")
    if erro:
        return jsonify({"erro": erro}), 400

    ano_nascimento, erro = v.inteiro_opcional(dados, "ano_nascimento", minimo=0, maximo=2100)
    if erro:
        return jsonify({"erro": erro}), 400

    novo_id, _ = db.execute(
        "INSERT INTO autores (nome, nacionalidade, ano_nascimento) VALUES (?, ?, ?)",
        (nome, nacionalidade, ano_nascimento),
    )

    autor = db.query_one(
        "SELECT id, nome, nacionalidade, ano_nascimento FROM autores WHERE id = ?",
        (novo_id,),
    )
    return jsonify(autor), 201


# ------------------------------------------------------------------
# PUT /autores/<id> -> atualiza um autor
# ------------------------------------------------------------------
@autores_bp.route("/autores/<int:autor_id>", methods=["PUT"])
def atualizar_autor(autor_id):
    atual = db.query_one(
        "SELECT id, nome, nacionalidade, ano_nascimento FROM autores WHERE id = ?",
        (autor_id,),
    )
    if atual is None:
        return jsonify({"erro": "Autor nao encontrado."}), 404

    dados, erro = v.pegar_json(request)
    if erro:
        return jsonify({"erro": erro}), 400

    nome, erro = v.texto_opcional(dados, "nome", padrao=atual["nome"])
    if erro:
        return jsonify({"erro": erro}), 400

    nacionalidade, erro = v.texto_opcional(
        dados, "nacionalidade", padrao=atual["nacionalidade"]
    )
    if erro:
        return jsonify({"erro": erro}), 400

    ano_nascimento, erro = v.inteiro_opcional(
        dados, "ano_nascimento", minimo=0, maximo=2100, padrao=atual["ano_nascimento"]
    )
    if erro:
        return jsonify({"erro": erro}), 400

    db.execute(
        """
        UPDATE autores
           SET nome = ?, nacionalidade = ?, ano_nascimento = ?
         WHERE id = ?
        """,
        (nome, nacionalidade, ano_nascimento, autor_id),
    )

    autor = db.query_one(
        "SELECT id, nome, nacionalidade, ano_nascimento FROM autores WHERE id = ?",
        (autor_id,),
    )
    return jsonify(autor), 200


# ------------------------------------------------------------------
# DELETE /autores/<id> -> apaga o autor (e seus livros, via ON DELETE CASCADE)
# ------------------------------------------------------------------
@autores_bp.route("/autores/<int:autor_id>", methods=["DELETE"])
def apagar_autor(autor_id):
    autor = db.query_one("SELECT id, nome FROM autores WHERE id = ?", (autor_id,))
    if autor is None:
        return jsonify({"erro": "Autor nao encontrado."}), 404

    total = db.query_one(
        "SELECT COUNT(*) AS total FROM livros WHERE autor_id = ?", (autor_id,)
    )["total"]

    db.execute("DELETE FROM autores WHERE id = ?", (autor_id,))

    return jsonify({
        "mensagem": f"Autor '{autor['nome']}' apagado com sucesso.",
        "livros_apagados_em_cascata": total,
    }), 200
