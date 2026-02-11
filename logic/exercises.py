import random
import streamlit as st
from logic.difficulty import dificuldade_por_nivel

def gerar_exercicio(T, lang):

    # 🔁 MODO CORREÇÃO
    if st.session_state.modo_correcao:
        if not st.session_state.erros:
            st.session_state.modo_correcao = False
            st.session_state.novo_exercicio = True
            return

        erro = st.session_state.erros[0]

        st.session_state.update({
            "a": erro["a"],
            "b": erro["b"],
            "operacao": erro["operacao"],
            "resultado": erro["resultado"],
            "explicacao": erro["explicacao"],
        })
        return

    # 🔹 MODO NORMAL
    dificuldade = st.session_state.dificuldade_manual
    if not dificuldade:
        dificuldade = dificuldade_por_nivel(st.session_state.nivel, lang)

    if dificuldade in ["Fácil", "Easy"]:
        minimo, maximo = 1, 10
    elif dificuldade in ["Médio", "Medium"]:
        minimo, maximo = 10, 50
    else:
        minimo, maximo = 50, 100

    operacao = random.choice(st.session_state.operacoes_ativas)

    if operacao == "+":
        a, b = random.randint(minimo, maximo), random.randint(minimo, maximo)
        resultado = a + b
        explicacao = T["tip_sum"]

    elif operacao == "-":
        a, b = random.randint(minimo, maximo), random.randint(minimo, maximo)
        resultado = a - b
        explicacao = T["tip_sub"]

    elif operacao == "*":
        a, b = random.randint(minimo, maximo), random.randint(minimo, maximo)
        resultado = a * b
        explicacao = T["tip_mul"]

    else:
        raise ValueError("Operação inválida")

    st.session_state.update({
        "a": a,
        "b": b,
        "operacao": operacao,
        "resultado": resultado,
        "explicacao": explicacao,
    })
