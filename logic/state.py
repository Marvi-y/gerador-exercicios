import streamlit as st

def init_state():
    defaults = {
        # exercício atual
        "a": None,
        "b": None,
        "operacao": None,
        "resultado": None,
        "explicacao": None,

        # progressão
        "nivel": 1,
        "acertos": 0,
        "dificuldade_manual": None, 

        # histórico
        "historico": [],
        "erros": [],

        # modos
        "modo_correcao": False,

        # configurações
        "operacoes_ativas": ["+", "-", "*"],
        "lang": "pt",
    }

    for k, v in defaults.items():
        st.session_state.setdefault(k, v)
