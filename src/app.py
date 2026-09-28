from pathlib import Path
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

st.set_page_config(page_title="Moprefipe - Monitoramento Preditivo de Finanças Pessoais", page_icon="🏦", layout="centered")

# ---------------------------------------------------------------------
# 1. Configurações Iniciais e Variáveis de Ambiente
# ---------------------------------------------------------------------
load_dotenv()

# Ancoragem dinâmica de caminhos 
BASE_DIR = Path(__file__).resolve().parent

# Trata tanto o cenário de 'app.py' estar na raiz quanto dentro de 'src/'
DATA_DIR = BASE_DIR / "data" if (BASE_DIR / "data").exists() else BASE_DIR.parent / "data"

PROMPT_PATH = BASE_DIR / "system-prompt.md"

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("A variável de ambiente **GEMINI_API_KEY** não foi configurada.")
    st.stop()

# Inicialização do Cliente Gemini (SDK Oficial)
@st.cache_resource
def get_genai_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)

client = get_genai_client(API_KEY)

# ---------------------------------------------------------------------
# 2. Carregamento de Recursos Cheados (Performance & I/O)
# ---------------------------------------------------------------------
@st.cache_data(ttl=3600)
def carregar_system_prompt(path: Path) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Você é o Moprefipe, um agente preditivo de finanças."
    except Exception as e:
        st.error(f"Erro ao carregar o System Prompt: {e}")
        st.stop()

@st.cache_data(ttl=300)
def carregar_base_conhecimento(data_dir: Path) -> str:
    """Lê os arquivos de dados locais e formata um único contexto delimitado."""
    def ler_arquivo(filename: str, default: str) -> str:
        filepath = data_dir / filename
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            return default

    v_cliente = ler_arquivo("cliente.json", "Dados do cliente não encontrados.")
    v_atendimentos = ler_arquivo("atendimentos.json", "Atendimentos não encontrados.")
    v_produtos = ler_arquivo("produtos.json", "Produtos não encontrados.")

    # Processamento seguro das transações em CSV via Pandas
    transacoes_path = data_dir / "transacoes.csv"
    try:
        df_transacoes = pd.read_csv(transacoes_path)
        v_transacoes = df_transacoes.to_string(index=False)
    except FileNotFoundError:
        v_transacoes = "Transações não encontradas."
    except Exception as e:
        v_transacoes = f"Erro ao processar transações: {e}"

    return f"""

=== BASE DE CONHECIMENTO DO CLIENTE ===

[DADOS DO CLIENTE]
{v_cliente}

[HISTÓRICO DE TRANSAÇÕES]
{v_transacoes}

[HISTÓRICO DE ATENDIMENTOS]
{v_atendimentos}

[CATÁLOGO DE PRODUTOS DISPONÍVEIS]
{v_produtos}
=======================================
"""

SYSTEM_PROMPT = carregar_system_prompt(PROMPT_PATH)
CONTEXT = carregar_base_conhecimento(DATA_DIR)

# ---------------------------------------------------------------------
# 3. Interface do Usuário (Streamlit UI & Gestão de Chat)
# ---------------------------------------------------------------------
st.title("🏦 Moprefipe")
st.markdown("Seu co-piloto financeiro preventivo e conselheiro.")

# Inicialização do Histórico no Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Loop de interação do Chat
if prompt := st.chat_input("O que vamos planejar hoje?"):
    # 1. Registra e renderiza a pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Constrói o histórico conversacional para manter o contexto multi-turn
    historico_conversacao = ""
    for msg in st.session_state.messages[:-1]:  # Ignora a última (que acabou de entrar)
        papel = "Usuário" if msg["role"] == "user" else "Moprefipe"
        historico_conversacao += f"{papel}: {msg['content']}\n"

    # Montagem final do prompt injetando Contexto + Histórico + Pergunta Atual
    prompt_completo = f"""
{CONTEXT}

[HISTÓRICO DA CONVERSA RECENTE]
{historico_conversacao if historico_conversacao else "Nenhuma interação anterior."}

[NOVA PERGUNTA DO USUÁRIO]
{prompt}
"""

    # 3. Invocação da LLM via SDK Oficial do Gemini
    with st.chat_message("assistant"):
        with st.spinner("Moprefipe está cruzando seus dados financeiros..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt_completo,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.2,  # Baixa temperatura para maior alinhamento e menor alucinação
                    ),
                )
                resposta_genai = response.text
            except Exception as e:
                resposta_genai = (
                    "Puxa, estou com um pouco de dificuldade para acessar seus dados "
                    "neste exato momento. Que tal tentarmos de novo em alguns minutinhos?\n\n"
                    f"*(Detalhe técnico: {type(e).__name__})*"
                )

            st.markdown(resposta_genai)

    # 4. Registra a resposta da IA no histórico
    st.session_state.messages.append({"role": "assistant", "content": resposta_genai})