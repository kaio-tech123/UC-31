from flask import Flask, render_template
from flask import request

app = Flask (__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('login02.html')

@app.route('/autenticar02', methods = ['GET'])
def autenticar():
    nome = request.args.get('nome')
    curso = request.args.get('curso')
    cidade = request.args.get('cidade')
    idade = request.args.get('idade')
    return render_template(
        'autenticar02.html',
        nome=nome,
        curso=curso,
        cidade=cidade,
        idade=idade
    )

if __name__ == '__main__':
    app.run(debug=True)