from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash
)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'chave-aula-quiz-apostas'


PERGUNTAS = [
    {
        'pergunta': 'Qual é o nome da maior casa de apostas do Brasil?',
        'opcoes': ['Bet365', 'Betano', 'Estrela Bet', 'Sportingbet'],
        'correta': 'Betano'
    },
    {
        'pergunta': "O que significa 'odd' em apostas esportivas?",
        'opcoes': ['O valor do prêmio', 'A probabilidade do evento acontecer', 'O multiplicador de ganho', 'O limite de aposta'],
        'correta': 'O multiplicador de ganho'
    },
    {
        'pergunta': "O que é uma aposta 'ao vivo'?",
        'opcoes': [
            'Aposta feita pessoalmente na banca',
            'Aposta realizada enquanto o evento está acontecendo',
            'Aposta com transmissão ao vivo na TV',
            'Aposta com odds em tempo real mas só antes do jogo'
        ],
        'correta': 'Aposta realizada enquanto o evento está acontecendo'
    },
    {
        'pergunta': "O que é 'cashout' em apostas?",
        'opcoes': [
            'Sacar todo o saldo da conta',
            'Encerrar uma aposta antes do resultado final',
            'Apostar o dobro para recuperar perda',
            'Transferir saldo entre contas'
        ],
        'correta': 'Encerrar uma aposta antes do resultado final'
    },
    {
        'pergunta': 'Qual órgão regulamenta as casas de apostas no Brasil?',
        'opcoes': ['BACEN', 'ANATEL', 'SPA (Secretaria de Prêmios e Apostas)', 'ANVISA'],
        'correta': 'SPA (Secretaria de Prêmios e Apostas)'
    }
]


@app.route('/')
def inicio():
    return render_template('inicio.html', total_perguntas=len(PERGUNTAS))


@app.route('/quiz')
def quiz():

    if 'questao_atual' not in session:
        session['questao_atual'] = 0
        session['pontuacao'] = 0

    numero = session['questao_atual']

    if numero >= len(PERGUNTAS):
        return redirect(url_for('resultado'))

    pergunta_atual = PERGUNTAS[numero]

    progresso = int(numero / len(PERGUNTAS) * 100)

    return render_template(
        'quiz.html',
        numero=numero,
        total=len(PERGUNTAS),
        pergunta=pergunta_atual['pergunta'],
        opcoes=pergunta_atual['opcoes'],
        pontuacao=session['pontuacao'],
        progresso=progresso
    )


@app.route('/responder', methods=['POST'])
def responder():

    if 'questao_atual' not in session:
        return redirect(url_for('quiz'))

    resposta_usuario = request.form.get('resposta')
    numero = session['questao_atual']

    if not resposta_usuario:
        flash('Selecione uma opção antes de responder.', 'erro')
        return redirect(url_for('quiz'))

    pergunta_atual = PERGUNTAS[numero]

    if resposta_usuario == pergunta_atual['correta']:
        session['pontuacao'] += 1
        flash('Você acertou!', 'sucesso')
    else:
        flash(f"Você errou! A resposta certa era: {pergunta_atual['correta']}", 'erro')

    session['questao_atual'] = numero + 1

    session.modified = True

    return redirect(url_for('quiz'))


@app.route('/resultado')
def resultado():

    pontuacao = session.get('pontuacao', 0)
    total = len(PERGUNTAS)

    if pontuacao == total:
        mensagem = 'Perfeito! Você é expert em apostas! (sai do fake laerte)'
    elif pontuacao >= 3:
        mensagem = 'Boaaa! Você sabe do assunto.'
    elif pontuacao >= 2:
        mensagem = 'Mais ou menos... Melhor do que nada.'
    else:
        mensagem = 'Eita... bora aprender mais sobre o tema!'

    session.pop('questao_atual', None)
    session.pop('pontuacao', None)

    return render_template(
        'resultado.html',
        pontuacao=pontuacao,
        total=total,
        mensagem=mensagem
    )


@app.route('/reiniciar')
def reiniciar():

    session.clear()

    flash('Quiz reiniciado!', 'info')

    return redirect(url_for('inicio'))


if __name__ == '__main__':
    app.run(debug=True)