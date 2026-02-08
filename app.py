
import streamlit as st
from i18n.texts import TEXTS
from logic.state import init_state
from logic.difficulty import dificuldade_por_nivel
from ui.layout import titulo, configuracoes, historico
from logic.stats import calcular_estatisticas
from ui.layout import estatisticas
from logic.exercises import gerar_exercicio
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

init_state()

def init_state():
    if "operacoes_ativas" not in st.session_state:
        st.session_state.operacoes_ativas = ["+", "-", "*"]

    if "a" not in st.session_state:
        st.session_state.a = None
    if "b" not in st.session_state:
        st.session_state.b = None
    if "operacao" not in st.session_state:
        st.session_state.operacao = None
    

titulo(T)
configuracoes(T)
selecionar_operacoes(T)
if st.session_state.a is None:
    gerar_exercicio(T, st.session_state.lang)
    op = st.session_state.operacao
symbol = "²" if op == "^" and st.session_state.b == 2 else op

resposta = st.text_input(T["input"], placeholder=T["placeholder"])

if st.button(T["check"], use_container_width=True):
    try:
        resposta = int(resposta)
    except:
        st.warning(T["only_numbers"])
        st.stop()

    correto = resposta == st.session_state.resultado

    st.session_state.historico.append({
        "expressao": f"{st.session_state.a} {st.session_state.operacao} {st.session_state.b}",
        "resposta_usuario": resposta,
        "resposta_correta": st.session_state.resultado,
        "correto": correto
    })

    if correto:
        st.success(T["correct"])
    else:
        st.error(T["wrong"])
        st.info(st.session_state.explicacao)

    gerar_exercicio(T, st.session_state.lang)

if st.button(T["new"], use_container_width=True):
    gerar_exercicio(T, st.session_state.lang)

stats = calcular_estatisticas(st.session_state.historico)
estatisticas(T, stats)

historico(T)
