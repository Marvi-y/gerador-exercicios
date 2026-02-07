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
