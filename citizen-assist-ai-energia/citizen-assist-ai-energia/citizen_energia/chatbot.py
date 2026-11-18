"""Assistente de energia (terminal). Regras por palavras-chave => respostas reproduzíveis e rastreáveis ao cálculo."""
from __future__ import annotations

import re
import unicodedata

from . import cenarios, respostas as r


def normalizar(texto: str) -> str:
    t = unicodedata.normalize("NFD", texto.lower())
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", t).strip()


# (chaves de prefixo/frase, intencao) - a ordem define a prioridade
INTENCOES = [
    (("sair", "tchau", "encerrar"), "sair"),
    (("simular", "simulacao", "meu consumo", "minha conta", "calcular"), "simular"),
    (("fio b", "taxa do sol", "14300", "lei 14"), "fiob"),
    (("kwh", "quilowatt"), "kwh"),
    (("assinatura", "compartilhad", "alug", "inquilin", "sem telhado", "sem instalar"), "assinatura"),
    (("solar", "painel", "paineis", "fotovolt", "placa"), "solar"),
    (("led", "lampada", "iluminacao"), "led"),
    (("geladeira", "freezer", "expositor", "refriger", "balcao"), "refrigeracao"),
    (("ar condicionado", "split", "climatiz"), "ar"),
    (("co2", "carbono", "ambient", "emissao", "emissoes", "sustent"), "co2"),
    (("limita", "garantia", "certeza", "risco"), "limitacoes"),
    (("referencia", "fonte", "bibliograf"), "referencias"),
    (("compar", "alternativa", "melhor", "recomend", "vale a pena", "economizar"), "comparar"),
]
SAUDACOES = {"oi", "ola", "bom dia", "boa tarde", "boa noite", "ajuda", "menu", "help"}


def detectar_intencao(texto: str) -> str:
    t = normalizar(texto)
    if t in SAUDACOES:
        return "ajuda"
    toks = t.split()
    for chaves, intencao in INTENCOES:
        for k in chaves:
            if " " in k:
                if k in t:
                    return intencao
            elif any(tok.startswith(k) for tok in toks):
                return intencao
    return "desconhecida"


def _numero(txt: str) -> float | None:
    s = txt.lower().replace("r$", "").replace("kwh", "").replace("m2", "").replace("m²", "").strip()
    if not s:
        return None
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")
    try:
        v = float(s)
    except ValueError:
        return None
    return v if v >= 0 else None


class Assistente:
    def __init__(self, entrada=input, saida=print):
        self.entrada = entrada
        self.saida = saida
        self._padrao = cenarios.comparar()
        self.ultimo = self._padrao

    # --- fluxo guiado ---
    def _perguntar_numero(self, pergunta: str) -> float | None:
        resp = self.entrada(pergunta + " ")
        return _numero(resp) if resp.strip() else None

    def simular(self) -> str:
        self.saida("Vou fazer 5 perguntas rápidas (Enter = usar valor padrão). Use vírgula para decimais.")
        consumo = self._perguntar_numero("1) Consumo médio mensal em kWh (kWh é a energia que a fatura mede; procure 'consumo' na fatura):")
        tarifa = self._perguntar_numero("2) Tarifa em R$/kWh com tributos (veja na fatura):")
        imovel = self.entrada("3) O imóvel é próprio? (s/n): ").strip().lower()
        proprio = not imovel.startswith("n")
        area = self._perguntar_numero("4) Área livre no telhado em m²:")
        capital = self._perguntar_numero("5) Quanto você pode investir agora (R$)? Enter = sem limite:")
        self.ultimo = cenarios.comparar(consumo, tarifa, proprio, area, capital)
        return r.resumo_comparacao(self.ultimo)

    # --- resposta principal ---
    def responder(self, texto: str) -> str:
        i = detectar_intencao(texto)
        res = self.ultimo
        if i == "sair":
            return "Até logo! Lembre: confira tarifa e orçamentos reais antes de decidir."
        if i == "ajuda":
            return r.AJUDA
        if i == "simular":
            return self.simular()
        if i == "comparar":
            return r.resumo_comparacao(res)
        mapa = {"led": lambda: r.explicar_led(res), "refrigeracao": lambda: r.explicar_refrigeracao(res),
                "ar": lambda: r.explicar_ar(res), "solar": lambda: r.explicar_solar(res),
                "assinatura": lambda: r.explicar_assinatura(res), "fiob": lambda: r.explicar_fio_b(res), "kwh": r.explicar_kwh,
                "co2": lambda: r.explicar_co2(res), "limitacoes": r.limitacoes, "referencias": r.referencias}
        if i in mapa:
            return mapa[i]()
        return "Não entendi bem. " + r.AJUDA

    def executar(self) -> None:
        self.saida("=== Citizen Assist AI - Energia para pequenos comércios ===")
        self.saida("Aviso: valores são ESTIMATIVAS, não garantias.\n" + r.AJUDA)
        while True:
            try:
                msg = self.entrada("\nVocê: ")
            except (EOFError, KeyboardInterrupt):
                break
            if not msg.strip():
                continue
            resp = self.responder(msg)
            self.saida("\nAssistente: " + resp)
            if detectar_intencao(msg) == "sair":
                break


def main() -> None:
    Assistente().executar()
