from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/validação', methods = ['POST'])
def cadastro():

    nome = request.form.get('nome', '').strip().title()    
    email = request.form.get('email', '').strip()
    telefone = request.form.get('telefone', '').strip().replace()
    CPF = request.form.get('CPF', '').strip().replace()
    cidade = request.form.get('cidade', '').strip().title()
    estado = request.form.get('estado', '').strip()
    curso = request.form.get('curso', '').strip()
    idade = request.form.get('idade', '').strip()
    senha = request.form.get('senha', '').strip()

    erros = []

    if telefone:
        try:
            int(telefone)
            if len(telefone) != 11:
                erros.append("Telefone inválido.")
        except ValueError:
            erros.append("Telefone inválido.")

    if CPF:
        try:
            int(CPF)
            if len(CPF) != 11:
                erros.append("CPF inválido.")
        except ValueError:
            erros.append("CPF inválido.")

    if cidade and len(cidade) < 3:
        erros.append("Cidade inválida.")

    if estado and len(estado) != 2:
        erros.append("Estado inválido.")

    if idade:
        try:
            if int(idade) < 16:
                erros.append("Idade inválida.")
        except ValueError:
            erros.append("Idade inválida.")

    if senha:
        tem_numero = any(char.isdigit() for char in senha)
        if len(senha) < 8 or not tem_numero:
            erros.append("Senha muito fraca.")

   
    return f"""
    Cadastro realizado com sucesso!<br><br>
    Nome: {nome}<br>
    E-mail: {email}<br>
    Telefone: {telefone}<br>
    CPF: {CPF}<br>
    Cidade: {cidade}<br>
    Estado: {estado}<br>
    Curso: {curso}<br>
    Idade: {idade}<br>


    """

if __name__ == '__name__':
    app.run(debug=True)