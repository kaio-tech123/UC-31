from flask import (
    Flask,
    render_template,
    request,
    make_response,
    redirect,
    url_for
)

app = Flask(__name__)

@app.route('/')
def inicio():

    nome = request.cookies.get('nome')
    email = request.cookies.get('email')
    tema = request.cookies.get('tema', 'claro')

    return render_template(
        'inicio.html',
        nome=nome,
        email=email,
        tema=tema
    )

@app.route('/salvar', methods=['POST'])
def salvar():
    nome = request.form['nome']
    email = request.form['email']

    resposta = make_response(redirect('/'))
    resposta.set_cookie('nome', nome, max_age=60*60*24*30)
    resposta.set_cookie('email', email, max_age=60*60*24*30)

    return resposta

@app.route('/tema/<escolha>')
def trocar_tema(escolha):

    if escolha not in ['claro', 'escuro']:
        escolha = 'claro'

    resposta = make_response(
        redirect(url_for('inicio'))
    )

    resposta.set_cookie(
        'tema',
        escolha,
        max_age=60*60*24*30
    )

    return resposta

if __name__ == '__main__':
    app.run(debug=True)