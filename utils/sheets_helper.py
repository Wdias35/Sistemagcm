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
    planilha = client.open(base1)
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
    except Exception as e:
        st.error("Erro ao conectar com o Google Sheets:")
        st.exception(e)
        return False

    try:
        planilha = client.open(NOME_PLANILHA)
    except Exception as e:
        st.error("Erro ao abrir a planilha:")
        st.exception(e)
        return False

    try:
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
        st.error("Erro ao inserir os dados na aba:")
        st.exception(e)
        return False

