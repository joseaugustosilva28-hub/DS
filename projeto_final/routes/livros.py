"""Rotas da tabela FILHO: livros.

CRUD completo + rota com JOIN (livro com o NOME do autor)
+ busca por query string com LIKE e varios filtros combinados.
"""

from flask import Blueprint, jsonify, request

import database as db
import validacao as v

livros_bp = Blueprint("livros", __name__)

# SELECT reaproveitado: JOIN entre livros (filho) e autores (pai),
# trazendo o NOME do autor e nao apenas o autor_id.
SELECT_COM_JOIN = """
    SELECT l.id,
           l.titulo,
           l.ano,
           l.preco,
           l.autor_id,
           a.nome          AS autor,
           a.nacionalidade AS autor_nacionalidade
      FROM livros l
      INNER JOIN autores a ON a.id = l.autor_id
"""


def _autor_existe(autor_id):
    """Verifica se o autor informado existe (integridade antes do INSERT/UPDATE)."""
    return db.query_one("SELECT id FROM autores WHERE id = ?", (autor_id,)) is not None


# ------------------------------------------------------------------
# GET /livros -> lista simples de livros (dados da propria tabela filho)
# ------------------------------------------------------------------
@livros_bp.route("/livros", methods=["GET"])
def listar_livros():
    livros = db.query_all(
        "SELECT id, titulo, ano, preco, autor_id FROM livros ORDER BY titulo"
    )
    return jsonify(livros), 200


# ------------------------------------------------------------------
# GET /livros/completos -> ROTA COM JOIN
# Traz cada livro (filho) junto com o NOME do autor (pai).
# ------------------------------------------------------------------
@livros_bp.route("/livros/completos", methods=["GET"])
def listar_livros_com_autor():
    livros = db.query_all(SELECT_COM_JOIN + " ORDER BY a.nome, l.titulo")
    return jsonify(livros), 200


# ------------------------------------------------------------------
# GET /livros/busca -> BUSCA POR QUERY STRING COM LIKE
# Filtros (todos opcionais e combinaveis):
#   ?nome=casmurro&autor=machado&ano_min=1800&ano_max=1900&preco_max=50
# ------------------------------------------------------------------
@livros_bp.route("/livros/busca", methods=["GET"])
def buscar_livros():
    nome = request.args.get("nome", "").strip()
    autor = request.args.get("autor", "").strip()
    ano_min = request.args.get("ano_min", "").strip()
    ano_max = request.args.get("ano_max", "").strip()
    preco_max = request.args.get("preco_max", "").strip()

    sql = SELECT_COM_JOIN + " WHERE 1 = 1"
    parametros = []

    if nome:
        sql += " AND l.titulo LIKE ?"
        parametros.append(f"%{nome}%")
    if autor:
        sql += " AND a.nome LIKE ?"
        parametros.append(f"%{autor}%")

    if ano_min:
        try:
            parametros.append(int(ano_min))
        except ValueError:
            return jsonify({"erro": "O filtro 'ano_min' deve ser um numero inteiro."}), 400
        sql += " AND l.ano >= ?"

    if ano_max:
        try:
            parametros.append(int(ano_max))
        except ValueError:
            return jsonify({"erro": "O filtro 'ano_max' deve ser um numero inteiro."}), 400
        sql += " AND l.ano <= ?"

    if preco_max:
        try:
            parametros.append(float(preco_max))
        except ValueError:
            return jsonify({"erro": "O filtro 'preco_max' deve ser um numero."}), 400
        sql += " AND l.preco <= ?"

    sql += " ORDER BY l.titulo"

    resultados = db.query_all(sql, parametros)
    return jsonify({"total": len(resultados), "resultados": resultados}), 200


# ------------------------------------------------------------------
# GET /livros/<id> -> um livro especifico (tambem com JOIN)
# ------------------------------------------------------------------
@livros_bp.route("/livros/<int:livro_id>", methods=["GET"])
def obter_livro(livro_id):
    livro = db.query_one(SELECT_COM_JOIN + " WHERE l.id = ?", (livro_id,))
    if livro is None:
        return jsonify({"erro": "Livro nao encontrado."}), 404
    return jsonify(livro), 200


# ------------------------------------------------------------------
# POST /livros -> cria um livro (201 Created)
# Corpo: {"titulo": "...", "ano": 1899, "preco": 39.9, "autor_id": 1}
# ------------------------------------------------------------------
@livros_bp.route("/livros", methods=["POST"])
def criar_livro():
    dados, erro = v.pegar_json(request)
    if erro:
        return jsonify({"erro": erro}), 400

    titulo, erro = v.texto_obrigatorio(dados, "titulo")
    if erro:
        return jsonify({"erro": erro}), 400

    autor_id, erro = v.inteiro_obrigatorio(dados, "autor_id", minimo=1)
    if erro:
        return jsonify({"erro": erro}), 400

    ano, erro = v.inteiro_opcional(dados, "ano", minimo=0, maximo=2100)
    if erro:
        return jsonify({"erro": erro}), 400

    preco, erro = v.numero_opcional(dados, "preco", minimo=0, padrao=0.0)
    if erro:
        return jsonify({"erro": erro}), 400

    if not _autor_existe(autor_id):
        return jsonify({"erro": f"Nao existe autor com id {autor_id}."}), 400

    novo_id, _ = db.execute(
        "INSERT INTO livros (titulo, ano, preco, autor_id) VALUES (?, ?, ?, ?)",
        (titulo, ano, preco, autor_id),
    )

    livro = db.query_one(SELECT_COM_JOIN + " WHERE l.id = ?", (novo_id,))
    return jsonify(livro), 201


# ------------------------------------------------------------------
# PUT /livros/<id> -> atualiza um livro
# ------------------------------------------------------------------
@livros_bp.route("/livros/<int:livro_id>", methods=["PUT"])
def atualizar_livro(livro_id):
    atual = db.query_one(
        "SELECT id, titulo, ano, preco, autor_id FROM livros WHERE id = ?", (livro_id,)
    )
    if atual is None:
        return jsonify({"erro": "Livro nao encontrado."}), 404

    dados, erro = v.pegar_json(request)
    if erro:
        return jsonify({"erro": erro}), 400

    titulo, erro = v.texto_opcional(dados, "titulo", padrao=atual["titulo"])
    if erro:
        return jsonify({"erro": erro}), 400

    ano, erro = v.inteiro_opcional(dados, "ano", minimo=0, maximo=2100, padrao=atual["ano"])
    if erro:
        return jsonify({"erro": erro}), 400

    preco, erro = v.numero_opcional(dados, "preco", minimo=0, padrao=atual["preco"])
    if erro:
        return jsonify({"erro": erro}), 400

    autor_id, erro = v.inteiro_opcional(
        dados, "autor_id", minimo=1, padrao=atual["autor_id"]
    )
    if erro:
        return jsonify({"erro": erro}), 400

    if autor_id != atual["autor_id"] and not _autor_existe(autor_id):
        return jsonify({"erro": f"Nao existe autor com id {autor_id}."}), 400

    db.execute(
        """
        UPDATE livros
           SET titulo = ?, ano = ?, preco = ?, autor_id = ?
         WHERE id = ?
        """,
        (titulo, ano, preco, autor_id, livro_id),
    )

    livro = db.query_one(SELECT_COM_JOIN + " WHERE l.id = ?", (livro_id,))
    return jsonify(livro), 200


# ------------------------------------------------------------------
# DELETE /livros/<id> -> apaga um livro
# ------------------------------------------------------------------
@livros_bp.route("/livros/<int:livro_id>", methods=["DELETE"])
def apagar_livro(livro_id):
    livro = db.query_one("SELECT id, titulo FROM livros WHERE id = ?", (livro_id,))
    if livro is None:
        return jsonify({"erro": "Livro nao encontrado."}), 404

    db.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
    return jsonify({"mensagem": f"Livro '{livro['titulo']}' apagado com sucesso."}), 200
