import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_NAME = "SistemaGCM"

@st.cache_resource
def autenticar():
    creds_info = st.secrets["creds"]
    credentials = Credentials.from_service_account_info(creds_info, scopes=SCOPE)
    client = gspread.authorize(credentials)
    return client

def abrir_planilha():
    client = autenticar()
    return client.open(SHEET_NAME)

def carregar_dados(nome_base):
    try:
        planilha = abrir_planilha()
        aba = planilha.worksheet(nome_base)
        dados = aba.get_all_records()
        df = pd.DataFrame(dados)
        return df
    except gspread.exceptions.WorksheetNotFound:
        planilha = abrir_planilha()
        cabecalho = ["Data", "Horário", "Local", "Base Responsável", "Tipo de Ocorrência", "Observações"]
        planilha.add_worksheet(title=nome_base, rows="1000", cols=str(len(cabecalho)))
        aba = planilha.worksheet(nome_base)
        aba.append_row(cabecalho)
        return pd.DataFrame(columns=cabecalho)

def inserir_ocorrencia(dados):
    try:
        planilha = abrir_planilha()
        aba = planilha.worksheet(dados["Base Responsável"])
        nova_linha = [
            dados["Data"],
            dados["Horário"],
            dados["Local"],
            dados["Base Responsável"],
            dados["Tipo de Ocorrência"],
            dados["Observações"]
        ]
        aba.append_row(nova_linha)
        return True
    except Exception as e:
        print(f"Erro ao inserir ocorrência: {e}")
        return False

