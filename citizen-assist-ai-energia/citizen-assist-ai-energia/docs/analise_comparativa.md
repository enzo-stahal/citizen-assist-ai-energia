# Análise comparativa de alternativas de energia – Mercadinho/MEI (Santo André/SP)

> Todos os valores são **estimativas** baseadas nas premissas de `data/premissas.json`; não são resultados garantidos.

## 1. Contexto e necessidade

**Público:** microempreendedores individuais (MEI) que operam pequenos comércios (mercadinho/lanchonete de bairro). **Necessidade:** a conta de luz pesa no custo fixo e a tarifa da distribuidora (Enel SP, a confirmar pela fatura) sobe todo ano. **Pergunta que o assistente responde:** *como reduzir ou atender o consumo de energia do meu comércio, quanto custa, em quanto tempo se paga e o que eu preciso saber antes de decidir?*

## 2. Análise de consumo (dados ESTIMADOS – perfil-exemplo)

Fórmula: `kWh/mês = qtd × potência (W) × horas/dia × dias/mês × fator de uso ÷ 1000`. Período: 1 mês típico.

| Equipamento | Qtd | W | h/dia | dias/mês | Fator de uso | kWh/mês | % |
|---|---|---|---|---|---|---|---|
| Iluminação fluorescente (2 tubos 32 W + reator) | 12 | 70 | 12 | 30 | 1,00 | 302,4 | 28,5% |
| Expositor refrigerado vertical (bebidas) antigo | 2 | 400 | 24 | 30 | 0,55 | 316,8 | 29,9% |
| Freezer horizontal | 1 | 300 | 24 | 30 | 0,45 | 97,2 | 9,2% |
| Geladeira de balcão | 1 | 250 | 24 | 30 | 0,45 | 81,0 | 7,6% |
| Ar-condicionado split 12.000 BTU/h | 1 | 1.100 | 8 | 26 | 0,60 | 137,3 | 12,9% |
| PDV + computador + balança + impressora | 1 | 180 | 12 | 30 | 0,80 | 51,8 | 4,9% |
| CFTV + roteador | 1 | 60 | 24 | 30 | 1,00 | 43,2 | 4,1% |
| Ventilador / TV / outros | 1 | 150 | 10 | 30 | 0,70 | 31,5 | 3,0% |
| **Total** |  |  |  |  |  | **1.061,2** | 100% |

Custo mensal estimado: 1.061,2 kWh × R$ 1,10 = **R$ 1.167,34**. A refrigeração (expositores, freezer, geladeira) responde por ~47% do consumo e a iluminação por ~28%.

> **Para uso real:** substitua o perfil pelos dados da fatura (kWh/mês dos últimos 12 meses e tarifa unitária com tributos).

## 3. Premissas e origem dos dados

| Premissa | Valor | Unidade | Status | Fonte / justificativa |
|---|---|---|---|---|
| tarifa_kwh | 1.1 | R$/kWh (com tributos) | ESTIMADO | Estimativa para B3 comercial Enel SP. O reajuste de 4/7/2026 foi consultado (Exame/ANEEL), mas o valor unitário deve vir da FATURA REAL. |
| disponibilidade_kwh | 100 | kWh/mês | PUBLICO | ANEEL REN 1.000/2021 (custo de disponibilidade: 30/50/100 kWh para mono/bi/trifásico). Conferir artigo. |
| ano_inicio | 2027 | ano | PERFIL | Primeiro ano completo após a análise (hoje: nov/2026). |
| horizonte_anos | 10 | anos | ESTIMADO | Período de referência comum a todas as alternativas. |
| taxa_desconto | 0.12 | a.a. | ESTIMADO | Custo de oportunidade do dinheiro do MEI (proxy). Ajustar à Selic/crédito atual. |
| reajuste_tarifa | 0.06 | a.a. | ESTIMADO | Hipótese. A tarifa da Enel SP subiu ~79% entre 2016 e 2026 na baixa tensão (Canal Solar), média de ~6%/ano. |
| hsp_kwh_m2_dia | 4.5 | kWh/m²/dia | ESTIMADO | Ordem de grandeza para a Grande São Paulo. VERIFICAR no CRESESB SunData (Santo André). |
| performance_ratio | 0.78 | - | ESTIMADO | Faixa típica 0,75-0,82 (perdas de inversor, temperatura, sujeira, cabos). |
| degradacao_fv_ano | 0.005 | por ano | ESTIMADO | Garantias de fabricantes costumam indicar 0,4%-0,55%/ano. |
| custo_fv_rs_wp | 3.0 | R$/Wp instalado | ESTIMADO | Solfácil/Cenário Energia: média nacional R$ 2,45/Wp no 1T/2026 (residencial). Adotado valor maior por ser comercial pequeno, com instalação e homologação. |
| om_fv_pct_capex_ano | 0.01 | fração do investimento/ano | ESTIMADO | Limpeza e manutenção preventiva. Troca de inversor (~10-12 anos) NÃO incluída. |
| potencia_modulo_wp | 550 | Wp | ESTIMADO | Módulo comercial típico. |
| area_por_kwp_m2 | 5.0 | m²/kWp | ESTIMADO | Módulo de 550 Wp ocupa ~2,6 m² (+ folgas). |
| area_telhado_m2 | 40 | m² | PERFIL | Hipótese do estabelecimento-exemplo. |
| cobertura_alvo_fv | 0.9 | fração do consumo faturável | ESTIMADO | Dimensionamento para cobrir ~90% do consumo acima do custo de disponibilidade. |
| autoconsumo_simultaneo | 0.45 | fração da geração | PERFIL | Hipótese: o comércio abre de dia, mas parte da geração vai para a rede. Medir com dados horários. |
| fio_b_pct_por_ano | {'2026': 0.6, '2027': 0.75, '2028': 0.9} | fração do Fio B cobrada | PUBLICO | Lei 14.300/2022, art. 27 (60% em 2026, 75% em 2027, 90% em 2028) - confirmado em Canal Solar e Olhar Digital. |
| fio_b_pct_apos_tabela | 0.9 | fração | ESTIMADO | A partir de 2029 a regra será definida pela ANEEL; hipótese de manter 90%. Pode ser pior ou melhor. |
| fio_b_cheio_rs_kwh | 0.2065 | R$/kWh (100% do Fio B) | ESTIMADO | PROXY: exemplo CPFL Paulista 2026, 60% = R$ 0,1239/kWh (Canal Solar) => 100% = R$ 0,2065. NÃO é valor da Enel SP. |
| desconto_assinatura | 0.12 | fração da tarifa | ESTIMADO | Ofertas comerciais de energia por assinatura costumam anunciar 10%-20%. Verificar se o desconto já considera Fio B e tributos. |
| cobertura_assinatura | 0.9 | fração do consumo faturável | ESTIMADO | Contratos costumam limitar a franquia. |
| fator_emissao_kg_kwh | 0.0385 | kg CO2/kWh | PUBLICO | MCTI/SIRENE: média do SIN em 2023 = 38,5 kg/MWh (Eixos). Em 2025 os meses ficaram entre ~21 e ~29 kg/MWh (Canal Solar). |
| pacote_eficiencia_baixo_custo | ['M1', 'M2'] | ids de medidas | ESTIMADO | Medidas de payback curto agrupadas como 'Alternativa A'. |

## 4. Alternativas comparadas (mesma necessidade, mesmo período)

**Necessidade comum:** atender o consumo do comércio (1.061 kWh/mês) com menor custo. **Período de referência comum:** 10 anos (2027–2036). **Indicadores:** investimento, economia no 1º ano, payback (tempo para o caixa acumulado ficar positivo), VPL a 12% a.a. (ganho líquido em valor de hoje), CO₂ evitado.

- **A – Eficiência energética de baixo custo:** LED + manutenção da refrigeração.
- **B – Solar fotovoltaica própria (fonte renovável):** on-grid, regras da Lei 14.300 (Fio B escalonado).
- **C – Solar por assinatura (fonte renovável):** créditos de usina compartilhada, sem investimento.
- **A+B** e **A+C:** eficiência primeiro, depois solar dimensionada para o consumo já reduzido.

### 4.1 Medidas de eficiência avaliadas individualmente

| ID | Medida | kWh/mês evitados | Investimento | Economia 1º ano | Se paga em | VPL 10 anos |
|---|---|---|---|---|---|---|
| M1 | Trocar tubos fluorescentes por LED | 151,2 | R$ 720,00 | R$ 1.995,84 | ~4 meses | R$ 12.999,04 |
| M2 | Manutenção da refrigeração (borrachas de vedação + limpeza do condensador + termostato) | 34,7 | R$ 300,00 | R$ 457,38 | ~8 meses | R$ 2.224,57 |
| M3 | Trocar 1 expositor antigo por modelo eficiente (Selo Procel A) | 63,4 | R$ 7.000,00 | R$ 836,35 | ~7,0 anos | -R$ 1.098,21 |
| M4 | Trocar ar-condicionado por modelo inverter | 41,2 | R$ 3.200,00 | R$ 543,63 | ~5,2 anos | R$ 636,16 |

LED e manutenção compensam rápido; trocar equipamentos grandes só compensa quando o atual está no fim da vida. Por isso a alternativa A inclui apenas M1 e M2.

### 4.2 Comparação final

| Alternativa | Investimento | Economia 1º ano | Se paga em | VPL 10 anos | kWh evitados/gerados no ano 1 | CO₂ evitado ano 1 (kg) |
|---|---|---|---|---|---|---|
| **A** – Eficiência de baixo custo (LED + manutenção) | R$ 1.020,00 | R$ 2.453,22 | ~5 meses | R$ 15.223,61 | 2.230 | 86 |
| **B** – Solar fotovoltaica própria | R$ 23.100,00 | R$ 9.780,04 | ~2,3 anos | R$ 43.814,43 | 9.865 | 380 |
| **C** – Solar por assinatura | R$ 0,00 | R$ 1.370,32 | imediato (sem investimento) | R$ 9.669,74 | 10.381 | 400 |
| **AB** – A + Solar própria | R$ 19.170,00 | R$ 10.137,54 | ~23 meses | R$ 49.649,23 | 9.981 | 384 |
| **AC** – A + Solar por assinatura | R$ 1.020,00 | R$ 3.558,59 | ~3 meses | R$ 23.023,73 | 10.604 | 408 |

Solar própria (B): 7,70 kWp, 14 módulos, ~38 m², ~822 kWh/mês. Fórmula da geração: `kWp × HSP × 365/12 × PR`.

Economia da solar própria no ano t: `G_t × tarifa_t − G_t × (1 − autoconsumo) × FioB_t × %Fio B(ano) − O&M`.

### 4.3 Sensibilidade (solar própria – B)

| Tarifa (R$/kWh) | Custo (R$/Wp) | Se paga em | VPL 10 anos |
|---|---|---|---|
| R$ 0,90 | R$ 2,50 | ~2,4 anos | R$ 34.237,79 |
| R$ 0,90 | R$ 3,00 | ~2,8 anos | R$ 30.170,25 |
| R$ 0,90 | R$ 4,00 | ~3,7 anos | R$ 22.035,19 |
| R$ 1,10 | R$ 2,50 | ~23 meses | R$ 47.881,96 |
| R$ 1,10 | R$ 3,00 | ~2,3 anos | R$ 43.814,43 |
| R$ 1,10 | R$ 4,00 | ~3,0 anos | R$ 35.679,36 |
| R$ 1,30 | R$ 2,50 | ~19 meses | R$ 61.526,13 |
| R$ 1,30 | R$ 3,00 | ~23 meses | R$ 57.458,60 |
| R$ 1,30 | R$ 4,00 | ~2,5 anos | R$ 49.323,53 |

Efeito do autoconsumo simultâneo (quanto da geração é usada na hora e não paga Fio B):

| Autoconsumo | Se paga em | VPL 10 anos |
|---|---|---|
| 25% | ~2,4 anos | R$ 41.333,22 |
| 45% | ~2,3 anos | R$ 43.814,43 |
| 70% | ~2,2 anos | R$ 46.915,93 |

## 5. Viabilidade e impactos ambientais

| Alternativa | Viabilidade | Impactos ambientais |
|---|---|---|
| A | Alta: baixo custo, sem obra, funciona em imóvel alugado. | Menos consumo; descarte correto de lâmpadas e peças trocadas. |
| B | Exige imóvel próprio (ou autorização), telhado adequado, capital ou financiamento e homologação na distribuidora. Não funciona em queda de energia (on-grid). | Baixa emissão na operação; fabricação e descarte de painéis/inversor têm impacto. |
| C | Acessível a quem aluga ou não tem telhado; economia menor; risco contratual (fidelidade, reajuste). | Usa geração renovável compartilhada; o ganho depende de a usina ser realmente adicional à matriz. |

**CO₂:** fator médio do SIN = 38,5 kg/MWh (MCTI, 2023). Como a matriz brasileira já é muito renovável, os ganhos de CO₂ são pequenos em valor absoluto (A: 86 kg/ano; B: 380 kg/ano). O principal benefício das alternativas para o MEI é econômico; o benefício ambiental é real, porém modesto.

## 6. Justificativa da recomendação do assistente

Para o perfil-exemplo, a opção de maior VPL entre as **viáveis** é **AB** (A + Solar própria). A lógica do assistente (`citizen_energia/cenarios.py`): (1) sempre começar pela eficiência de baixo custo; (2) recomendar solar própria se o usuário é proprietário e tem capital; (3) caso contrário, solar por assinatura; (4) escolher pela maior VPL entre as opções viáveis. Os textos do assistente (`respostas.py`) usam exatamente os números calculados aqui.

## 7. Limitações

- Perfil de consumo, tarifa unitária, Fio B da Enel SP, HSP, custo por Wp e desconto de assinatura são **estimados**.
- Regras do Fio B depois de 2028 ainda serão definidas pela ANEEL.
- Não há juros de financiamento, troca de inversor, impostos sobre equipamentos nem valor residual.
- Não é projeto de engenharia nem aconselhamento financeiro.
