import json
import os
from datetime import datetime, timedelta

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "gameshub-edu-senha-secreta"

PASTA_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
CAMINHO_USUARIOS = os.path.join(PASTA_DADOS, "usuarios.json")
CAMINHO_JOGOS = os.path.join(PASTA_DADOS, "jogos.json")
CAMINHO_ALUGUEIS = os.path.join(PASTA_DADOS, "alugueis.json")

DIAS_ALUGUEL = 7


def ler_json(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read().strip()
        return json.loads(conteudo) if conteudo else []


def salvar_json(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def buscar(lista, campo, valor):
    for item in lista:
        if item[campo] == valor:
            return item
    return None


def gerar_novo_id(lista):
    return max([item["id"] for item in lista], default=0) + 1


@app.context_processor
def dados_globais():
    usuario_id = session.get("usuario_id")
    usuario = buscar(ler_json(CAMINHO_USUARIOS), "id", usuario_id) if usuario_id else None
    return {"usuario_logado": usuario}


@app.route("/")
def catalogo():
    jogos = ler_json(CAMINHO_JOGOS)
    ids_alugados = [a["jogo_id"] for a in ler_json(CAMINHO_ALUGUEIS)]
    for jogo in jogos:
        jogo["disponivel"] = jogo["id"] not in ids_alugados

    categoria_filtro = request.args.get("categoria", "")
    busca = request.args.get("busca", "").lower()

    if categoria_filtro:
        jogos = [j for j in jogos if j["categoria"] == categoria_filtro]
    if busca:
        jogos = [j for j in jogos if busca in j["nome"].lower()]

    categorias = sorted(set(j["categoria"] for j in ler_json(CAMINHO_JOGOS)))

    return render_template(
        "catalogo.html", jogos=jogos, categorias=categorias,
        categoria_filtro=categoria_filtro, busca=busca,
    )


@app.route("/jogo/<int:jogo_id>")
def detalhe_jogo(jogo_id):
    jogo = buscar(ler_json(CAMINHO_JOGOS), "id", jogo_id)
    if not jogo:
        flash("Esse jogo nao existe.", "erro")
        return redirect(url_for("catalogo"))

    alugados = [a["jogo_id"] for a in ler_json(CAMINHO_ALUGUEIS)]
    jogo["disponivel"] = jogo_id not in alugados
    return render_template("jogo_detalhe.html", jogo=jogo)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method != "POST":
        return render_template("cadastro.html", nome="", email="")

    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha", "")
    confirmar = request.form.get("confirmar_senha", "")
    usuarios = ler_json(CAMINHO_USUARIOS)

    erro = None
    if len(nome) < 2:
        erro = "Informe um nome valido."
    elif "@" not in email:
        erro = "Informe um email valido."
    elif len(senha) < 4:
        erro = "A senha precisa ter pelo menos 4 caracteres."
    elif senha != confirmar:
        erro = "As senhas nao sao iguais."
    elif buscar(usuarios, "email", email):
        erro = "Ja existe uma conta com esse email."

    if erro:
        flash(erro, "erro")
        return render_template("cadastro.html", nome=nome, email=email)

    usuarios.append({
        "id": gerar_novo_id(usuarios),
        "nome": nome,
        "email": email,
        "senha_hash": generate_password_hash(senha),
        "data_cadastro": datetime.now().strftime("%d/%m/%Y"),
    })
    salvar_json(CAMINHO_USUARIOS, usuarios)
    flash("Conta criada com sucesso. Agora faca login.", "sucesso")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method != "POST":
        return render_template("login.html", email="")

    email = request.form.get("email", "").strip().lower()
    senha = request.form.get("senha", "")
    usuario = buscar(ler_json(CAMINHO_USUARIOS), "email", email)

    if usuario and check_password_hash(usuario["senha_hash"], senha):
        session["usuario_id"] = usuario["id"]
        flash("Login feito com sucesso.", "sucesso")
        return redirect(url_for("catalogo"))

    flash("Email ou senha incorretos.", "erro")
    return render_template("login.html", email=email)


@app.route("/logout")
def logout():
    session.pop("usuario_id", None)
    flash("Voce saiu da conta.", "sucesso")
    return redirect(url_for("catalogo"))


@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    if not session.get("usuario_id"):
        flash("Entre na sua conta para ver o perfil.", "aviso")
        return redirect(url_for("login"))

    usuarios = ler_json(CAMINHO_USUARIOS)
    usuario = buscar(usuarios, "id", session["usuario_id"])

    if request.method == "POST":
        novo_nome = request.form.get("nome", "").strip()
        if len(novo_nome) < 2:
            flash("Informe um nome valido.", "erro")
        else:
            usuario["nome"] = novo_nome
            salvar_json(CAMINHO_USUARIOS, usuarios)
            flash("Perfil atualizado.", "sucesso")
            return redirect(url_for("perfil"))

    meus_alugueis = [a for a in ler_json(CAMINHO_ALUGUEIS) if a["usuario_id"] == usuario["id"]]
    for aluguel in meus_alugueis:
        aluguel["jogo"] = buscar(ler_json(CAMINHO_JOGOS), "id", aluguel["jogo_id"])

    return render_template("perfil.html", usuario=usuario, meus_alugueis=meus_alugueis)


@app.route("/alugar/<int:jogo_id>", methods=["POST"])
def alugar_jogo(jogo_id):
    if not session.get("usuario_id"):
        flash("Entre na sua conta para alugar um jogo.", "aviso")
        return redirect(url_for("login"))

    jogo = buscar(ler_json(CAMINHO_JOGOS), "id", jogo_id)
    alugueis = ler_json(CAMINHO_ALUGUEIS)

    if not jogo:
        flash("Jogo nao encontrado.", "erro")
        return redirect(url_for("catalogo"))
    if buscar(alugueis, "jogo_id", jogo_id):
        flash("Esse jogo ja esta alugado.", "aviso")
        return redirect(url_for("detalhe_jogo", jogo_id=jogo_id))

    hoje = datetime.now()
    alugueis.append({
        "id": gerar_novo_id(alugueis),
        "usuario_id": session["usuario_id"],
        "jogo_id": jogo_id,
        "data_inicio": hoje.strftime("%d/%m/%Y"),
        "data_devolucao": (hoje + timedelta(days=DIAS_ALUGUEL)).strftime("%d/%m/%Y"),
    })
    salvar_json(CAMINHO_ALUGUEIS, alugueis)
    flash("Jogo alugado com sucesso.", "sucesso")
    return redirect(url_for("perfil"))


@app.route("/devolver/<int:aluguel_id>", methods=["POST"])
def devolver_jogo(aluguel_id):
    if not session.get("usuario_id"):
        flash("Entre na sua conta para devolver um jogo.", "aviso")
        return redirect(url_for("login"))

    alugueis = ler_json(CAMINHO_ALUGUEIS)
    aluguel = buscar(alugueis, "id", aluguel_id)

    if not aluguel or aluguel["usuario_id"] != session["usuario_id"]:
        flash("Aluguel nao encontrado.", "erro")
        return redirect(url_for("perfil"))

    alugueis.remove(aluguel)
    salvar_json(CAMINHO_ALUGUEIS, alugueis)
    flash("Jogo devolvido com sucesso.", "sucesso")
    return redirect(url_for("perfil"))


if __name__ == "__main__":
    app.run(debug=True)
