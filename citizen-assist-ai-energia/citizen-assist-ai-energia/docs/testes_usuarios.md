# Testes com usuários

## Objetivo
Verificar se MEIs (ou pessoas próximas desse público, como familiares que ajudam no comércio) **entendem** e **acham úteis** as orientações do assistente, e ajustar o texto e o fluxo.

## Participantes sugeridos
3 a 5 pessoas que tenham ou ajudem em pequeno comércio. Registrar apenas perfil genérico (ex.: "dono de lanchonete, 40-50 anos").

## Situações a testar
| # | Situação | Comando/pergunta sugerida |
|---|---|---|
| 1 | Entender se vale a pena trocar lâmpadas | "vale a pena trocar as lâmpadas?" |
| 2 | Comparar opções com o consumo real | `simular` (usar a fatura do participante, sem fotografar dados pessoais) |
| 3 | Entender o Fio B | "o que é fio b?" |
| 4 | Participante que aluga o ponto | "e se eu alugo o ponto?" / `simular` respondendo "n" para imóvel próprio |
| 5 | Entender limitações | `limitações` |

## Perguntas após cada situação
1. Você entendeu a resposta? (1 a 5)
2. Alguma palavra ou número ficou confuso?
3. A informação ajudaria você a decidir algo? (1 a 5)
4. O que faltou?

## Registro

| Participante (perfil) | Situação | Compreensão (1-5) | Utilidade (1-5) | Comentários | Ajuste feito |
|---|---|---:|---:|---|---|
| Participante 1 – Dono de lanchonete, 40-50 anos | 1. Troca de lâmpadas | 5 | 5 | Entendeu que lâmpadas LED consomem menos energia e podem reduzir a conta de luz. | Nenhum ajuste necessário. |
| Participante 1 – Dono de lanchonete, 40-50 anos | 2. Simulação de consumo | 4 | 5 | Achou interessante comparar o consumo atual com as possíveis economias, mas teve dificuldade com o valor em kWh. | Explicar melhor o significado de kWh. |
| Participante 1 – Dono de lanchonete, 40-50 anos | 3. Entender o Fio B | 3 | 4 | Entendeu parcialmente, mas achou o termo técnico difícil. | Utilizar palavras mais simples e exemplos práticos. |
| Participante 2 – Pessoa que ajuda em uma mercearia familiar, 25-35 anos | 4. Aluga o ponto comercial | 5 | 5 | Entendeu que, por não ser proprietário do imóvel, precisa conversar com o dono antes de realizar mudanças na instalação elétrica. | Destacar a importância da autorização do proprietário. |
| Participante 2 – Pessoa que ajuda em uma mercearia familiar, 25-35 anos | 5. Limitações | 4 | 4 | Gostou de saber que as simulações são estimativas, mas gostaria de entender melhor o que pode alterar os resultados. | Explicar que tarifas e condições de instalação podem mudar a economia. |
| Participante 3 – Dono de salão de beleza, 30-40 anos | 1. Troca de lâmpadas | 5 | 5 | Considerou a orientação simples e útil para reduzir os gastos mensais. | Nenhum ajuste necessário. |
| Participante 3 – Dono de salão de beleza, 30-40 anos | 2. Simulação de consumo | 4 | 5 | Conseguiu acompanhar a simulação, mas gostaria de visualizar melhor quanto economizaria por mês e por ano. | Destacar a economia mensal e anual. |
| Participante 3 – Dono de salão de beleza, 30-40 anos | 3. Entender o Fio B | 4 | 4 | Compreendeu a explicação depois de receber um exemplo relacionado à energia solar. | Manter exemplos cotidianos nas explicações. |
| Participante 3 – Dono de salão de beleza, 30-40 anos | 5. Limitações | 5 | 5 | Entendeu que o assistente não substitui uma avaliação técnica ou uma análise oficial da concessionária. | Nenhum ajuste necessário. |

## Ajustes realizados após os testes

| Data | Problema observado | Mudança no assistente | Arquivo alterado (commit) |
|---|---|---|---|
| 18/11/2026 | Dificuldade para entender o termo kWh. | Adicionada uma explicação simples sobre consumo de energia (comando `kwh`, com exemplo de lâmpada, e dica na pergunta de consumo do `simular`). | `citizen_energia/respostas.py`, `citizen_energia/chatbot.py`
| 18/11/2026 | Explicação do Fio B considerada muito técnica. | Simplificada a explicação com a analogia do "pedágio" e um exemplo em reais com energia solar (100 kWh enviados à rede). | `citizen_energia/respostas.py`, `citizen_energia/chatbot.py` |
| 18/11/2026 | Falta de destaque para a economia mensal e anual. | Cada opção do `simular` e do `comparar` agora mostra a economia por mês e no 1º ano. | `citizen_energia/respostas.py` |
| 18/11/2026 | Dúvidas sobre instalações em imóveis alugados. | Reforçada a orientação de conversar com o proprietário e pedir autorização por escrito antes de mexer na instalação (na recomendação, na solar e na assinatura). | `citizen_energia/respostas.py`  |
| 18/11/2026 | Dúvida sobre o que pode alterar os resultados. | Incluído em `limitações` o que pode mudar a economia: tarifa, regra do Fio B, telhado, uso da energia solar e preço dos equipamentos. | `citizen_energia/respostas.py`  |

## Síntese

Os testes indicaram que o assistente apresenta uma boa compreensão geral das necessidades dos pequenos comerciantes, principalmente nas orientações sobre economia de energia e substituição de lâmpadas por modelos LED.

Os dados de consumo foram consideradas úteis porque permitem visualizar possíveis economias na conta de energia. Entretanto, alguns termos técnicos, como kWh e Fio B, podem dificultar a compreensão de usuários sem conhecimento sobre eletricidade.

Também foi identificada a importância de orientar corretamente pessoas que trabalham em imóveis alugados, destacando a necessidade de autorização do proprietário para determinadas alterações.

Com base nos resultados, foram feitas melhorias na linguagem, na apresentação dos valores de economia e nas explicações técnicas.
