import streamlit as st

def init_state():
    defaults = {
        "lang": "pt",

        # progresso
        "nivel": 1,
        "acertos": 0,
        "historico": [],
        "erros": [],
        "mostrar_feedback": False,
        "feedback_tipo": None,
        "etapa": "responder",

        # modos
        "modo_correcao": False,

        # dificuldade
        "dificuldade_manual": None,

        # exercício atual
        "a": None,
        "b": None,
        "operacao": None,
        "resultado": None,
        "explicacao": None,

        # controle
        "operacoes_ativas": ["+", "-", "*"],
        "novo_exercicio": True,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
