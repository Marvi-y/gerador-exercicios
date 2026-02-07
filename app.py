import streamlit as st
import random
from texts import TEXTS

# =============================
# CONFIGURAÇÃO DA PÁGINA
# =============================
st.set_page_config(
    page_title="Gerador Educacional",
    page_icon="📘",
    layout="centered"
)

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
# TÍTULO
# =============================
st.title(T["title"])
st.write(T["subtitle"])

# =============================
# INICIALIZA ESTADOS
# =============================
if "nivel" not in st.session_state:
    st.session_state.nivel = 1
    st.session_state.acertos = 0
    st.session_state.a = None
    st.session_state.b = None
    st.session_state.operacao = None
    st.session_state.resultado = None
    st.session_state.explicacao = None

# =============================
# FUNÇÕES
# =============================
def dificuldade_por_nivel(nivel):
    if nivel == 1:
        return "Easy" if st.session_state.lang == "en" else "Fácil"
    elif nivel == 2:
        return "Medium" if st.session_state.lang == "en" else "Médio"
    else:
        return "Hard" if st.session_state.lang == "en" else "Difícil"

def gerar_exercicio():
    dificuldade = dificuldade_por_nivel(st.session_state.nivel)

    if dificuldade in ["Fácil", "Easy"]:
        minimo, maximo = 1, 10
    elif dificuldade in ["Médio", "Medium"]:
        minimo, maximo = 10, 50
    else:
        minimo, maximo = 50, 100

    a = random.randint(minimo, maximo)
    b = random.randint(minimo, maximo)
    operacao = random.choice(["+", "-", "*"])

    if operacao == "+":
        resultado = a + b
        explicacao = T["tip_sum"]
    elif operacao == "-":
        resultado = a - b
        explicacao = T["tip_sub"]
    else:
        resultado = a * b
        explicacao = T["tip_mul"]

    st.session_state.a = a
    st.session_state.b = b
    st.session_state.operacao = operacao
    st.session_state.resultado = resultado
    st.session_state.explicacao = explicacao

# =============================
# GERAR EXERCÍCIO INICIAL
# =============================
if st.session_state.a is None:
    gerar_exercicio()

# =============================
# INTERFACE
# =============================
st.subheader(f"🏆 {T['level']} {st.session_state.nivel}")
st.write(f"{T['difficulty']}: **{dificuldade_por_nivel(st.session_state.nivel)}**")
st.write(f"🔥 {T['streak']}: {st.session_state.acertos}/3")

st.subheader(
    f"{T['exercise']}: "
    f"{st.session_state.a} "
    f"{st.session_state.operacao} "
    f"{st.session_state.b}"
)

resposta = st.text_input(
    T["input"],
    placeholder=T["placeholder"]
)

# =============================
# VERIFICAÇÃO
# =============================
if st.button(T["check"], use_container_width=True):
    try:
        resposta = int(resposta)
    except:
        st.warning(T["only_numbers"])
        st.stop()

    if resposta == st.session_state.resultado:
        st.success(T["correct"])
        st.session_state.acertos += 1

        if st.session_state.acertos >= 3:
            if st.session_state.nivel < 3:
                st.session_state.nivel += 1
                st.session_state.acertos = 0
                st.success(T["unlock"])
            else:
                st.balloons()

        gerar_exercicio()

    else:
        st.error(T["wrong"])
        st.info(st.session_state.explicacao)
        st.session_state.acertos = 0

if st.button(T["new"], use_container_width=True):
    gerar_exercicio()
