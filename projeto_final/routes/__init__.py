"""Pacote com os Blueprints (grupos de rotas) da API."""

from routes.autores import autores_bp
from routes.livros import livros_bp

__all__ = ["autores_bp", "livros_bp"]
