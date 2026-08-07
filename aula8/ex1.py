from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Meu nome é João Silva"

if __name__ == "__main__":
    app.run(debug=True)
