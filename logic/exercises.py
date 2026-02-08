import random
import streamlit as st
from logic.difficulty import dificuldade_por_nivel

def gerar_exercicio(T, lang):
    dificuldade = st.session_state.dificuldade_manual

    if not dificuldade:
        dificuldade = dificuldade_por_nivel(st.session_state.nivel, lang)

    if dificuldade in ["Fácil", "Easy"]:
        minimo, maximo = 1, 10
    elif dificuldade in ["Médio", "Medium"]:
        minimo, maximo = 10, 50
    else:
        minimo, maximo = 50, 100

    operacoes = st.session_state.get("operacoes_ativas", ["+", "-", "*"])
    operacao = random.choice(operacoes)

    # valores padrão (segurança)
    a = b = resultado = None
    explicacao = ""

    if operacao == "+":
        a = random.randint(minimo, maximo)
        b = random.randint(minimo, maximo)
        resultado = a + b
        explicacao = T["tip_sum"]

    elif operacao == "-":
        a = random.randint(minimo, maximo)
        b = random.randint(minimo, maximo)
        resultado = a - b
        explicacao = T["tip_sub"]

    elif operacao == "*":
        a = random.randint(minimo, maximo)
        b = random.randint(minimo, maximo)
        resultado = a * b
        explicacao = T["tip_mul"]

    elif operacao == "/":
        b = random.randint(1, 10)
        resultado = random.randint(1, 10)
        a = b * resultado
        explicacao = T["tip_div"]

    elif operacao == "^":
        a = random.randint(2, 5)
        b = random.randint(2, 3)
        resultado = a ** b
        explicacao = T["tip_pow"]

    else:
        raise ValueError(f"Operação inválida: {operacao}")

    st.session_state.update({
        "a": a,
        "b": b,
        "operacao": operacao,
        "resultado": resultado,
        "explicacao": explicacao
    })
