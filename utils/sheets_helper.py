# sheets_helper.py (corrigido)
import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

NOME_PLANILHA = "SistemaGCM"

# Conecta com a planilha Google via Streamlit Secrets
def conectar():
    creds = Credentials.from_service_account_info(st.secrets["creds"])
    client = gspread.authorize(creds)
    return client

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

import streamlit as st

import streamlit as st

def inserir_ocorrencia(registro, base):
    try:
        client = conectar()
        planilha = client.open(NOME_PLANILHA)
        try:
            aba = planilha.worksheet(base)
        except:
            aba = planilha.add_worksheet(title=base, rows="1000", cols="20")
            cabecalho = list(registro.keys())
            aba.append_row(cabecalho)

        valores = list(registro.values())
        aba.append_row(valores)
        return True
    except Exception as e:
        st.error(f"Erro ao inserir ocorrência: {e}")  # <- mostra o erro na tela
        return False
