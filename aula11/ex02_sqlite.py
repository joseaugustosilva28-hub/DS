import sqlite3

conexao = sqlite3.connect("loja.db")

cursor = conexao.cursor()


cursor.execute("SELECT * FROM produtos")

produtos = cursor.fetchall()


for produto in produtos:
    print(produto)


conexao.close()
