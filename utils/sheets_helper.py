# utils/sheets_helper.py
import gspread
#from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd

def autenticar():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["creds"], scope)
    client = gspread.authorize(creds)
    return client

def abrir_planilha():
    client = autenticar()
    SHEET_NAME = "SistemaGCM"
    return client.open(SHEET_NAME)

def carregar_dados(nome_aba):
    planilha = abrir_planilha()
    try:
        aba = planilha.worksheet(nome_aba)
    except gspread.WorksheetNotFound:
        aba = planilha.add_worksheet(title=nome_aba, rows="100", cols="10")
        cabecalhos = ["Data", "Horário", "Local", "Base Responsável", "Tipo de Ocorrência", "Observações"]
        aba.append_row(cabecalhos)
    dados = aba.get_all_records()
    return pd.DataFrame(dados)

def inserir_ocorrencia(nome_aba, dados):
    planilha = abrir_planilha()
    try:
        aba = planilha.worksheet(nome_aba)
    except gspread.WorksheetNotFound:
        aba = planilha.add_worksheet(title=nome_aba, rows="100", cols="10")
        cabecalhos = ["Data", "Horário", "Local", "Base Responsável", "Tipo de Ocorrência", "Observações"]
        aba.append_row(cabecalhos)
    aba.append_row(list(dados.values()))
    return True
