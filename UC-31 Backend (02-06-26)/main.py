from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

    mensagem = ""

    if request.method == 'POST':
        nome = request.form.get('nome')
        if not nome:
            mensagem = "O campo nome não pode estar vazio"
        jogo = request.form.get('jogo')
        if not jogo:
            mensagem = "O campo jogo não pode estar vazio"
        email = request.form.get('email')
        if not email:
            mensagem = "O email não pode estar vazio"
        else:
            mensagem = f"Cadastro realizado com sucesso! Seja bem-vindo, {nome}"
    return render_template('cadastro.html', mensagem=mensagem)

if __name__ == '__main__':
    app.run(debug=True)