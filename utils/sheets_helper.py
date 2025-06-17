# ✅ utils/sheets_helper.py
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st

SHEET_NAME = "SistemaGcm"

@st.cache_resource
def conectar():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["creds"]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(credentials)
    return client

def carregar_dados(base):
    try:
        client = conectar()
        planilha = client.open(SHEET_NAME)
        aba = planilha.worksheet(base)
        dados = aba.get_all_records()
        return pd.DataFrame(dados)
    except Exception as e:
        print("Erro ao carregar dados:", e)
        return pd.DataFrame()

def inserir_ocorrencia(ocorrencia, base):
    try:
        client = conectar()
        planilha = client.open(SHEET_NAME)
        try:
            aba = planilha.worksheet(base)
        except gspread.exceptions.WorksheetNotFound:
            aba = planilha.add_worksheet(title=base, rows="1000", cols="20")
            aba.append_row(["Data", "Horário", "Local", "Base Responsável", "Tipo de Ocorrência", "Observações"])

        aba.append_row([
            ocorrencia["data"],
            ocorrencia["horario"],
            ocorrencia["local"],
            ocorrencia["base"],
            ocorrencia["tipo"],
            ocorrencia["observacoes"]
        ])
        return True
    except Exception as e:
        print("Erro ao inserir ocorrência:", e)
        return False
