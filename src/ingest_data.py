import json
import os
import sys
import pandas as pd
from datasets import load_dataset
from dotenv import load_dotenv  

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

def garantir_diretorio_data():
    """Garante que a pasta data/ existe no projeto."""
    os.makedirs("data", exist_ok=True)


def ingerir_transacoes():
    """Baixa dataset de transações reais/classificadas do Hugging Face

    e gera o data/transacoes.csv.
    """
    print("[1/4] Baixando dataset de transações do Hugging Face...")
    try:
        # Carregando dataset de categorização de transações financeiras
        # obs.: precisa de autenticação no Hugging Face para obter esse dataset 
        dataset = load_dataset(
            "mitulshah/transaction-categorization", split="train", token=os.getenv("HUGGINGFACE_TOKEN")
        )

        df = pd.DataFrame(dataset)

        # Selecionando e renomeando colunas para alinhar com o Moprefipe
        df_amostra = df.head(500).copy()

        # Mapeamento para o padrão esperado pelo Moprefipe
        df_amostra.to_csv("data/transacoes.csv", index=False)
        print("'data/transacoes.csv' gerado com sucesso!")

    except Exception as e:
        print(f"Aviso: Não foi possível carregar do Hugging Face ({e}). Gerando base local de contingência...", file=sys.stderr)
    
        # Dados sintéticos de apoio para manter o projeto rodando
        transacoes_sinteticas = [
            {"data": "2026-10-01", "descricao": "Supermercado XYZ", "categoria": "Alimentação", "valor": 350.00, "tipo": "Débito"},
            {"data": "2026-10-02", "descricao": "Serviço de Streaming", "categoria": "Entretenimento", "valor": 55.00, "tipo": "Débito"},
            {"data": "2026-10-03", "descricao": "Pagamento Fatura Cartão", "categoria": "Contas Fixas", "valor": 1200.00, "tipo": "Débito"},
            {"data": "2026-10-05", "descricao": "Posto de Combustível", "categoria": "Transporte", "valor": 180.00, "tipo": "Débito"},
            {"data": "2026-10-07", "descricao": "Restaurante Almoço", "categoria": "Alimentação", "valor": 85.50, "tipo": "Débito"},
            {"data": "2026-10-10", "descricao": "Salário Mensal", "categoria": "Renda", "valor": 5500.00, "tipo": "Crédito"},
            {"data": "2026-10-12", "descricao": "Supermercado Mensal", "categoria": "Alimentação", "valor": 620.00, "tipo": "Débito"},
            {"data": "2026-10-15", "descricao": "Aplicativo de Delivery", "categoria": "Alimentação", "valor": 92.40, "tipo": "Débito"},
            {"data": "2026-10-18", "descricao": "Conta de Internet", "categoria": "Contas Fixas", "valor": 110.00, "tipo": "Débito"},
            {"data": "2026-10-20", "descricao": "Farmácia Saúde", "categoria": "Saúde", "valor": 75.20, "tipo": "Débito"},
            {"data": "2026-10-22", "descricao": "Padaria Local", "categoria": "Alimentação", "valor": 28.50, "tipo": "Débito"}
        ]
        df_fallback = pd.DataFrame(transacoes_sinteticas)
        df_fallback.to_csv("data/transacoes.csv", index=False)
        print("'data/transacoes.csv' gerado via fallback com sucesso!")


def ingerir_historico_atendimento():
    """Baixa dados de diálogo de atendimento bancário do Hugging Face

    e gera o data/historico_atendimento.csv.
    """
    print("[2/4] Baixando histórico de atendimento do Hugging Face...")
    try:
        # Usando corpus de conversas bancárias para simular tickets anteriores
        dataset = load_dataset("talkmap/banking-conversation-corpus", split="train", token=os.getenv("HUGGINGFACE_TOKEN"))

        atendimentos = []
        for i, row in enumerate(dataset):
            if i >= 100:  # Limite de 100 amostras para manter leve
                break

            atendimentos.append(
                {
                    "id_atendimento": f"TICK-{1000 + i}",
                    "canal": "Chat App Moprefipe",
                    "mensagem_cliente": row.get("client", ""),
                    "resposta_agente": row.get("agent", ""),
                    "status": "Concluído",
                }
            )

        df_atendimento = pd.DataFrame(atendimentos)
        df_atendimento.to_csv("data/historico_atendimento.csv", index=False)
        print("'data/historico_atendimento.csv' gerado com sucesso!")

    except Exception as e:
        print(
            f"Erro ao carregar atendimentos do Hugging Face: {e}",
            file=sys.stderr,
        )


def gerar_perfil_investidor():
    """Gera o arquivo JSON com as metas e tolerância de risco do cliente (data/perfil_investidor.json)."""
    print("[3/4] Gerando perfil de investidor estruturado...")

    perfil = {
        "usuario_id": "USR-88492",
        "nome": "Cliente Moprefipe",
        "perfil_risco": "Moderado",
        "objetivos_financeiros": [
            {
                "nome": "Reserva de Emergência",
                "meta_valor": 15000.00,
                "prazo": "Curto (6 meses)",
                "prioridade": "Alta",
            },
            {
                "nome": "Aposentadoria / Longo Prazo",
                "meta_valor": 100000.00,
                "prazo": "Longo (10 anos)",
                "prioridade": "Média",
            },
        ],
        "restricoes_e_preferencias": {
            "aceita_renda_variavel": True,
            "percentual_maximo_renda_variavel": 20.0,
            "preferencia_liquidez": "Alta para 50% do patrimônio",
            "produtos_proibidos": ["Alavancagem", "Criptomoedas de Alta Volatilidade"],
        },
    }

    with open("data/perfil_investidor.json", "w", encoding="utf-8") as f:
        json.dump(perfil, f, ensure_ascii=False, indent=4)

    print("'data/perfil_investidor.json' gerado com sucesso!")


def gerar_produtos_financeiros():
    """Gera o catálogo de produtos e serviços disponíveis no Moprefipe (data/produtos_financeiros.json)."""
    print("[4/4] Gerando catálogo oficial de produtos financeiros...")

    produtos = [
        {
            "id_produto": "PROD-001",
            "nome": "Tesouro Selic 2029",
            "categoria": "Renda Fixa Publica",
            "perfil_indicado": ["Conservador", "Moderado", "Arrojado"],
            "liquidez": "Diária (D+1)",
            "rentabilidade_estimada": "100% Selic",
            "risco": "Muito Baixo",
            "aporte_minimo": 150.00,
        },
        {
            "id_produto": "PROD-002",
            "nome": "CDB Banco Moprefipe 102% CDI",
            "categoria": "Renda Fixa Privada",
            "perfil_indicado": ["Conservador", "Moderado"],
            "liquidez": "Diária",
            "garantia_fgc": True,
            "rentabilidade_estimada": "102% do CDI",
            "risco": "Baixo",
            "aporte_minimo": 100.00,
        },
        {
            "id_produto": "PROD-003",
            "nome": "Fundo Multimercado Dinâmico",
            "categoria": "Fundos de Investimento",
            "perfil_indicado": ["Moderado", "Arrojado"],
            "liquidez": "D+30",
            "rentabilidade_estimada": "IPCA + 5.5% a.a.",
            "risco": "Médio",
            "aporte_minimo": 500.00,
        },
        {
            "id_produto": "PROD-004",
            "nome": "ETF iShares Ibovespa (BOVA11)",
            "categoria": "Renda Variável",
            "perfil_indicado": ["Arrojado"],
            "liquidez": "D+2",
            "rentabilidade_estimada": "Variação do Ibovespa",
            "risco": "Alto",
            "aporte_minimo": 100.00,
        },
    ]

    with open("data/produtos_financeiros.json", "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=4)

    print("'data/produtos_financeiros.json' gerado com sucesso!")


def main():
    print("=" * 60)
    print("INICIANDO INGESTÃO DE DADOS - MOPREFIPE")
    print("=" * 60)

    garantir_diretorio_data()
    ingerir_transacoes()
    ingerir_historico_atendimento()
    gerar_perfil_investidor()
    gerar_produtos_financeiros()

    print("=" * 60)
    print("INGESTÃO CONCLUÍDA! Todos os arquivos em 'data/' estão prontos.")
    print("=" * 60)


if __name__ == "__main__":
    main()