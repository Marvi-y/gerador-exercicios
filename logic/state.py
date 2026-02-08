import streamlit as st

def init_state():
    defaults = {
        "nivel": 1,
        "acertos": 0,
        "historico": [],
        "erros": [],
        "modo_treino_erros": False,
        "dificuldade_manual": None,

        # exercício atual
        "a": None,
        "b": None,
        "operacao": None,
        "resultado": None,
        "explicacao": None,

        # configurações do usuário
        "operacoes_ativas": ["+", "-", "*"],
        "precisa_novo_exercicio": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
