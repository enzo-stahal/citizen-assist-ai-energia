"""Textos do assistente. Todos os números vêm de cenarios.comparar(): a resposta é consequência do cálculo."""
from __future__ import annotations

from . import calculos as c


def brl(v: float) -> str:
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-R$ " if v < -0.004 else "R$ ") + s


def num(v: float, casas: int = 0) -> str:
    s = f"{v:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def _payback(r) -> str:
    if r.payback_anos is None:
        return "não se paga em 10 anos"
    if r.payback_anos == 0:
        return "imediato (sem investimento)"
    meses = r.payback_anos * 12
    return f"~{num(meses)} meses" if meses < 24 else f"~{num(r.payback_anos, 1)} anos"


RODAPE = ("Estimativas, não garantias: dependem de tarifa, uso real, clima e regras. "
          "Digite 'limitações' ou 'referências' para ver as condições e as fontes.")


def linha_opcao(r) -> str:
    extra = ""
    if "kwp" in r.detalhes:
        extra = f" [{num(r.detalhes['kwp'], 2)} kWp, {r.detalhes['modulos']} placas]"
    return (f"- {r.nome}{extra}\n"
            f"    Investimento: {brl(r.investimento)} | Economia: ~{brl(r.economia_ano1_rs / 12)} por mês (~{brl(r.economia_ano1_rs)} no 1º ano)\n"
            f"    Se paga em: {_payback(r)} | Ganho líquido em 10 anos (VPL): {brl(r.vpl_rs)}\n"
            f"    CO₂ evitado no 1º ano: {num(r.co2_ano1_kg)} kg")


def resumo_comparacao(res: dict) -> str:
    p = res["premissas"]
    partes = [
        f"Consumo considerado: {num(res['consumo_mes'])} kWh/mês (~{brl(res['custo_mes'])}/mês a "
        f"{brl(p['tarifa_kwh'])}/kWh).",
        "Comparação no mesmo período de 10 anos "
        f"({int(p['ano_inicio'])}-{int(p['ano_inicio']) + int(p['horizonte_anos']) - 1}):",
    ]
    for k in ("A", "B", "C", "AB", "AC"):
        partes.append(linha_opcao(res[k]))
    partes.append(recomendacao(res))
    for n in res["notas"]:
        partes.append("Obs.: " + n)
    partes.append(RODAPE)
    return "\n".join(partes)


def recomendacao(res: dict) -> str:
    rec = res[res["recomendada"]]
    A = res["A"]
    txt = ["", "RECOMENDAÇÃO (para este perfil):",
           f"1) Comece pela eficiência (opção A): {brl(A.investimento)} se pagam em {_payback(A)}. "
           "É o passo de menor risco e ainda reduz o tamanho da solar necessária."]
    if res["recomendada"] == "AB":
        txt.append(f"2) Depois, solar própria dimensionada para o consumo reduzido ({_payback(res['AB'])} para a combinação A+B). "
                   "Peça 3 orçamentos e confira o Fio B da Enel SP.")
    else:
        motivo = ("imóvel alugado" if not res["proprietario"] else "capital disponível menor que o investimento da solar própria")
        txt.append(f"2) Como há restrição ({motivo}), considere solar por assinatura: sem investimento inicial, "
                   "economia menor e dependente do contrato.")
    if not res["proprietario"]:
        txt.append("ATENÇÃO: Se o imóvel é alugado, converse com o proprietário ANTES de qualquer alteração na instalação elétrica (painéis, medidor, quadro) e peça a autorização por escrito.")
    txt.append(f"Resultado combinado recomendado ({rec.nome}): ganho líquido em 10 anos ~{brl(rec.vpl_rs)} (VPL).")
    caras = [m for m in res["medidas"] if m.vpl_rs < 0]
    if caras:
        txt.append("Não compensa agora: " + "; ".join(m.nome[0].lower() + m.nome[1:] for m in caras) +
                   " (só vale se o equipamento atual estiver quebrando).")
    return "\n".join(txt)


def explicar_led(res: dict) -> str:
    m = next(x for x in res["medidas"] if x.chave == "M1")
    return (f"Trocar tubos fluorescentes por LED reduz a potência de ~70 W para ~35 W por luminária. "
            f"No perfil-exemplo isso evita ~{num(m.detalhes['kwh_mes_evitados'])} kWh/mês "
            f"(~{brl(m.economia_ano1_rs)} no 1º ano) e o investimento de {brl(m.investimento)} se paga em {_payback(m)}.\n"
            "Conta: kWh = quantidade × watts × horas/dia × dias ÷ 1000.\n" + RODAPE)


def explicar_refrigeracao(res: dict) -> str:
    m2 = next(x for x in res["medidas"] if x.chave == "M2")
    m3 = next(x for x in res["medidas"] if x.chave == "M3")
    return (f"Refrigeração é o maior consumo do mercadinho. Manutenção simples (borrachas, condensador limpo, termostato) "
            f"evita ~{num(m2.detalhes['kwh_mes_evitados'])} kWh/mês e se paga em {_payback(m2)}.\n"
            f"Trocar um expositor antigo por modelo eficiente custa ~{brl(m3.investimento)} e se paga em {_payback(m3)} "
            f"(VPL {brl(m3.vpl_rs)}): só compensa se o equipamento atual estiver no fim da vida. Nunca desligue a refrigeração "
            "de alimentos para economizar: o risco sanitário é maior que a economia.\n" + RODAPE)


def explicar_ar(res: dict) -> str:
    m4 = next(x for x in res["medidas"] if x.chave == "M4")
    return (f"Ar-condicionado inverter evita ~{num(m4.detalhes['kwh_mes_evitados'])} kWh/mês no perfil-exemplo; "
            f"custa ~{brl(m4.investimento)} e se paga em {_payback(m4)}. Antes de trocar, regule o termostato (23-24 °C), "
            "limpe os filtros e mantenha portas e janelas fechadas.\n" + RODAPE)


def explicar_solar(res: dict) -> str:
    B = res["B"]
    p = res["premissas"]
    return (f"Solar própria (on-grid): {num(B.detalhes['kwp'], 2)} kWp ({B.detalhes['modulos']} placas, "
            f"~{num(B.detalhes['area_necessaria_m2'])} m²) gera ~{num(B.detalhes['geracao_kwh_mes'])} kWh/mês. "
            f"Investimento ~{brl(B.investimento)}, economia no 1º ano ~{brl(B.economia_ano1_rs)}, "
            f"se paga em {_payback(B)}.\n"
            "Pela Lei 14.300, a energia injetada na rede paga parte do Fio B (75% em 2027, 90% em 2028). "
            f"Premissas importantes: {num(p['hsp_kwh_m2_dia'], 1)} kWh/m²/dia de sol e {int(p['autoconsumo_simultaneo'] * 100)}% da geração "
            "usada na hora. " + B.alertas[0] + "\n"
            + ("Se o imóvel é alugado, converse com o proprietário ANTES de qualquer alteração na instalação elétrica (painéis, medidor, quadro) e peça a autorização por escrito.\n" if not res["proprietario"] else "") + RODAPE)


def explicar_assinatura(res: dict) -> str:
    C = res["C"]
    p = res["premissas"]
    return (f"Solar por assinatura: sem instalar nada, você recebe créditos de uma usina compartilhada. "
            f"Com desconto de {int(p['desconto_assinatura'] * 100)}% (ESTIMADO), a economia no 1º ano seria ~{brl(C.economia_ano1_rs)}, "
            "sem investimento. Serve para quem aluga o ponto ou não tem telhado. Cuidado com fidelidade, multa e reajuste.\n"
            "Se o imóvel é alugado, converse com o proprietário ANTES de qualquer alteração na instalação elétrica (painéis, medidor, quadro) e peça a autorização por escrito.\n" + RODAPE)


def explicar_fio_b(res: dict) -> str:
    p = res["premissas"]
    pct = c.pct_fio_b(p, 2027)
    exemplo = 100 * p["fio_b_cheio_rs_kwh"] * pct
    return ("Pense no Fio B como um 'pedágio' pelo uso da rede da Enel. Com painéis solares, a energia que você produz e usa na hora "
            "não paga pedágio. Já a sobra, que vai para a rede e vira crédito, paga parte dele. Pela Lei 14.300/2022 (art. 27) essa parte é "
            "60% em 2026, 75% em 2027 e 90% em 2028.\n"
            f"Exemplo (estimativa): se seus painéis mandarem 100 kWh para a rede em 2027, você pagaria cerca de {brl(exemplo)} de pedágio "
            "sobre esses créditos. Por isso o ideal é usar o máximo da energia solar durante o dia, quando a loja está aberta.\n"
            "Depois de 2028 a ANEEL definirá a regra, então há incerteza. Quem pediu conexão até 7/1/2023 mantém a regra antiga até 2045.\n"
            + RODAPE)


def explicar_kwh() -> str:
    return ("kWh (quilowatt-hora) é a unidade que a conta de luz usa para medir quanto de energia você gastou. "
            "1 kWh é o que um aparelho de 1.000 W (como um ferro de passar) gasta ligado por 1 hora. "
            "Uma lâmpada LED de 35 W ligada 12 horas por dia gasta cerca de 0,42 kWh por dia (35 × 12 ÷ 1000).\n"
            "Na sua fatura, procure o 'consumo' em kWh do mês e o preço por kWh. Multiplicando um pelo outro, você chega ao valor da energia.\n"
            + RODAPE)


def explicar_co2(res: dict) -> str:
    p = res["premissas"]
    return (f"Usamos o fator médio do sistema elétrico brasileiro: {num(p['fator_emissao_kg_kwh'] * 1000, 1)} kg CO₂/MWh (MCTI, 2023). "
            "Como a matriz do Brasil já é majoritariamente renovável, cada kWh evitado poupa pouco CO₂ "
            f"(ex.: solar própria ~{num(res['B'].co2_ano1_kg)} kg/ano; eficiência A ~{num(res['A'].co2_ano1_kg)} kg/ano). "
            "O ganho principal dessas opções é econômico. Outros impactos: descarte correto de lâmpadas, painéis e gases de "
            "refrigeração antigos, e a energia de fabricação dos painéis, que não entra neste cálculo.\n" + RODAPE)


def limitacoes() -> str:
    return ("LIMITAÇÕES (leia antes de decidir):\n"
            "- Tarifa, custo por Wp, sol, desconto de assinatura e uso dos equipamentos são ESTIMADOS; veja data/premissas.json.\n"
            "- O perfil do mercadinho é um exemplo; seu consumo real pode ser bem diferente (use sua fatura).\n"
            "- A regra do Fio B após 2028 é incerta; a tarifa pode subir mais ou menos que 6% ao ano.\n"
            "- Não incluímos juros de financiamento, impostos sobre equipamentos, troca de inversor nem valor residual.\n"
            "- O que pode mudar a sua economia: reajustes da tarifa, mudança na regra do Fio B, condições do telhado (sombra, inclinação, área), "
            "quanto da energia solar você usa na hora, preço dos equipamentos e o uso real no seu comércio.\n"
            "- Solar on-grid não funciona durante queda de energia.\n"
            "- Não é projeto de engenharia nem aconselhamento financeiro: peça 3 orçamentos e um projeto técnico.\n"
            "- Valores são estimativas, não resultados garantidos.")


def referencias() -> str:
    return ("REFERÊNCIAS PRINCIPAIS (lista completa em docs/referencias.md):\n"
            "- Lei 14.300/2022, art. 27 (Fio B) - planalto.gov.br\n"
            "- Canal Solar: 'Consumidores passarão a arcar com 60% do Fio B a partir de 2026'\n"
            "- ANEEL/Exame: reajuste da Enel SP em 4/7/2026\n"
            "- Solfácil/Cenário Energia: preço médio R$ 2,45/Wp (1T/2026)\n"
            "- MCTI/SIRENE: fator de emissão do SIN (38,5 kg CO₂/MWh em 2023)\n"
            "- CRESESB SunData (irradiação) - a verificar pelo grupo")


AJUDA = ("Sou o assistente de energia do Citizen Assist AI para pequenos comércios (MEI). Posso ajudar com:\n"
         "- 'simular': calcula com o SEU consumo e compara as opções\n"
         "- 'comparar': mostra a comparação com o mercadinho-exemplo\n"
         "- 'led', 'geladeira', 'ar condicionado', 'solar', 'assinatura', 'fio b', 'kwh', 'co2'\n"
         "- 'limitações' e 'referências'\n"
         "- 'sair'")
