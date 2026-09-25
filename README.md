# 🤖 Moprefipe: Agente Financeiro Inteligente e Proativo

[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-green)](#)
[![Tech Stack](https://img.shields.io/badge/Tech-Python%20%7C%20GenAI%20%7C%20Prompt%20Engineering-blue)](#)

Este repositório contém a implementação do **Moprefipe**, um agente financeiro inteligente desenvolvido como parte do laboratório **BIA do Futuro**. 

Diferente de chatbots tradicionais e reativos, o Moprefipe foi projetado com foco em **proatividade, hiper-personalização e alta confiabilidade**, utilizando IA Generativa para atuar como um verdadeiro parceiro financeiro do usuário, sempre com métricas rígidas para mitigação de alucinações.

---

## 🎯 O Desafio: Lab BIA do Futuro

O setor financeiro exige precisão. O objetivo deste projeto foi transcender o atendimento básico, criando um agente capaz de:
- Analisar o histórico e o perfil do investidor.
- Fornecer recomendações contextualizadas.
- Manter uma postura consultiva e segura, barrando respostas fora do escopo financeiro (*guardrails*).

## 📁 Estrutura do Projeto & Status das Entregas

O desenvolvimento seguiu uma esteira lógica de documentação e prototipagem. A situação atual do projeto é:

- [x] **`docs/01-documentacao-agente.md`**: Definição da persona (Moprefipe), escopo de atuação e arquitetura do agente.
- [x] **`docs/02-base-conhecimento.md`**: Mapeamento dos dados estruturados e contexto de negócios (perfil de investidor, portfólio, histórico).
- [x] **`docs/03-prompts.md`**: Construção do *System Prompt* utilizando técnicas de *Few-Shot Prompting* e injeção de contexto para controle estrito de qualidade.
- [x] **`app.py`**: Prototipagem da aplicação funcional, integrando a lógica de LLM com a base de conhecimento.
- [ ] **`docs/04-metricas.md`**: (Pendente) Definição de SLOs (Service Level Objectives) para precisão, tempo de resposta e taxa de alucinação.
- [ ] **`docs/05-pitch.md`**: (Pendente) Roteiro da apresentação executiva do projeto.

---

## 🧠 Arquitetura e Engenharia de Prompts

O núcleo de inteligência do **Moprefipe** baseia-se em princípios fortes de Engenharia de Prompts:
1. **Contexto Fechado**: O agente opera estritamente sobre a base de conhecimento fornecida, garantindo segurança na recomendação de produtos financeiros.
2. **Prevenção de Alucinação**: Instruções explícitas no *System Prompt* obrigam o agente a declarar desconhecimento caso a pergunta fuja da sua base de dados, em vez de inventar dados mercadológicos.
3. **Tom de Voz**: Profissional, analítico e encorajador.

## 🚀 Como Executar o Protótipo

Para rodar a aplicação localmente, certifique-se de ter o Python instalado e siga os passos:

1. Clone o repositório:
   ```bash
   git clone https://github.com/elvingup/dio-lab-bia-do-futuro.git
   cd dio-lab-bia-do-futuro

   ```


2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate

```


3. Instale as dependências:
```bash
pip install -r requirements.txt

```


4. Configure suas variáveis de ambiente (ex: API Keys) no arquivo `.env`.


5. Execute a aplicação:
```bash
python app.py 
# ou 'streamlit run app.py' / 'gradio app.py' dependendo da interface escolhida

```



---

## 🛡️ Cultura de Confiabilidade

Inspirado em práticas de SRE (Site Reliability Engineering), o Moprefipe é desenvolvido com a mentalidade de que *falhas no setor financeiro custam caro*. A separação entre base de conhecimento, regras de prompt e código de aplicação visa facilitar futuras auditorias e implementações de testes automatizados (como matrizes de confusão para avaliar a assertividade das recomendações).

---

*Projeto desenvolvido para fins didáticos e demonstração de arquitetura de agentes autônomos.*
