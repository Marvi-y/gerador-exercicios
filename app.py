import streamlit as st
from i18n.texts import TEXTS
from logic.state import init_state
from logic.exercises import gerar_exercicio
from logic.stats import calcular_estatisticas
from ui.layout import titulo, configuracoes, historico, estatisticas
from ui.settings import selecionar_operacoes

st.set_page_config(page_title="Gerador Educacional", page_icon="📘")

# idioma
if "lang" not in st.session_state:
    st.session_state.lang = "pt"

st.session_state.lang = st.selectbox(
    "🌐 Language / Idioma",
    ["pt", "en"],
    format_func=lambda x: "Português 🇧🇷" if x == "pt" else "English 🇺🇸"
)

T = TEXTS[st.session_state.lang]

# estado
init_state()

# 🔑 gera exercício ANTES de mostrar qualquer coisa
if st.session_state.novo_exercicio:
    gerar_exercicio(T, st.session_state.lang)
    st.session_state.novo_exercicio = False

# ---------------- UI ----------------
titulo(T)
configuracoes(T)
selecionar_operacoes(T)

a = st.session_state.a
b = st.session_state.b
op = st.session_state.operacao

symbol = "²" if op == "^" and b == 2 else op

st.subheader(
    f"{T['exercise']}: {a} {symbol} {b if op != '^' else ''}"
)

# 🔒 FORM resolve ENTER + estado quebrado
with st.form("resposta_form", clear_on_submit=True):
    resposta = st.text_input(T["input"])
    submitted = st.form_submit_button(T["check"])

if submitted:
    try:
        resposta = int(resposta)
    except:
        st.warning(T["only_numbers"])
        st.stop()

    correto = resposta == st.session_state.resultado

    st.session_state.historico.append({
        "expressao": f"{a} {op} {b}",
        "resposta_usuario": resposta,
        "resposta_correta": st.session_state.resultado,
        "correto": correto
    })

    if correto:
        st.success(T["correct"])
    else:
        st.error(T["wrong"])
        st.info(st.session_state.explicacao)

    st.session_state.novo_exercicio = True
    st.rerun()

if st.button(T["new"], use_container_width=True):
    st.session_state.novo_exercicio = True
    st.rerun()

stats = calcular_estatisticas(st.session_state.historico)
estatisticas(T, stats)
historico(T)
