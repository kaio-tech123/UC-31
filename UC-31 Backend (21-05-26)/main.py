from flask import Flask, render_template
from flask import request

app = Flask (__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html')

@app.route('/autenticar', methods = ['GET'])
def autenticar():
    usuario = request.args.get('usuario')
    senha = request.args.get('senha')
    return render_template(
        'autenticar.html',
        usuario=usuario,
        senha=senha
    )

if __name__ == '__main__':
    app.run(debug=True)