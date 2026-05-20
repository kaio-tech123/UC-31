from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cardapio')
def cardapio():
    return render_template('cardapio.html')

@app.route('/lanche/<nome>')
def lanche(nome):
    lanches_validos = ['pizza', 'hamburguer', 'batata', 'milkshake']
    
    encontrado = nome.lower() in lanches_validos
    
    return render_template('lanche.html', nome=nome, encontrado=encontrado)

@app.route('/pedidos')
def pedidos():
    return render_template('pedidos.html')

@app.route('/cliente')
def cliente(nome, city):
    
    return render_template('cliente.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

if __name__ == '__main__':
    app.run(debug=True)