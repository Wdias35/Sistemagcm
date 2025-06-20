import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import streamlit as st

# Nome da planilha
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
        except Exception as e:
            st.warning(f"Aba '{base}' não encontrada.")
    
    return pd.DataFrame(dados_finais)

def inserir_ocorrencia(registro, base):
    try:
        client = conectar()
        planilha = client.open(NOME_PLANILHA)
        try:
            aba = planilha.worksheet(base)
        except:
            # Cria a aba com todos os campos esperados
            aba = planilha.add_worksheet(title=base, rows="1000", cols="20")
            cabecalho = ["data", "horario", "local", "base", "tipo", "observacoes", "latitude", "longitude"]
            aba.append_row(cabecalho)

        # Reorganiza os valores na mesma ordem das colunas
        valores = [
            registro.get("data", ""),
            registro.get("horario", ""),
            registro.get("local", ""),
            registro.get("base", ""),
            registro.get("tipo", ""),
            registro.get("observacoes", ""),
            registro.get("latitude", ""),
            registro.get("longitude", "")
        ]
        aba.append_row(valores)
        return True
    except Exception as e:
        st.error(f"Erro ao inserir ocorrência: {e}")
        return False


