from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__) 

ARQUIVO = "filmes.json"

def carregar_filmes():
    """Lê o arquivo JSON e retorna uma lista de filmes"""

    if not os.path.exists(ARQUIVO):
        return []
    
    with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
        try:
            return json.load(arquivo)
        except json.JSONDecodeError:
            return []
        
def salvar_filmes(lista_filmes):
    """Salva a lista de filmes no arquivo JSON."""

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(
            lista_filmes,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


@app.route("/", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        filme = {
            "nome": request.form["nome"],
            "genero": request.form["genero"],
            "ano": request.form["ano"]
        }

        filmes = carregar_filmes()
        filmes.append(filme)
        salvar_filmes(filmes)

        return redirect(url_for("listar"))
    
    return render_template("cadastro.html")

@app.route("/filmes")
def listar():

    filmes = carregar_filmes()

    return render_template(
        "filmes.html",
        filmes=filmes
    )

if __name__=="__main__":
    app.run(debug=True)