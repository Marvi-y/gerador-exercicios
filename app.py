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
if "historico" not in st.session_state:
    st.session_state.historico = []
if "nivel" not in st.session_state:
    st.session_state.nivel = 1
    st.session_state.acertos = 0
    st.session_state.a = None
    st.session_state.b = None
    st.session_state.operacao = None
    st.session_state.resultado = None
    st.session_state.explicacao = None
if "erros" not in st.session_state:
    st.session_state.erros = []

if "modo_treino_erros" not in st.session_state:
    st.session_state.modo_treino_erros = False
if "dificuldade_manual" not in st.session_state:
    st.session_state.dificuldade_manual = None


# =============================
# FUNÇÕES
# =============================
def gerar_exercicio():
    if st.session_state.dificuldade_manual:
        dificuldade = st.session_state.dificuldade_manual
    else:
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

    st.session_state.update({
        "a": a,
        "b": b,
        "operacao": operacao,
        "resultado": resultado,
        "explicacao": explicacao
    })


# =============================
# GERAR EXERCÍCIO INICIAL
# =============================
if st.session_state.a is None:
    gerar_exercicio()

# =============================
# INTERFACE
# =============================
st.subheader("⚙️ Configurações")

opcao = st.selectbox(
    "Escolha a dificuldade (ou deixe automático)",
    ["Automático", "Fácil", "Médio", "Difícil"]
)

if opcao == "Automático":
    st.session_state.dificuldade_manual = None
else:
    st.session_state.dificuldade_manual = opcao

st.subheader(f"🏆 {T['level']} {st.session_state.nivel}")
st.write(f"{T['difficulty']}: **{dificuldade_por_nivel(st.session_state.nivel)}**")
st.write(f"🔥 {T['streak']}: {st.session_state.acertos}/3")
if st.session_state.erros:
    if st.button("🔁 Treinar exercícios errados"):
        st.session_state.modo_treino_erros = True
        erro = random.choice(st.session_state.erros)


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
        st.session_state.historico.append({
        "expressao": f"{st.session_state.a} {st.session_state.operacao} {st.session_state.b}",
        "resposta_usuario": resposta,
        "resposta_correta": st.session_state.resultado,
        "correto": True
        })

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
        st.session_state.historico.append({
        "expressao": f"{st.session_state.a} {st.session_state.operacao} {st.session_state.b}",
        "resposta_usuario": resposta,
        "resposta_correta": st.session_state.resultado,
        "correto": False
        })
if st.session_state.modo_treino_erros:
    if st.button("⬅️ Voltar ao modo normal"):
        st.session_state.modo_treino_erros = False
        gerar_exercicio()

 
if st.button(T["new"], use_container_width=True):
    gerar_exercicio()
st.divider()
st.subheader("📊 Histórico de respostas")

if not st.session_state.historico:
    st.write("Nenhum exercício resolvido ainda.")
else:
    for item in reversed(st.session_state.historico):
        if item["correto"]:
            st.success(
                f"✅ {item['expressao']} = {item['resposta_correta']} "
                f"(Você respondeu {item['resposta_usuario']})"
            )
        if st.session_state.modo_treino_erros:
            st.session_state.erros = [
                e for e in st.session_state.erros
                if not (
                    e["a"] == st.session_state.a and
                    e["b"] == st.session_state.b and
                    e["operacao"] == st.session_state.operacao
                )
            ]

        else:
            st.error(
                f"❌ {item['expressao']} = {item['resposta_correta']} "
                f"(Você respondeu {item['resposta_usuario']})"
            )
            st.session_state.erros.append({
                "a": st.session_state.a,
                "b": st.session_state.b,
                "operacao": st.session_state.operacao,
                "resultado": st.session_state.resultado,
                "explicacao": st.session_state.explicacao
                })


