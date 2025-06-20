import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Nome da planilha no Google Sheets
NOME_PLANILHA = "SistemaGCM"

# Conecta com a planilha usando credenciais do Streamlit Secrets
def conectar():
    creds = Credentials.from_service_account_info(st.secrets["creds"])
    client = gspread.authorize(creds)
    return client

# Carrega os dados da aba específica (base) ou de todas
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

# Insere nova ocorrência com todos os campos, incluindo latitude e longitude
def inserir_ocorrencia(registro, base):
    try:
        client = conectar()
        planilha = client.open(NOME_PLANILHA)
def inserir_ocorrencia(registro, base):
    try:
        client = conectar()
        planilha = client.open(NOME_PLANILHA)

        # Tenta acessar a aba da base
        try:
            aba = planilha.worksheet(base)
            # Se a aba estiver vazia (sem cabeçalho), recria
            if not aba.get_all_values():
                cabecalho = ["data", "horario", "local", "base", "tipo", "observacoes", "latitude", "longitude"]
                aba.append_row(cabecalho)
        except:
            aba = planilha.add_worksheet(title=base, rows="1000", cols="20")
            cabecalho = ["data", "horario", "local", "base", "tipo", "observacoes", "latitude", "longitude"]
            aba.append_row(cabecalho)

        # Garante a ordem dos dados
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
        print("Erro ao inserir ocorrência:", e)
        return False
