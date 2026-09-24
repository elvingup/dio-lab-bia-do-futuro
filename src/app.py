import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

# =====================================================================
# 1. Configuração do Modelo GenAI (SDK Oficial)
# =====================================================================
# A chave de API deve estar configurada nas variáveis de ambiente do SO.
API_KEY = os.getenv("GEMINI_API_KEY", "SUA_CHAVE_API_AQUI")
genai.configure(api_key=API_KEY)

# =====================================================================
# 2. Carregamento do System Prompt
# =====================================================================
# Lê as regras de negócio e de segurança do Moprefipe
try:
    with open("../system-prompt.md", "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    SYSTEM_PROMPT = "Você é o Moprefipe, um agente preditivo de finanças."

# Inicializamos o modelo de IA e passamos o system prompt como instrução base
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# =====================================================================
# 3. Carregamento da Base de Conhecimento com Pandas
# =====================================================================
def carregar_arquivos_dados():
    """Lê os arquivos mockados usando Pandas e formata como texto para o contexto."""
    # Cliente
    try:
        with open("../data/cliente.json", "r", encoding="utf-8") as f:
            v_cliente = f.read()
    except FileNotFoundError:
        v_cliente = "Dados do cliente não encontrados."

    # Transações (Utilizando Pandas para processar o CSV estruturado)
    try:
        df_transacoes = pd.read_csv("../data/transacoes.csv")
        # to_string formata o dataframe como uma tabela textual limpa
        v_transacoes = df_transacoes.to_string(index=False) 
    except FileNotFoundError:
        v_transacoes = "Transações não encontradas."

    # Atendimentos
    try:
        with open("../data/atendimentos.json", "r", encoding="utf-8") as f:
            v_atendimentos = f.read()
    except FileNotFoundError:
        v_atendimentos = "Atendimentos anteriores não encontrados."

    # Produtos
    try:
        with open("../data/produtos.json", "r", encoding="utf-8") as f:
            v_produtos = f.read()
    except FileNotFoundError:
        v_produtos = "Produtos não encontrados."
        
    return v_cliente, v_transacoes, v_atendimentos, v_produtos

var_cliente, var_transacoes, var_atendimentos, var_produtos = carregar_arquivos_dados()

# =====================================================================
# 4. Montagem do Contexto
# =====================================================================
CONTEXT = f"""
CLIENTE:
{var_cliente}

TRANSAÇÕES RECENTES (Histórico):
{var_transacoes}

ATENDIMENTOS ANTERIORES:
{var_atendimentos}

PRODUTOS DISPONÍVEIS:
{var_produtos}
"""

# =====================================================================
# 5. Interface Gráfica com Streamlit
# =====================================================================
st.set_page_config(page_title="Moprefipe - Co-piloto Financeiro", page_icon="🏦")
st.title("🏦 Moprefipe")
st.markdown("Seu co-piloto financeiro preventivo e conselheiro.")

# Histórico de mensagens do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Renderiza as mensagens anteriores na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de entrada para o usuário
if prompt := st.chat_input("O que vamos planejar hoje?"):
    # 1. Exibe a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Exibe o assistente carregando
    with st.chat_message("assistant"):
        with st.spinner("Moprefipe está cruzando seus dados financeiros..."):
            try:
                # O SDK gerencia a chamada à API. Injetamos apenas o contexto e a dúvida.
                prompt_completo = f"CONTEXTO DA BASE DE CONHECIMENTO:\n{CONTEXT}\n\nPERGUNTA DO USUÁRIO:\n{prompt}"
                
                response = model.generate_content(prompt_completo)
                resposta_genai = response.text
                
            except Exception as e:
                # Tratamento de erro alinhado com o tom empático e livre de jargões técnicos da documentação
                resposta_genai = f"Puxa, estou com um pouco de dificuldade para acessar seus dados neste exato momento. Que tal tentarmos de novo em alguns minutinhos? (Detalhe técnico: {e})"
            
            st.markdown(resposta_genai)
            
    # 3. Salva a resposta no histórico da sessão
    st.session_state.messages.append({"role": "assistant", "content": resposta_genai})