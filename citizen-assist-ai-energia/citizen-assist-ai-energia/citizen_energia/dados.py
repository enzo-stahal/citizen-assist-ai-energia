"""Carregamento de premissas, equipamentos e medidas (pasta data/)."""
from __future__ import annotations

import csv
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"


def premissas_completas(caminho: Path | None = None) -> dict:
    """Premissas com valor, unidade, status e fonte."""
    with open(caminho or DATA / "premissas.json", encoding="utf-8") as f:
        bruto = json.load(f)
    return {k: v for k, v in bruto.items() if not k.startswith("_")}


def premissas(caminho: Path | None = None) -> dict:
    """Apenas os valores (dict simples chave -> valor)."""
    return {k: v["valor"] for k, v in premissas_completas(caminho).items()}


def _ler_csv(nome: str) -> list[dict]:
    with open(DATA / nome, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def equipamentos() -> list[dict]:
    linhas = _ler_csv("equipamentos_mercadinho.csv")
    for linha in linhas:
        for c in ("qtd", "potencia_w", "horas_dia", "dias_mes", "fator_uso"):
            linha[c] = float(linha[c])
    return linhas


def medidas() -> list[dict]:
    linhas = _ler_csv("medidas_eficiencia.csv")
    for linha in linhas:
        for c in ("fracao_alvo", "economia_pct", "custo_inicial_rs", "custo_anual_rs", "vida_util_anos"):
            linha[c] = float(linha[c])
        linha["alvos"] = [x.strip() for x in linha["alvos"].split(";")]
    return linhas
