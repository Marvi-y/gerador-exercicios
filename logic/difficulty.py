import streamlit as st
def dificuldade_por_nivel(nivel, lang):
    if nivel == 1:
        return "Fácil" if lang == "pt" else "Easy"
    elif nivel == 2:
        return "Médio" if lang == "pt" else "Medium"
    else:
        return "Difícil" if lang == "pt" else "Hard"
