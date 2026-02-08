import streamlit as st
from i18n.texts import TEXTS
from logic.state import init_state
from logic.exercises import gerar_exercicio, dificuldade_por_nivel
from ui.layout import titulo, configuracoes, historico
from logic.stats import calcular_estatisticas
from ui.layout import estatisticas

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

if st.session_state.a is None:
    gerar_exercicio(T, st.session_state.lang)

titulo(T)
configuracoes(T)

st.subheader(
    f"{T['exercise']}: {st.session_state.a} "
    f"{st.session_state.operacao} {st.session_state.b}"
)

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
