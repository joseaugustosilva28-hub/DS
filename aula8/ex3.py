from flask import Flask
from datetime import date

app = Flask(__name__)

@app.route("/saudacao")
def saudacao():
    return "Bem-vindo a minha API!"

@app.route("/data")
def data():
    hoje = date.today()
    return str(hoje)

if __name__ == "__main__":
    app.run(debug=True)
