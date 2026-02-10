import streamlit as st 

def init_state():
    defaults = {
        "a": None,
        "b": None,
        "operacao": None,
        "resultado": None,
        "explicacao": None,
        "historico": [],
        "operacoes_ativas": ["+", "-", "*"],
        "lang": "pt",
    }
    
for k, v in defaults.items():
    st.session_state.setdefault(k, v)
