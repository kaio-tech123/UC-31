from flask import Flask

app = Flask(__name__)

@app.route('/arearestrita/<int:id>')
def area_restrita(id):
    if id == 1:
        return "<h1>Cadeado Fechado</h1>"
    elif id == 2:
        return "<h1>Cadeado Aberto</h1>"
    else:
        return "<h1>ID inválido! Use 1 ou 2</h1>", 400


# Página inicial simples
@app.route('/')
def home():
    return '''
    <h1>Questão 03 - Área Restrita</h1>
    <p><a href="/arearestrita/1">Testar Cadeado Fechado (ID 1)</a></p>
    <p><a href="/arearestrita/2">Testar Cadeado Aberto (ID 2)</a></p>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=5000)