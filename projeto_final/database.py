"""Camada de acesso ao banco de dados SQLite.

Aqui ficam a conexao, as funcoes auxiliares de consulta e a criacao
do banco a partir dos arquivos .sql (schema.sql e seed.sql).
"""

import os
import sqlite3

from flask import g

import config


def get_connection():
    """Retorna a conexao do SQLite da requisicao atual (cria se necessario).

    - row_factory = sqlite3.Row permite acessar as colunas pelo nome.
    - PRAGMA foreign_keys = ON ativa as FOREIGN KEYs (no SQLite vem desligado).
    """
    if "db" not in g:
        g.db = sqlite3.connect(config.DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_connection(exception=None):
    """Fecha a conexao no fim da requisicao (registrada em app.teardown_appcontext)."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query_all(sql, params=()):
    """Executa um SELECT e devolve uma lista de dicionarios."""
    cursor = get_connection().execute(sql, params)
    linhas = cursor.fetchall()
    cursor.close()
    return [dict(linha) for linha in linhas]


def query_one(sql, params=()):
    """Executa um SELECT e devolve um dicionario ou None."""
    cursor = get_connection().execute(sql, params)
    linha = cursor.fetchone()
    cursor.close()
    return dict(linha) if linha is not None else None


def execute(sql, params=()):
    """Executa INSERT/UPDATE/DELETE, faz commit e devolve (lastrowid, rowcount)."""
    conexao = get_connection()
    cursor = conexao.execute(sql, params)
    conexao.commit()
    resultado = (cursor.lastrowid, cursor.rowcount)
    cursor.close()
    return resultado


def _ler_arquivo_sql(caminho):
    """Le o conteudo de um arquivo .sql."""
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def init_db(com_dados_exemplo=True):
    """Cria (ou recria) o banco executando sql/schema.sql e sql/seed.sql.

    Usa uma conexao propria para poder ser chamada fora de uma requisicao.
    """
    conexao = sqlite3.connect(config.DATABASE)
    conexao.execute("PRAGMA foreign_keys = ON")
    conexao.executescript(_ler_arquivo_sql(config.SCHEMA_FILE))
    if com_dados_exemplo:
        conexao.executescript(_ler_arquivo_sql(config.SEED_FILE))
    conexao.commit()
    conexao.close()


def garantir_banco():
    """Cria o banco automaticamente na primeira execucao, se ainda nao existir."""
    if not os.path.exists(config.DATABASE):
        init_db(com_dados_exemplo=True)
