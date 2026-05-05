from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')
   

@app.route('/contato')
def contato():
    nome = "Joãozinho"
    return render_template('index.html', title= 'Página inicial', nome=nome)

@app.route('/usuario')
def usuario():
    usuario = {'nome:', 'João', 'email:', 'joaozinho@gmail.com'}
    return render_template('index.html', title= 'Página inicial', usuario=usuario)

if __name__ == '__main__':
    app.run()

