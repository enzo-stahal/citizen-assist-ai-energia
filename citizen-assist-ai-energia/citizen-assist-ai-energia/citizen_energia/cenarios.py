"""Alternativas para o mesmo problema: reduzir/atender o consumo de um pequeno comércio.

A  = Eficiência energética de baixo custo (LED + manutenção da refrigeração)
B  = Solar fotovoltaica própria (on-grid, Lei 14.300)
C  = Energia solar por assinatura (geração distribuída compartilhada)
AB = A + B (solar dimensionada para o consumo já reduzido)
AC = A + C
Todas comparadas no mesmo horizonte (padrão: 10 anos) e mesma necessidade.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import calculos as c
from . import dados


@dataclass
class Resultado:
    chave: str
    nome: str
    investimento: float
    economia_ano1_rs: float
    energia_ano1_kwh: float          # kWh evitados (eficiencia) ou gerados/creditados (solar)
    fluxos: list[float]
    payback_anos: float | None
    vpl_rs: float
    co2_ano1_kg: float
    detalhes: dict = field(default_factory=dict)
    alertas: list[str] = field(default_factory=list)


def _fechar(chave, nome, fluxos, energia_ano1, p, detalhes=None, alertas=None) -> Resultado:
    return Resultado(
        chave=chave,
        nome=nome,
        investimento=max(-fluxos[0], 0.0) + 0.0,   # +0.0 evita "-0,00"
        economia_ano1_rs=fluxos[1],
        energia_ano1_kwh=energia_ano1,
        fluxos=fluxos,
        payback_anos=c.payback_anos(fluxos),
        vpl_rs=c.vpl(fluxos, p["taxa_desconto"]),
        co2_ano1_kg=c.co2_evitado_kg(energia_ano1, p),
        detalhes=detalhes or {},
        alertas=alertas or [],
    )


# ---------- Eficiencia ----------
def avaliar_medida(m: dict, consumos: dict[str, float], p: dict, fator_custo: float = 1.0) -> Resultado:
    H = int(p["horizonte_anos"])
    base_kwh_mes = sum(consumos[a] for a in m["alvos"]) * m["fracao_alvo"]
    kwh_mes = base_kwh_mes * m["economia_pct"]
    custo = m["custo_inicial_rs"] * fator_custo
    fluxos = [-custo]
    for t in range(1, H + 1):
        f = kwh_mes * 12 * c.tarifa_no_ano(p, t) - m["custo_anual_rs"] * fator_custo
        if t % int(m["vida_util_anos"]) == 0 and t < H:   # reposicao ao fim da vida util
            f -= custo
        fluxos.append(f)
    return _fechar(m["id"], m["nome"], fluxos, kwh_mes * 12, p,
                   detalhes={"kwh_mes_evitados": kwh_mes, "consumo_alvo_kwh_mes": base_kwh_mes})


def somar(chave: str, nome: str, itens: list[Resultado], p: dict, alertas=None) -> Resultado:
    n = len(itens[0].fluxos)
    fluxos = [sum(i.fluxos[t] for i in itens) for t in range(n)]
    det = {"kwh_mes_evitados": sum(i.detalhes.get("kwh_mes_evitados", 0) for i in itens)}
    for i in itens:
        det.update({k: v for k, v in i.detalhes.items() if k != "kwh_mes_evitados"})
    r = _fechar(chave, nome, fluxos, sum(i.energia_ano1_kwh for i in itens), p, det, alertas)
    for i in itens:
        for a in i.alertas:
            if a not in r.alertas:
                r.alertas.append(a)
    return r


# ---------- Solar propria ----------
def avaliar_fv(consumo_mes: float, p: dict, proprietario: bool = True,
               area_m2: float | None = None, capital: float | None = None,
               chave: str = "B", nome: str = "Solar fotovoltaica própria") -> Resultado:
    H = int(p["horizonte_anos"])
    dim = c.dimensionar_fv(consumo_mes, p, area_m2)
    kwp = dim["kwp"]
    ger_mes_ano1 = kwp * c.geracao_kwh_mes_por_kwp(p)
    capex = kwp * 1000 * p["custo_fv_rs_wp"]
    fluxos = [-capex]
    for t in range(1, H + 1):
        ger_t = ger_mes_ano1 * 12 * (1 - p["degradacao_fv_ano"]) ** (t - 1)
        ano = int(p["ano_inicio"]) + t - 1
        fio_b_t = p["fio_b_cheio_rs_kwh"] * (1 + p["reajuste_tarifa"]) ** (t - 1) * c.pct_fio_b(p, ano)
        compensada = ger_t * (1 - p["autoconsumo_simultaneo"])
        fluxos.append(ger_t * c.tarifa_no_ano(p, t) - compensada * fio_b_t - capex * p["om_fv_pct_capex_ano"])
    alertas = ["Sistema on-grid desliga durante queda de energia da rede (não serve como backup)."]
    if dim["limitado_por_area"]:
        alertas.append("A área de telhado limita a potência: a solar não cobre todo o consumo desejado.")
    if not proprietario:
        alertas.append("Imóvel alugado: precisa de autorização do proprietário e contrato longo o bastante para recuperar o investimento.")
    if capital is not None and capex > capital:
        alertas.append("Investimento maior que o capital disponível: exigiria financiamento (juros NÃO incluídos no cálculo).")
    r = _fechar(chave, nome, fluxos, ger_mes_ano1 * 12, p,
                detalhes={"kwp": kwp, "modulos": dim["modulos"], "area_necessaria_m2": dim["area_necessaria_m2"],
                          "geracao_kwh_mes": ger_mes_ano1}, alertas=alertas)
    return r


# ---------- Solar por assinatura ----------
def avaliar_assinatura(consumo_mes: float, p: dict, chave: str = "C",
                       nome: str = "Solar por assinatura") -> Resultado:
    H = int(p["horizonte_anos"])
    creditos_mes = max(consumo_mes - p["disponibilidade_kwh"], 0.0) * p["cobertura_assinatura"]
    fluxos = [0.0] + [creditos_mes * 12 * c.tarifa_no_ano(p, t) * p["desconto_assinatura"] for t in range(1, H + 1)]
    alertas = ["Verifique multa de cancelamento, prazo de fidelidade, reajuste do contrato e se o desconto já inclui o Fio B.",
               "O cliente continua pagando a taxa mínima (custo de disponibilidade) e a iluminação pública."]
    return _fechar(chave, nome, fluxos, creditos_mes * 12, p,
                   detalhes={"creditos_kwh_mes": creditos_mes}, alertas=alertas)


# ---------- Comparacao completa ----------
def comparar(consumo_mes: float | None = None, tarifa: float | None = None,
             proprietario: bool = True, area_m2: float | None = None,
             capital: float | None = None, p: dict | None = None) -> dict:
    """Compara as alternativas. Se consumo_mes for None usa o perfil-exemplo (mercadinho)."""
    p = dict(p or dados.premissas())
    if tarifa is not None:
        p["tarifa_kwh"] = tarifa
    equips = dados.equipamentos()
    meds = {m["id"]: m for m in dados.medidas()}
    consumos = c.consumo_por_id(equips)
    total_perfil = sum(consumos.values())

    escala = 1.0
    notas = []
    if consumo_mes is not None and consumo_mes > 0:
        escala = consumo_mes / total_perfil
        consumos = {k: v * escala for k, v in consumos.items()}
        notas.append("Perfil de equipamentos escalado proporcionalmente ao seu consumo, assim como os custos das medidas. "
                     "Valide com orçamentos reais.")
    consumo_total = sum(consumos.values())

    medidas_res = [avaliar_medida(m, consumos, p, fator_custo=escala) for m in meds.values()]
    por_id = {r.chave: r for r in medidas_res}
    A = somar("A", "Eficiência de baixo custo (LED + manutenção)",
              [por_id[i] for i in p["pacote_eficiencia_baixo_custo"]], p)
    consumo_pos_A = max(consumo_total - A.detalhes["kwh_mes_evitados"], 0.0)

    B = avaliar_fv(consumo_total, p, proprietario, area_m2, capital)
    C = avaliar_assinatura(consumo_total, p)
    B2 = avaliar_fv(consumo_pos_A, p, proprietario, area_m2, capital)
    C2 = avaliar_assinatura(consumo_pos_A, p)
    AB = somar("AB", "A + Solar própria", [A, B2], p)
    AC = somar("AC", "A + Solar por assinatura", [A, C2], p)

    viaveis = {"AC": AC}
    if proprietario and (capital is None or AB.investimento <= capital):
        viaveis["AB"] = AB
    recomendada = max(viaveis.values(), key=lambda r: r.vpl_rs).chave

    return {
        "premissas": p, "escala": escala, "notas": notas,
        "consumo_mes": consumo_total, "custo_mes": consumo_total * p["tarifa_kwh"],
        "consumo_pos_A": consumo_pos_A,
        "medidas": medidas_res, "A": A, "B": B, "C": C, "AB": AB, "AC": AC,
        "recomendada": recomendada, "proprietario": proprietario, "capital": capital,
    }
