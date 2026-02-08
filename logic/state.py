import streamlit as st
def init_state():
    if "operacoes_ativas" not in st.session_state:
        st.session_state.operacoes_ativas = ["+", "-", "*"]

    if "a" not in st.session_state:
        st.session_state.a = None
    if "b" not in st.session_state:
        st.session_state.b = None
    if "operacao" not in st.session_state:
        st.session_state.operacao = None
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
