import streamlit as st
from i18n.texts import TEXTS
from logic.state import init_state
from logic.exercises import gerar_exercicio
from logic.stats import calcular_estatisticas
from ui.layout import titulo, configuracoes, historico, estatisticas, erro
from ui.settings import selecionar_operacoes

st.set_page_config(page_title="Gerador Educacional", page_icon="📘")

init_state()
T = TEXTS[st.session_state.lang]

# 🔑 GERA EXERCÍCIO ANTES DA UI
if st.session_state.novo_exercicio:
    gerar_exercicio(T, st.session_state.lang)
    st.session_state.novo_exercicio = False

# ---------------- UI ----------------
titulo(T)
configuracoes(T)
selecionar_operacoes(T)

a, b, op = st.session_state.a, st.session_state.b, st.session_state.operacao
symbol = "²" if op == "^" and b == 2 else op

st.subheader(f"{T['exercise']}: {a} {symbol} {b if op != '^' else ''}")

resposta = st.text_input(T["input"], key="resposta")

if st.button(T["check"], use_container_width=True):
    try:
        resposta = int(resposta)
    except:
        st.warning(T["only_numbers"])
        st.stop()

    correto = resposta == st.session_state.resultado

    registro = {
        "a": a,
        "b": b,
        "operacao": op,
        "resultado": st.session_state.resultado,
        "correto":correto,
        "explicacao": st.session_state.explicacao,
    }

    if correto:
        st.success(T["correct"])
        st.session_state.acertos += 1

        if st.session_state.modo_correcao:
            st.session_state.erros.pop(0)
    else:
        st.error(T["wrong"])
        st.info(st.session_state.explicacao)
        st.session_state.erros.append(registro)

    st.session_state.historico.append(registro)
    st.session_state.novo_exercicio = True
    st.rerun()

erro(T)

stats = calcular_estatisticas(st.session_state.historico)
estatisticas(T, stats)
historico(T)
