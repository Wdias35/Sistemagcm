import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SHEET_IDS = st.secrets["planilhas"]  # <- novo trecho

def autenticar():
    creds = Credentials.from_service_account_info(st.secrets["creds"], scopes=SCOPE)
    client = gspread.authorize(creds)
    return client

def abrir_planilha():
    login = st.session_state.get("login")  # login da base (ex: base1)
    sheet_id = SHEET_IDS.get(login)
    if not sheet_id:
        raise Exception(f"ID da planilha não encontrado para o login: {login}")
    client = autenticar()
    return client.open_by_key(sheet_id)

def carregar_dados():
    planilha = abrir_planilha()
    aba = planilha.worksheet("Ocorrências")
    dados = aba.get_all_records()
    return dados

def inserir_ocorrencia(dados):
    planilha = abrir_planilha()
    aba = planilha.worksheet("Ocorrências")
    aba.append_row(dados)
    return True
