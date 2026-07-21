from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
ARQUIVO = "livros.json"


def carregar_livros():
    if not os.path.exists(ARQUIVO):
        salvar_livros([])
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def salvar_livros(livros):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(livros, f, indent=4, ensure_ascii=False)


@app.route("/", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        ano = request.form["ano"]
        categoria = request.form["categoria"]
        quantidade = request.form["quantidade"]

        if not titulo or not autor or not ano or not categoria or not quantidade:
            return render_template("cadastro.html", erro="Preencha todos os campos.")
        if not ano.isdigit():
            return render_template("cadastro.html", erro="O ano deve ser numérico.")
        if not quantidade.isdigit() or int(quantidade) <= 0:
            return render_template("cadastro.html", erro="A quantidade deve ser maior que zero.")

        livros = carregar_livros()
        livros.append({
            "titulo": titulo,
            "autor": autor,
            "ano": ano,
            "categoria": categoria,
            "quantidade": int(quantidade)
        })
        salvar_livros(livros)
        return redirect(url_for("listar"))

    return render_template("cadastro.html")


@app.route("/livros")
def listar():
    return render_template("livros.html", livros=carregar_livros())


@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    resultado = None
    buscou = False

    if request.method == "POST":
        buscou = True
        titulo = request.form["titulo"]
        for livro in carregar_livros():
            if livro["titulo"].lower() == titulo.lower():
                resultado = livro
                break

    return render_template("buscar.html", resultado=resultado, buscou=buscou)


@app.route("/editar/<int:indice>", methods=["GET", "POST"])
def editar(indice):
    livros = carregar_livros()

    if request.method == "POST":
        livros[indice] = {
            "titulo": request.form["titulo"],
            "autor": request.form["autor"],
            "ano": request.form["ano"],
            "categoria": request.form["categoria"],
            "quantidade": int(request.form["quantidade"])
        }
        salvar_livros(livros)
        return redirect(url_for("listar"))

    return render_template("editar.html", livro=livros[indice], indice=indice)


@app.route("/excluir/<int:indice>")
def excluir(indice):
    livros = carregar_livros()
    livros.pop(indice)
    salvar_livros(livros)
    return redirect(url_for("listar"))


if __name__ == "__main__":
    app.run(debug=True)