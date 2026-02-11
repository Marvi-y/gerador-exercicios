from collections import Counter

def calcular_estatisticas(historico):
    if not historico:
        return None

    total = len(historico)
    acertos = sum(1 for h in historico if h.get("correto"))
    erros = total - acertos

    taxa_acerto = round((acertos / total) * 100, 1)

    operacoes = [
    h["operacao"]
    for h in historico
    if not h.get("correto")
    ]

    erros_por_operacao = Counter(operacoes)

    return {
        "total": total,
        "acertos": acertos,
        "erros": erros,
        "taxa_acerto": taxa_acerto,
        "erros_por_operacao": erros_por_operacao
    }
