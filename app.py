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

if st.session_state.etapa == "responder":

    if st.button(T["check"], use_container_width=True):

        try:
            resposta_int = int(resposta)
        except:
            st.warning(T["only_numbers"])
            st.stop()

        correto = resposta_int == st.session_state.resultado

        registro = {
            "a": a,
            "b": b,
            "operacao": op,
            "resposta_usuario": resposta_int,
            "correto": correto,
        }

        st.session_state.historico.append(registro)

        if correto:
            st.session_state.acertos += 1
            st.session_state.feedback_tipo = "correct"

            if st.session_state.modo_correcao and st.session_state.erros:
                st.session_state.erros.pop(0)
        else:
            st.session_state.feedback_tipo = "wrong"
            st.session_state.erros.append(registro)

        st.session_state.etapa = "feedback"
        st.rerun()
    
   if st.session_state.etapa == "feedback":

      if st.session_state.feedback_tipo == "correct":
         st.success(T["correct"])
      else:
         st.error(T["wrong"])
         st.info(st.session_state.explicacao)

    if st.button(T["new"], use_container_width=True):
        st.session_state.etapa = "responder"
        st.session_state.novo_exercicio = True
        st.rerun()
        
    st.session_state.historico.append(registro)
    
    if correto:
        st.session_state.feedback_tipo = "correct"

        if st.session_state.modo_correcao:
            if st.session_state.erros:
                st.session_state.erros.pop(0)

        else:
            st.session_state.feedback_tipo = "wrong"
            st.session_state.erros.append(registro)

    st.session_state.mostrar_feedback = True
    st.rerun()

    if st.session_state.mostrar_feedback:

        if st.session_state.feedback_tipo == "correct":
            st.success(T["correct"])

        elif st.session_state.feedback_tipo == "wrong":
            st.error(T["wrong"])
            st.info(st.session_state.explicacao)

    # prepara próximo exercício
    st.session_state.mostrar_feedback = False
    st.session_state.novo_exercicio = True
    st.rerun()

    st.divider()

if st.button(T["new"], use_container_width=True):
    st.session_state.novo_exercicio = True
    st.rerun()

erro(T)

stats = calcular_estatisticas(st.session_state.historico)
estatisticas(T, stats)
historico(T)
