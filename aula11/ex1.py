import sqlite3

conexao = sqlite3.connect("loja.db")

cursor = conexao.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    preco REAL
)
""")


cursor.execute(
    "INSERT INTO produtos (nome, preco) VALUES (?, ?)",
    ("Mouse", 50)
)

cursor.execute(
    "INSERT INTO produtos (nome, preco) VALUES (?, ?)",
    ("Teclado", 100)
)

cursor.execute(
    "INSERT INTO produtos (nome, preco) VALUES (?, ?)",
    ("Monitor", 800)
)


conexao.commit()

conexao.close()

print("Produtos cadastrados!")
