# Referências e status de verificação

Legenda: **Consultada** = conferida ao montar o projeto (18/11/2026), conferir novamente antes de entregar. **A verificar** = o grupo precisa consultar a fonte primária e atualizar `data/premissas.json`.

| # | Fonte | O que usamos | Status |
|---|---|---|---|
| 1 | Lei 14.300/2022, art. 27 (Planalto) – marco legal da geração distribuída | Escalonamento do Fio B: 60% (2026), 75% (2027), 90% (2028); regra antiga até 2045 para quem pediu conexão até 7/1/2023; regra após 2028 definida pela ANEEL | Consultada via imprensa especializada; **ler o texto da lei no Planalto** |
| 2 | Canal Solar – "Consumidores passarão a arcar com 60% do Fio B a partir de 2026" – https://canalsolar.com.br/consumidores-60-do-fio-b-2026/ | Exemplo CPFL Paulista: 60% do Fio B = R$ 0,1239/kWh (proxy do Fio B cheio) | Consultada. **A verificar:** TUSD Fio B da Enel SP |
| 3 | Exame – Aneel aprova aumento médio de 10,18% nas tarifas da Enel São Paulo – https://exame.com/economia/contas-de-luz-aneel-aprova-aumento-medio-de-1018-nas-tarifas-da-enel-sao-paulo/ | Reajuste de 4/7/2026 (baixa tensão residencial ~9,02%; alta tensão 15%) | Consultada. **A verificar:** tarifa B3 comercial na fatura |
| 4 | Canal Solar – tag Enel São Paulo – https://canalsolar.com.br/tag/enel-sao-paulo/ | Alta de ~79% na tarifa de baixa tensão entre 2016 e 2026 (base do reajuste anual de 6%) | Consultada (manchete) |
| 5 | Cenário Energia/Solfácil – https://cenarioenergia.com.br/2026/06/09/preco-do-watt-pico-residencial-recua-7-em-um-ano-e-abre-janela-de-oportunidade-na-mmgd/ | Preço médio nacional R$ 2,45/Wp (1T/2026), residencial | Consultada. Adotamos R$ 3,00/Wp para comercial pequeno (**estimado**) |
| 6 | Greener via Eixos – https://eixos.com.br/solar/precos-de-sistemas-fotovoltaicos-caem-30-em-janeiro-de-2024/ | Sistema comercial de 50 kWp ≈ R$ 122,5 mil (jan/2024) = R$ 2,45/Wp | Consultada (dado de 2024) |
| 7 | Eixos – https://eixos.com.br/brasil-tem-menor-taxa-de-emissao-de-carbono-na-geracao-eletrica-em-onze-anos/ (dados MCTI) | Fator de emissão do SIN em 2023: 38,5 kg CO₂/MWh | Consultada |
| 8 | Canal Solar – https://canalsolar.com.br/emissoes-de-co₂-geracao-eletrica-mcti/ (dados MCTI/SIRENE) | Fatores mensais de 2025: 21,5 a 28,9 kg/MWh | Consultada. **A verificar:** valor oficial mais recente em gov.br/mcti → SIRENE → fatores de emissão |
| 9 | ANEEL – REN 1.000/2021 | Custo de disponibilidade (30/50/100 kWh) | **A verificar** (artigo e valores) |
| 10 | CRESESB – SunData | Irradiação solar (HSP) para Santo André | **A verificar** (usamos 4,5 kWh/m²/dia como estimativa) |
| 11 | Programa Procel / Inmetro (ENCE e Selo Procel de refrigeradores e condicionadores de ar) | Ordem de grandeza da economia de equipamentos eficientes | **A verificar** |
| 12 | Propostas/orçamentos de integradores solares e de empresas de assinatura de energia | Custo real do sistema e desconto real da assinatura | **A obter** (mínimo 3) |

## O que NÃO foi encontrado e está como estimativa

- Tarifa unitária B3 comercial da Enel SP com tributos (R$ 1,10/kWh é suposição; usar a fatura real).
- Valor do Fio B da Enel SP (usado proxy da CPFL Paulista).
- Desconto típico de assinatura (12% é suposição; depende do contrato).
