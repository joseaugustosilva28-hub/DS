"""Configuracoes gerais do projeto (caminhos e parametros do servidor)."""

import os

# Pasta raiz do projeto (onde este arquivo esta)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pasta com os arquivos .sql
SQL_DIR = os.path.join(BASE_DIR, "sql")

# Arquivo do banco de dados SQLite
DATABASE = os.path.join(BASE_DIR, "biblioteca.db")

# Scripts SQL usados na criacao do banco
SCHEMA_FILE = os.path.join(SQL_DIR, "schema.sql")
SEED_FILE = os.path.join(SQL_DIR, "seed.sql")

# Configuracoes do servidor Flask
HOST = "127.0.0.1"
PORT = 5000
DEBUG = True
