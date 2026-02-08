import streamlit as st

from i18n.texts import TEXTS
from logic.state import init_state
from logic.exercises import gerar_exercicio
from logic.stats import calcular_estatisticas
from ui.layout import titulo, configuracoes, historico, estatisticas
from ui.settings import selecionar_operacoes

# =============================
# CONFIGURAÇÃO DA PÁGINA
# =============================
st.set_page_config(
    page_title="Gerador Educacional",
    page_icon="📘",
    layout="centered"
)

# =============================
# ESTADO GLOBAL
# =============================
init_state()

# =============================
# IDIOMA
# =============================
if "lang" not in st.session_state:
    st.session_state.lang = "pt"

st.session_state.lang = st.selectbox(
    "🌐 Language / Idioma",
    ["pt", "en"],
    format_func=lambda x: "Português 🇧🇷" if x == "pt" else "English 🇺🇸"
)

T = TEXTS[st.session_state.lang]

# =============================
# TOPO / CONFIGURAÇÕES
# =============================
titulo(T)
configuracoes(T)
selecionar_operacoes(T)

# =============================
# CONTROLE CENTRAL DO EXERCÍCIO
# =============================
if (
    st.session_state.operacao is None
    or st.session_state.precisa_novo_exercicio
):
    gerar_exercicio(T, st.session_state.lang)
    st.session_state.precisa_novo_exercicio = False

# =============================
# EXERCÍCIO ATUAL (RENDER)
# =============================
a = st.session_state.a
b = st.session_state.b
op = st.session_state.operacao

symbol = "²" if op == "^" and b == 2 else op

st.subheader(
    f"{T['exercise']}: {a} {symbol} {b if op != '^' else ''}"
)

# =============================
# RESPOSTA DO USUÁRIO
# =============================
resposta = st.text_input(
    T["input"],
    placeholder=T["placeholder"]
)

# =============================
# VERIFICAR RESPOSTA
# =============================
if st.button(T["check"], use_container_width=True):
    try:
        resposta_int = int(resposta)
    except:
        st.warning(T["only_numbers"])
        st.stop()

    correto = resposta_int == st.session_state.resultado

    st.session_state.historico.append({
        "expressao": f"{a} {op} {b}",
        "resposta_usuario": resposta_int,
        "resposta_correta": st.session_state.resultado,
        "correto": correto
    })

    if correto:
        st.success(T["correct"])
    else:
        st.error(T["wrong"])
        st.info(st.session_state.explicacao)

    # pede novo exercício (sem gerar aqui)
    st.session_state.precisa_novo_exercicio = True

# =============================
# NOVO EXERCÍCIO (MANUAL)
# =============================
if st.button(T["new"], use_container_width=True):
    st.session_state.precisa_novo_exercicio = True

# =============================
# ESTATÍSTICAS
# =============================
stats = calcular_estatisticas(st.session_state.historico)
estatisticas(T, stats)

# =============================
# HISTÓRICO
# =============================
historico(T)
