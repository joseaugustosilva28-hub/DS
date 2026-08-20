"""API REST - Biblioteca (Flask + SQLite).

Arquivo principal: cria a aplicacao, registra as rotas e sobe o servidor.

Uso:
    python app.py              # cria o banco (se nao existir) e roda a API
    python app.py --init-db    # recria o banco com os dados de exemplo
"""

import sys

from flask import Flask, jsonify

import config
import database as db
from routes import autores_bp, livros_bp


def create_app():
    """Cria e configura a aplicacao Flask."""
    app = Flask(__name__)
    app.json.ensure_ascii = False  # deixa acentos legiveis no JSON
    app.json.sort_keys = False

    # Fecha a conexao com o banco ao final de cada requisicao
    app.teardown_appcontext(db.close_connection)

    # Registra os grupos de rotas
    app.register_blueprint(autores_bp)
    app.register_blueprint(livros_bp)

    # --------------------------------------------------------------
    # Rota inicial: documentacao rapida da API
    # --------------------------------------------------------------
    @app.route("/", methods=["GET"])
    def inicio():
        return jsonify({
            "api": "Biblioteca",
            "tabelas": {"pai": "autores", "filho": "livros"},
            "rotas": {
                "autores": [
                    "GET    /autores                 (filtros: ?nome=&nacionalidade=)",
                    "GET    /autores/<id>",
                    "POST   /autores",
                    "PUT    /autores/<id>",
                    "DELETE /autores/<id>",
                    "GET    /autores/<id>/livros     (filtro por caminho)",
                    "GET    /autores/sem-livros      (LEFT JOIN)",
                ],
                "livros": [
                    "GET    /livros",
                    "GET    /livros/completos        (JOIN com o nome do autor)",
                    "GET    /livros/busca            (LIKE: ?nome=&autor=&ano_min=&ano_max=&preco_max=)",
                    "GET    /livros/<id>",
                    "POST   /livros",
                    "PUT    /livros/<id>",
                    "DELETE /livros/<id>",
                ],
            },
        }), 200

    # --------------------------------------------------------------
    # Tratadores de erro: sempre responder em JSON
    # --------------------------------------------------------------
    @app.errorhandler(400)
    def erro_400(e):
        return jsonify({"erro": "Requisicao invalida."}), 400

    @app.errorhandler(404)
    def erro_404(e):
        return jsonify({"erro": "Rota ou recurso nao encontrado."}), 404

    @app.errorhandler(405)
    def erro_405(e):
        return jsonify({"erro": "Metodo HTTP nao permitido para esta rota."}), 405

    @app.errorhandler(500)
    def erro_500(e):
        return jsonify({"erro": "Erro interno no servidor."}), 500

    return app


app = create_app()


if __name__ == "__main__":
    if "--init-db" in sys.argv:
        db.init_db(com_dados_exemplo=True)
        print(f"Banco recriado com dados de exemplo em: {config.DATABASE}")
    else:
        db.garantir_banco()
        print(f"Banco em uso: {config.DATABASE}")
        app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
