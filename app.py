from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

usuario_cadastrado = None
senha_cadastrada = None

@app.route('/', methods=['GET', 'POST'])
def cadastro():
    global usuario_cadastrado, senha_cadastrada
    
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        
        senha_cadastrada = generate_password_hash(senha)
        usuario_cadastrado = nome
        
        return redirect(url_for('login'))
        
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global usuario_cadastrado, senha_cadastrada
    erro = None
    
    if request.method == 'POST':
        nome_tentativa = request.form['nome']
        senha_tentativa = request.form['senha']
        
        if usuario_cadastrado and nome_tentativa == usuario_cadastrado:
            if check_password_hash(senha_cadastrada, senha_tentativa):
                return render_template('boas_vindas.html', nome=usuario_cadastrado)
            else:
                erro = "Senha incorreta!"
        else:
            erro = "Usuário não encontrado!"
            
    return render_template('login.html', erro=erro)

if __name__ == '__main__':
    app.run(debug=True)