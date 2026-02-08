import streamlit as st
import random
from texts import TEXTS

# =============================
# CONFIGURAÇÃO
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
# FUNÇÕES AUXILIARES
# =============================
def dificuldade_por_nivel(nivel):
    if nivel == 1:
        return "Fácil" if st.session_state.lang == "pt" else "Easy"
    elif nivel == 2:
        return "Médio" if st.session_state.lang == "pt" else "Medium"
    else:
        return "Difícil" if st.session_state.lang == "pt" else "Hard"


def gerar_exercicio():
    if st.session_state.modo_treino_erros and st.session_state.erros:
        erro = random.choice(st.session_state.erros)
        st.session_state.update(erro)
        return

    dificuldade = (
        st.session_state.dificuldade_manual
        or dificuldade_por_nivel(st.session_state.nivel)
    )

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

    st.session_state.update({
        "a": a,
        "b": b,
        "operacao": operacao,
        "resultado": resultado,
        "explicacao": explicacao
    })

# =============================
# ESTADO INICIAL
# =============================
for key, default in {
    "nivel": 1,
    "acertos": 0,
    "historico": [],
    "erros": [],
    "modo_treino_erros": False,
    "dificuldade_manual": None,
    "a": None
}.items():
    st.session_state.setdefault(key, default)

if st.session_state.a is None:
    gerar_exercicio()

# =============================
# INTERFACE
# =============================
st.title(T["title"])
st.write(T["subtitle"])

st.subheader(T["settings"])
opcao = st.selectbox(
    T["choose_difficulty"],
    [T["auto"], T["easy"], T["medium"], T["hard"]]
)


st.session_state.dificuldade_manual = (
    None if opcao == T["auto"] else opcao
)


st.subheader(f"🏆 {T['level']} {st.session_state.nivel}")
st.write(
    f"{T['difficulty']}: **{st.session_state.dificuldade_manual or dificuldade_por_nivel(st.session_state.nivel)}**"
)
st.write(f"🔥 {T['streak']}: {st.session_state.acertos}/3")

if st.session_state.erros:
    st.button(T["train_errors"])
    st.session_state.modo_treino_erros = True
    gerar_exercicio()
if st.session_state.modo_treino_erros:
if st.button(T["back_normal"]):
st.session_state.modo_treino_erros = False
gerar_exercicio()
st.subheader(
    f"{T['exercise']}: {st.session_state.a} "
    f"{st.session_state.operacao} {st.session_state.b}"
)

resposta = st.text_input(T["input"], placeholder=T["placeholder"])

# =============================
# VERIFICAÇÃO
# =============================
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
        st.session_state.acertos += 1

        if st.session_state.modo_treino_erros:
            st.session_state.erros = [
                e for e in st.session_state.erros
                if not (
                    e["a"] == st.session_state.a and
                    e["b"] == st.session_state.b and
                    e["operacao"] == st.session_state.operacao
                )
            ]

        if st.session_state.acertos >= 3:
            st.session_state.nivel = min(3, st.session_state.nivel + 1)
            st.session_state.acertos = 0
            st.success(T["unlock"])

    else:
        st.error(T["wrong"])
        st.info(st.session_state.explicacao)
        st.session_state.acertos = 0

        st.session_state.erros.append({
            "a": st.session_state.a,
            "b": st.session_state.b,
            "operacao": st.session_state.operacao,
            "resultado": st.session_state.resultado,
            "explicacao": st.session_state.explicacao
        })

    gerar_exercicio()

if st.button(T["new"], use_container_width=True):
    gerar_exercicio()

# =============================
# HISTÓRICO
# =============================
st.divider()
st.subheader(T["history"])


if not st.session_state.historico:
    st.write(T["no_history"])
else:
    for item in reversed(st.session_state.historico):
        if item["correto"]:
            st.success(f"✅ {item['expressao']} = {item['resposta_correta']}")
        else:
            st.error(f"❌ {item['expressao']} = {item['resposta_correta']}")
