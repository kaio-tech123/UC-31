from flask import Flask, render_template

app = Flask(__name__)

@app.route('/ola/<nome>')
def saudacao(nome):
    # O Flask pega o que estiver na URL e coloca na variável 'nome'
    return f"Olá, {nome}! Seja bem-vinda ao sistema."