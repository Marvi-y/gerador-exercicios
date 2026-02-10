import streamlit as st

def init_state():
    defaults = {
        "nivel": 1,
        "acertos": 0,
        "historico": [],
        "erros": [],
        "modo_treino_erros": False,
        "dificuldade_manual": None,

        "a": None,
        "b": None,
        "operacao": None,
        "resultado": None,
        "explicacao": None,

        "operacoes_ativas": ["+", "-", "*"],
        "novo_exercicio": True,
    }

    for k, v in defaults.items():
        st.session_state.setdefault(k, v)
