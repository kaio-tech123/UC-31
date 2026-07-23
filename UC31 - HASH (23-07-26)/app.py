from flask import Flask, render_template, session, redirect, url_for, request
from functools import wraps

app = Flask(__name__)
app.secret_key = 'chave_secreta_qualquer'

def login_necessario(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'usuario_nome' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorada


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form.get('nome')
        session['usuario_nome'] = nome
        return redirect(url_for('painel'))
    return render_template('login.html')


@app.route('/painel')
@login_necessario
def painel():
    nome = session.get('usuario_nome')
    return render_template('painel.html', nome=nome)


@app.route('/cantinho')
@login_necessario
def cantinho():
    nome = session.get('usuario_nome')

    visitas = session.get('visitas_cantinho', 0)
    visitas += 1
    session['visitas_cantinho'] = visitas

    return render_template('cantinho.html',
                           nome=nome,
                           cor='Azul',
                           linguagem='Python',
                           frase='Devagar se vai ao longe',
                           visitas=visitas)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)