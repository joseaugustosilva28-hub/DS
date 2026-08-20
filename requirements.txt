-- ============================================================
-- Projeto Final - API Biblioteca
-- Estrutura do banco de dados (SQLite)
-- Tabela "pai":   autores
-- Tabela "filho": livros  (FOREIGN KEY -> autores.id)
-- ============================================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS livros;
DROP TABLE IF EXISTS autores;

-- ----------------------------
-- Tabela pai: autores
-- ----------------------------
CREATE TABLE autores (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    nome           TEXT    NOT NULL,
    nacionalidade  TEXT    NOT NULL DEFAULT 'Desconhecida',
    ano_nascimento INTEGER
);

-- ----------------------------
-- Tabela filho: livros
-- Cada livro pertence a um autor.
-- ON DELETE CASCADE: ao apagar o autor, seus livros sao apagados.
-- ----------------------------
CREATE TABLE livros (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo     TEXT    NOT NULL,
    ano        INTEGER,
    preco      REAL    NOT NULL DEFAULT 0,
    autor_id   INTEGER NOT NULL,
    FOREIGN KEY (autor_id) REFERENCES autores (id) ON DELETE CASCADE
);

-- Indice para acelerar as buscas dos livros por autor
CREATE INDEX idx_livros_autor_id ON livros (autor_id);
