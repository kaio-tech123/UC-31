from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = "segredo123"

perguntas = [
    {
        "pergunta": "Qual é o nome da maior casa de apostas do Brasil?",
        "opcoes": ["Bet365", "Betano", "Estrela Bet", "Sportingbet"],
        "correta": "Betano"
    },
    {
        "pergunta": "O que significa 'odd' em apostas esportivas?",
        "opcoes": ["O valor do prêmio", "A probabilidade do evento acontecer", "O multiplicador de ganho", "O limite de aposta"],
        "correta": "O multiplicador de ganho"
    },
    {
        "pergunta": "O que é uma aposta 'ao vivo'?",
        "opcoes": [
            "Aposta feita pessoalmente na banca",
            "Aposta realizada enquanto o evento está acontecendo",
            "Aposta com transmissão ao vivo na TV",
            "Aposta com odds em tempo real mas só antes do jogo"
        ],
        "correta": "Aposta realizada enquanto o evento está acontecendo"
    },
    {
        "pergunta": "O que é 'cashout' em apostas?",
        "opcoes": [
            "Sacar todo o saldo da conta",
            "Encerrar uma aposta antes do resultado final",
            "Apostar o dobro para recuperar perda",
            "Transferir saldo entre contas"
        ],
        "correta": "Encerrar uma aposta antes do resultado final"
    },
    {
        "pergunta": "Qual órgão regulamenta as casas de apostas no Brasil?",
        "opcoes": ["BACEN", "ANATEL", "SPA (Secretaria de Prêmios e Apostas)", "ANVISA"],
        "correta": "SPA (Secretaria de Prêmios e Apostas)"
    }
]


@app.route("/")
def index():
    return """
    <h2>🎰 Quiz - Casas de Apostas</h2>
    <p>Teste seus conhecimentos sobre o mundo das apostas esportivas!</p>
    <a href="/quiz">Começar o quiz</a>
    """


@app.route("/quiz")
def quiz():
    # se for a primeira vez, inicializa a session
    if "questao_atual" not in session:
        session["questao_atual"] = 0
        session["pontuacao"] = 0

    numero = session["questao_atual"]

    # se já respondeu tudo, manda pro resultado
    if numero >= len(perguntas):
        return redirect(url_for("resultado"))

    pergunta_atual = perguntas[numero]

    # monta o html das opções
    opcoes_html = ""
    for opcao in pergunta_atual["opcoes"]:
        opcoes_html += f"""
        <label style="display:block; margin: 8px 0;">
            <input type="radio" name="resposta" value="{opcao}"> {opcao}
        </label>
        """

    return f"""
    <h2>Pergunta {numero + 1} de {len(perguntas)}</h2>
    <p><strong>{pergunta_atual['pergunta']}</strong></p>

    <form action="/responder" method="POST">
        {opcoes_html}
        <br>
        <button type="submit">Responder</button>
    </form>

    <p style="color: gray;">Pontuação atual: {session['pontuacao']}</p>
    """


@app.route("/responder", methods=["POST"])
def responder():
    resposta_usuario = request.form.get("resposta")
    numero = session["questao_atual"]

    # verifica se a resposta tá certa
    if resposta_usuario == perguntas[numero]["correta"]:
        session["pontuacao"] += 1

    # passa pra próxima pergunta
    session["questao_atual"] = numero + 1

    return redirect(url_for("quiz"))


@app.route("/resultado")
def resultado():
    pontuacao = session.get("pontuacao", 0)
    total = len(perguntas)

    if pontuacao == total:
        mensagem = "🏆 Perfeito! Você é expert em apostas!"
    elif pontuacao >= 3:
        mensagem = "😎 Muito bem! Você manja do assunto."
    elif pontuacao >= 2:
        mensagem = "📚 Razoável! Vale estudar mais um pouco."
    else:
        mensagem = "😅 Opa... bora aprender mais sobre o tema!"

    # limpa a session pra poder jogar de novo
    session.clear()

    return f"""
    <h2>Resultado Final</h2>
    <p>Você acertou <strong>{pontuacao} de {total}</strong> perguntas.</p>
    <p>{mensagem}</p>
    <br>
    <a href="/quiz">Jogar de novo</a>
    """


if __name__ == "__main__":
    app.run(debug=True)