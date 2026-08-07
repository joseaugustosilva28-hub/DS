from flask import Flask, jsonify
import sqlite3


app = Flask(__name__)


def conectar():

    conexao = sqlite3.connect("biblioteca.db")
    conexao.row_factory = sqlite3.Row

    return conexao



@app.route("/livros-completo", methods=["GET"])
def livros_completo():

    conexao = conectar()


    livros = conexao.execute("""
    SELECT 
        livros.id,
        livros.titulo,
        autores.nome AS autor
    FROM livros
    JOIN autores 
    ON livros.autor_id = autores.id
    """).fetchall()


    resultado = [dict(livro) for livro in livros]


    conexao.close()


    return jsonify(resultado)



if __name__ == "__main__":
    app.run(debug=True)
