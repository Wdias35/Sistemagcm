import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SHEET_NAME = "SistemaGCM"
NOME_PLANILHA = "SistemaGCM"

# Conecta com a planilha Google via Streamlit Secrets
def conectar():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["creds"], scopes=scopes)

    #creds = Credentials.from_service_account_info(st.secrets["creds"])
    client = gspread.authorize(creds)
    return client

# Carrega os dados da aba específica (ou todas as abas)
def carregar_dados(base):
    client = conectar()
    planilha = client.open(NOME_PLANILHA)
    dados_finais = []

    if base == "todas":
        for aba in planilha.worksheets():
            valores = aba.get_all_records()
            dados_finais.extend(valores)
    else:
        try:
            aba = planilha.worksheet(base)
            valores = aba.get_all_records()
            dados_finais.extend(valores)
        except:
            pass

    return pd.DataFrame(dados_finais)

# Insere uma nova ocorrência na aba correspondente
def inserir_ocorrencia(dados, base):
    client = conectar()
    planilha = client.open(NOME_PLANILHA)
    aba = planilha.worksheet(base)
    ultima_linha = len(aba.get_all_values()) + 1
    linha = [
        dados["data"],
        dados["horario"],
        dados["local"],
        dados["base"],
        dados["tipo"],
        dados["observacoes"]
    ]
    aba.insert_row(linha, ultima_linha)
    return True
