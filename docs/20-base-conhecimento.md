# Base de Conhecimento

## Dados Utilizados

O agente utiliza dados mockados nos arquivos da pasta `data` para efetuar o RAG (Retrieval Augmented Generation). Os arquivos utilizados pelo agente são os seguintes:

| Arquivo | Formato | Utilização pelo Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores |
| `perfil_investidor.json` | JSON | Personalizar recomendações |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente |

---

## Estratégia de Integração

### Como os dados são carregados?

Os dados da Base de Conhecimento são armazenados localmente na pasta `data/` e carregados pela aplicação no início da execução. Os arquivos CSV são lidos com **Pandas**, enquanto os arquivos JSON são carregados como estruturas Python.

A aplicação mantém os dados carregados em memória durante a sessão, evitando a leitura dos arquivos a cada interação do usuário. No caso da interface desenvolvida com Streamlit, o carregamento pode ser realizado com mecanismos de cache da própria plataforma, reduzindo operações desnecessárias de I/O durante as interações.

Os quatro arquivos são tratados de acordo com sua finalidade:

* `perfil_investidor.json`: carregado como o contexto cadastral e comportamental principal do cliente;
* `transacoes.csv`: carregado para consultas e análises sobre receitas, despesas, categorias e padrões de gastos;
* `historico_atendimento.csv`: carregado para recuperar informações relevantes de interações anteriores;
* `produtos_financeiros.json`: carregado como catálogo das opções financeiras disponíveis para consulta e comparação.

O carregamento da Base de Conhecimento é separado da geração da resposta pelo LLM. Dessa forma, o modelo de linguagem não acessa diretamente os arquivos: a aplicação é responsável por localizar, filtrar e organizar os dados que poderão ser utilizados na resposta.

### Como os dados são usados no prompt?

Os dados da Base de Conhecimento **não são incluídos integralmente no System Prompt**. O System Prompt contém apenas as instruções permanentes do Moprefipe: sua identidade, objetivo, regras de comportamento, limites de atuação, critérios de segurança e orientações para evitar alucinações.

A cada solicitação do usuário, a aplicação identifica quais informações da Base de Conhecimento são relevantes para responder à pergunta. Em seguida, recupera e organiza somente esse subconjunto de dados em um **contexto dinâmico**, que é enviado ao LLM juntamente com a mensagem do usuário.

O fluxo lógico é:

**Mensagem do usuário → identificação dos dados relevantes → recuperação dos dados → montagem do contexto → aplicação das instruções do agente → LLM → validação da resposta**

Por exemplo:

* uma pergunta sobre gastos em alimentação consulta principalmente `transacoes.csv`;
* uma pergunta sobre o perfil e os objetivos do cliente utiliza `perfil_investidor.json`;
* uma pergunta sobre interações anteriores utiliza `historico_atendimento.csv`;
* uma solicitação de comparação entre produtos consulta `produtos_financeiros.json`, podendo também utilizar o perfil e os objetivos do cliente para fornecer contexto.

O contexto enviado ao LLM deve ser estruturado de forma explícita, separando os dados recuperados da pergunta do usuário. Isso permite que o modelo diferencie **dados fornecidos pela aplicação** de **instruções do usuário**.

Além disso, informações financeiras específicas devem ser respondidas somente quando houver dados correspondentes na Base de Conhecimento. Quando os dados necessários não estiverem disponíveis, o agente deve informar essa limitação em vez de preencher a lacuna com uma suposição. Essa estratégia está alinhada às regras de segurança e anti-alucinação definidas na documentação do Moprefipe.

---

## Exemplo de Contexto Montado

Eis um exemplo de como os dados são formatados para o agente:

```text
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
```
