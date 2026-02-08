import streamlit as st

def titulo(T):
    st.title(T["title"])
    st.write(T["subtitle"])


def configuracoes(T):
    st.subheader(T["settings"])
    opcao = st.selectbox(
        T["choose_difficulty"],
        [T["auto"], T["easy"], T["medium"], T["hard"]]
    )
    st.session_state.dificuldade_manual = None if opcao == T["auto"] else opcao


def historico(T):
    st.divider()
    st.subheader(T["history"])

    if not st.session_state.historico:
        st.write(T["no_history"])
        return

    for item in reversed(st.session_state.historico):
        if item["correto"]:
            st.success(f"✅ {item['expressao']} = {item['resposta_correta']}")
        else:
            st.error(f"❌ {item['expressao']} = {item['resposta_correta']}")