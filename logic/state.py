import streamlit as st

def init_state():
    defaults = {
        "nivel": 1,
        "acertos": 0,
        "historico": [],
        "erros": [],
        "modo_treino_erros": False,
        "dificuldade_manual": None,
        "a": None
    }

    for key, value in defaults.items():
        st.session_state.setdefault(key, value)