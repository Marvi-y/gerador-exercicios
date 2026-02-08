import random
import streamlit as st

def dificuldade_por_nivel(nivel, lang):
    if nivel == 1:
        return "Fácil" if lang == "pt" else "Easy"
    elif nivel == 2:
        return "Médio" if lang == "pt" else "Medium"
    else:
        return "Difícil" if lang == "pt" else "Hard"


def gerar_exercicio(T, lang):
    if st.session_state.modo_treino_erros and st.session_state.erros:
        erro = random.choice(st.session_state.erros)
        st.session_state.update(erro)
        return

    dificuldade = (
        st.session_state.dificuldade_manual
        or dificuldade_por_nivel(st.session_state.nivel, lang)
    )

    if dificuldade in ["Fácil", "Easy"]:
        minimo, maximo = 1, 10
    elif dificuldade in ["Médio", "Medium"]:
        minimo, maximo = 10, 50
    else:
        minimo, maximo = 50, 100

    a = random.randint(minimo, maximo)
    b = random.randint(minimo, maximo)
    operacao = random.choice(["+", "-", "*", "/", "^"])

    operacao = random.choice(["+", "-", "*", "/", "^"])
    st.session_state.update({
        "a": a,
        "b": b,
        "operacao": operacao,
        "resultado": resultado,
        "explicacao": explicacao
    })
