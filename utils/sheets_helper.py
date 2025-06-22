import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import streamlit as st

NOME_PLANILHA = "SistemaGCM"

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

        cabecalho_atual = aba.row_values(1)
        if not cabecalho_atual:
            aba.append_row(list(registro.keys()))
        elif cabecalho_atual != list(registro.keys()):
            st.error("❌ Cabeçalho da planilha não está compatível com o sistema.")
            return False

        valores = list(registro.values())
        aba.append_row(valores)
        return True
    except Exception as e:
        st.error(f"Erro ao inserir ocorrência: {e}")
        return False
