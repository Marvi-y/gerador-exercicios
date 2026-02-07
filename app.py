import streamlit as st
import random

st.set_page_config(page_title="Gerador Educacional", page_icon="📘", layout="centered")

st.title("📘 Plataforma de Exercícios Matemáticos")
st.write("Aprenda no seu ritmo. Evolua com mérito.")

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
        return "Fácil"
    elif nivel == 2:
        return "Médio"
    else:
        return "Difícil"

def gerar_exercicio():
    dificuldade = dificuldade_por_nivel(st.session_state.nivel)

    if dificuldade == "Fácil":
        minimo, maximo = 1, 10
    elif dificuldade == "Médio":
        minimo, maximo = 10, 50
    else:
        minimo, maximo = 50, 100

    a = random.randint(minimo, maximo)
    b = random.randint(minimo, maximo)
    operacao = random.choice(["+", "-", "*"])

    if operacao == "+":
        resultado = a + b
        explicacao = f"💡 Dica: somar é juntar valores: {a} + {b} = {resultado}"
    elif operacao == "-":
        resultado = a - b
        explicacao = f"💡 Dica: subtrair é tirar uma quantidade da outra: {a} - {b} = {resultado}"
    else:
        resultado = a * b
        explicacao = "💡 Dica: multiplicar é somar várias vezes"

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
st.subheader(f"🏆 Nível {st.session_state.nivel}")
st.write(f"Dificuldade: **{dificuldade_por_nivel(st.session_state.nivel)}**")
st.write(f"🔥 Acertos consecutivos: {st.session_state.acertos}/3")

st.subheader(
    f"✏️ Exercício: {st.session_state.a} "
    f"{st.session_state.operacao} "
    f"{st.session_state.b}"
)

resposta = st.text_input(
    "✏️ Digite sua resposta",
    placeholder="Ex: 42"
)


if st.button("Verificar"):
    try:
        resposta = int(resposta)
    except:
        st.warning("Digite apenas números")
        st.stop()

    if resposta == st.session_state.resultado:
        st.success("✅ Correto! Você está evoluindo!")
        st.session_state.acertos += 1

        # DESBLOQUEIO DE NÍVEL
        if st.session_state.acertos >= 3:
            if st.session_state.nivel < 3:
                st.session_state.nivel += 1
                st.session_state.acertos = 0
                st.success("🎉 Novo nível desbloqueado!")
            else:
                st.balloons()

        gerar_exercicio()

    else:
        st.error("❌ Tente novamente")
        st.info(st.session_state.explicacao)
        st.session_state.acertos = 0

if st.button("🔄 Novo exercício"):
    gerar_exercicio()
    
