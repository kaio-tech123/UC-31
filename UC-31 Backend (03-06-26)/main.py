from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/validação', methods = ['POST'])
def cadastro():

    nome = request.form.get('nome', '').strip().title()
    email = request.form.get('email', '').strip().lower()
    cidade = request.form.get('cidade', '').strip().title()

    return f"""
    Nome: {nome}<br>
    Email: {email}<br>
    Cidade: {cidade}
    """

if __name__ == '__name__':
    app.run(debug=True)