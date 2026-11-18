"""Formulas basicas de energia, geracao, custo e indicadores financeiros.

Convencoes: energia em kWh, potencia em W/kWp, dinheiro em R$ (nominal).
Ano 0 = investimento; anos 1..N = fluxos de caixa anuais.
"""
from __future__ import annotations


# ---------- Consumo ----------
def consumo_equipamento_kwh_mes(e: dict) -> float:
    """E (kWh/mes) = qtd x P(W) x horas/dia x dias/mes x fator_de_uso / 1000."""
    return e["qtd"] * e["potencia_w"] * e["horas_dia"] * e["dias_mes"] * e["fator_uso"] / 1000.0


def consumo_por_id(equips: list[dict]) -> dict[str, float]:
    return {e["id"]: consumo_equipamento_kwh_mes(e) for e in equips}


# ---------- Solar ----------
def geracao_kwh_mes_por_kwp(p: dict) -> float:
    """Geracao mensal media por kWp = HSP x (365/12) x PR."""
    return p["hsp_kwh_m2_dia"] * 365.0 / 12.0 * p["performance_ratio"]


def pct_fio_b(p: dict, ano: int) -> float:
    """Fracao do Fio B cobrada sobre a energia compensada (Lei 14.300, art. 27)."""
    tabela = {int(k): v for k, v in p["fio_b_pct_por_ano"].items()}
    return tabela.get(ano, p["fio_b_pct_apos_tabela"])


def dimensionar_fv(consumo_kwh_mes: float, p: dict, area_m2: float | None = None) -> dict:
    """Potencia (kWp) limitada pelo consumo faturavel e pela area do telhado."""
    area = p["area_telhado_m2"] if area_m2 is None else area_m2
    ger_kwp = geracao_kwh_mes_por_kwp(p)
    faturavel = max(consumo_kwh_mes - p["disponibilidade_kwh"], 0.0)
    alvo_kwp = faturavel * p["cobertura_alvo_fv"] / ger_kwp
    max_area_kwp = area / p["area_por_kwp_m2"]
    bruto = min(alvo_kwp, max_area_kwp)
    modulos = int(bruto * 1000 // p["potencia_modulo_wp"])
    kwp = modulos * p["potencia_modulo_wp"] / 1000.0
    return {
        "kwp": kwp,
        "modulos": modulos,
        "kwp_alvo": alvo_kwp,
        "limitado_por_area": max_area_kwp < alvo_kwp,
        "area_necessaria_m2": kwp * p["area_por_kwp_m2"],
    }


# ---------- Tarifa ----------
def tarifa_no_ano(p: dict, t: int) -> float:
    """Tarifa no ano t (t=1 e o ano inicial) com reajuste anual."""
    return p["tarifa_kwh"] * (1 + p["reajuste_tarifa"]) ** (t - 1)


# ---------- Indicadores ----------
def vpl(fluxos: list[float], taxa: float) -> float:
    return sum(f / (1 + taxa) ** t for t, f in enumerate(fluxos))


def payback_anos(fluxos: list[float]) -> float | None:
    """Tempo (anos, com interpolacao) para o fluxo acumulado ficar >= 0. None se nao ocorre no horizonte."""
    if fluxos[0] >= 0:
        return 0.0
    acum = fluxos[0]
    for t in range(1, len(fluxos)):
        anterior = acum
        acum += fluxos[t]
        if acum >= 0 and fluxos[t] > 0:
            return (t - 1) + (-anterior) / fluxos[t]
    return None


def co2_evitado_kg(kwh: float, p: dict) -> float:
    return kwh * p["fator_emissao_kg_kwh"]
