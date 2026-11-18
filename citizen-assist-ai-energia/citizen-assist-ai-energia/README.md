# Citizen Assist AI – Módulo de Energia e Sustentabilidade para MEI

**Global Solution 2026 – Soluções em Energias Renováveis e Sustentáveis (Ciência da Computação, 1CC)**

> Este repositório contém a contribuição da disciplina *Soluções em Energias Renováveis e Sustentáveis* ao Citizen Assist AI.
> Se o projeto for integrado a outras disciplinas, toda a contribuição de energia está na pasta `citizen_energia/`, em `data/` e em `docs/`.

## Integrantes

Enzo Stahal Freitas | 569001
Matheus Bruno de Lima | 572944

## Público e problema

**Público:** microempreendedores individuais (MEI) com pequenos comércios (exemplo analisado: mercadinho/lanchonete de bairro em Santo André/SP).

**Problema:** a energia é um dos maiores custos fixos do comércio de bairro (refrigeração e iluminação ligadas o dia todo), a tarifa da distribuidora sobe todo ano e o MEI não tem como avaliar sozinho se vale a pena reduzir o consumo, instalar painéis ou assinar energia solar, nem entende regras como o "Fio B" da Lei 14.300.

**Contribuição do assistente:** responde em linguagem simples, com números calculados, comparando alternativas para a mesma necessidade, e sempre informa as premissas, as fontes e as limitações.

## Funcionalidades de energia

| Comando no assistente | O que faz |
|---|---|
| `simular` | Pergunta consumo, tarifa, se o imóvel é próprio, área de telhado e capital; calcula e compara as alternativas com os dados do usuário |
| `comparar` | Mostra a comparação completa com o mercadinho-exemplo |
| `led`, `geladeira`, `ar condicionado` | Explica cada medida de eficiência com números |
| `solar`, `assinatura`, `fio b` | Explica as alternativas com fonte renovável e a regra da Lei 14.300 |
| `co2` | Mostra o impacto ambiental e por que é modesto na matriz brasileira |
| `limitações`, `referências` | Lista as condições das estimativas e as fontes |

## Alternativas comparadas (mesma necessidade, período de 10 anos)

- **A – Eficiência de baixo custo:** LED + manutenção da refrigeração.
- **B – Solar fotovoltaica própria** (fonte renovável): on-grid com Fio B escalonado (Lei 14.300).
- **C – Solar por assinatura** (fonte renovável): sem investimento inicial.
- **A+B** e **A+C:** eficiência primeiro, depois solar dimensionada para o consumo já reduzido.

Resultados, fórmulas, sensibilidade e justificativas: [`docs/analise_comparativa.md`](docs/analise_comparativa.md).

## Como executar

Requer Python 3.10+. Não precisa instalar nenhuma biblioteca.

```bash
python main.py
```

Para testar, digite no assistente, por exemplo: `comparar`, `simular`, `vale a pena trocar as lâmpadas?`, `e painel solar?`, `o que é fio b?`, `limitações`, `referências`.

## Estrutura

```
main.py                      # entrada do assistente
citizen_energia/
  dados.py                   # leitura de premissas e CSVs
  calculos.py                # fórmulas: kWh, geração, Fio B, VPL, payback, CO2
  cenarios.py                # alternativas A, B, C, A+B, A+C e regra de recomendação
  respostas.py               # textos do assistente (usam os números calculados)
  chatbot.py                 # conversa no terminal e reconhecimento de intenções
data/
  premissas.json             # cada premissa com valor, unidade, status e fonte
  equipamentos_mercadinho.csv  # perfil de consumo (ESTIMADO)
  medidas_eficiencia.csv     # medidas, custos e economias (ESTIMADO)
docs/
  analise_comparativa.md     # cálculos, comparação, sensibilidade, impactos, justificativas
  referencias.md             # fontes e status de verificação
  testes_usuarios.md         # registros dos testes com usuários e dos ajustes
```

## Dados e honestidade das estimativas

Cada premissa em `data/premissas.json` tem o status **PUBLICO** (veio de fonte consultada), **ESTIMADO** (suposição justificada) ou **PERFIL** (hipótese do estabelecimento-exemplo). Os resultados são estimativas, **não garantias**. Os valores mais sensíveis (tarifa, custo por Wp, Fio B da Enel SP, irradiação) devem ser substituídos por dados da fatura real e por orçamentos antes de qualquer decisão.
