import streamlit as st

def selecionar_operacoes(T):
    st.subheader(T["operations"])

    ops = {
        "+": T["op_sum"],
        "-": T["op_sub"],
        "*": T["op_mul"],
        "/": T["op_div"],
        "^": T["op_pow"],
    }

    selecionadas = []

    for simbolo, label in ops.items():
        if st.checkbox(label, value=simbolo in st.session_state.operacoes_ativas):
            selecionadas.append(simbolo)

    if not selecionadas:
        st.warning(T["select_one_op"])
    else:
        st.session_state.operacoes_ativas = selecionadas