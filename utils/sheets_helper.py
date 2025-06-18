import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import streamlit as st  # ok aqui, desde que usado com cuidado

# Nome da planilha no Google Sheets
NOME_PLANILHA = "SistemaGCM"

def conectar():
    creds = Credentials.from_service_account_info(st.secrets["creds"])
    client = gspread.authorize(creds)
    return client

def carregar_dados(base):
    try:
        client = conectar()
        planilha = client.open(NOME_PLANILHA)
        dados_finais = []

        if base == "todas":
            for aba in planilha.worksheets():
                valores = aba.get_all_records()
                dados_finais.extend(valores)
        else:
            aba = planilha.worksheet(base)
            valores = aba.get_all_records()
            dados_finais.extend(valores)

        return pd.DataFrame(dados_finais)

    except Exception as e:
        # Em vez de usar st.error(), apenas levanta o erro para o app.py tratar
        raise RuntimeError(f"Erro ao carregar dados: {e}")

def inserir_ocorrencia(registro, base):
    try:
        client = conectar()
        planilha = client.open(NOME_PLANILHA)

        try:
            aba = planilha.worksheet(base)
        except gspread.exceptions.WorksheetNotFound:
            aba = planilha.add_worksheet(title=base, rows="1000", cols="20")
            cabecalho = list(registro.keys())
            aba.append_row(cabecalho)

        valores = list(registro.values())
        aba.append_row(valores)
        return True

    except Exception as e:
        raise RuntimeError(f"Erro ao inserir ocorrência: {e}")
