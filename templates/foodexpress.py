from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# 2. Cardápio (Lista de lanches)
@app.route('/cardapio')
def cardapio():
    return render_template('cardapio.html')

# 3. Página dinâmica do lanche
@app.route('/lanche/<nome>')
def lanche(nome):
    return render_template('lanche.html', nome_lanche=nome)

# 4. Página de pedidos
@app.route('/pedidos')
def pedidos():
    return render_template('pedidos.html')

# 5. Página dinâmica do cliente
@app.route('/cliente/<nome>/<cidade>')
def cliente(nome, cidade):
    return render_template('cliente.html', nome_cliente=nome, cidade_cliente=cidade)

# 6. Página de contato
@app.route('/contato')
def contato():
    return render_template('contato.html')

if __name__ == '__main__':
    app.run(debug=True)