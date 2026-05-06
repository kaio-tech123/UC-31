from flask import Flask

app = Flask(__name__)

@app.route('/operacao/<string:tipo>/<op1>/<op2>')
def operacao(tipo, op1, op2):
    try:
        n1 = float(op1)
        n2 = float(op2)
    except:
        return "<h1>Erro: Use números válidos!</h1>"

    if tipo == "sum":
        resultado = n1 + n2
    elif tipo == "sub":
        resultado = n1 - n2
    elif tipo == "mult":
        resultado = n1 * n2
    elif tipo == "div":
        if n2 == 0:
            return "<h1>Erro: Divisão por zero!</h1>"
        resultado = n1 / n2
    else:
        return "<h1>Tipo inválido! (sum, sub, mult, div)</h1>"

    return f"<h1>{tipo.upper()} = {resultado}</h1>"


@app.route('/')
def home():
    return '''
    <h1>Questão 04 - Simplificado</h1>
    <p><a href="/operacao/sum/10/5">sum 10 5</a></p>
    <p><a href="/operacao/sub/20/7">sub 20 7</a></p>
    <p><a href="/operacao/mult/6/8">mult 6 8</a></p>
    <p><a href="/operacao/div/100/4">div 100 4</a></p>
    '''


if __name__ == '__main__':
    app.run(debug=True)