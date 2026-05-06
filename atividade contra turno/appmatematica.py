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