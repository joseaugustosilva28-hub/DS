import sqlite3


conexao = sqlite3.connect("biblioteca.db")

cursor = conexao.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS autores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor_id INTEGER,
    FOREIGN KEY (autor_id) REFERENCES autores(id)
)
""")


cursor.execute(
    "INSERT INTO autores (nome) VALUES (?)",
    ("Machado de Assis",)
)

cursor.execute(
    "INSERT INTO autores (nome) VALUES (?)",
    ("J.K. Rowling",)
)


cursor.execute(
    "INSERT INTO livros (titulo, autor_id) VALUES (?, ?)",
    ("Dom Casmurro", 1)
)

cursor.execute(
    "INSERT INTO livros (titulo, autor_id) VALUES (?, ?)",
    ("Memorias Postumas", 1)
)

cursor.execute(
    "INSERT INTO livros (titulo, autor_id) VALUES (?, ?)",
    ("Harry Potter", 2)
)


conexao.commit()

conexao.close()

print("Banco criado e dados inseridos!")
