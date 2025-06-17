
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Define escopos de acesso ao Google Sheets e Drive
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Lê as credenciais do st.secrets
creds_dict = st.secrets["creds"]
credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

# Autentica com o Google Sheets
client = gspread.authorize(credentials)

# Nome da planilha central
SHEET_NAME = "SistemaGCM"

def abrir_planilha():
    """Abre e retorna a planilha principal"""
    return client.open(SHEET_NAME)

def carregar_dados(nome_aba):
    """Carrega dados de uma aba específica"""
    planilha = abrir_planilha()
    aba = planilha.worksheet(nome_aba)
    return aba.get_all_records()

def adicionar_ocorrencia(nome_aba, dados):
    """Adiciona uma nova ocorrência na aba"""
    planilha = abrir_planilha()
    aba = planilha.worksheet(nome_aba)
    aba.append_row(dados)

def obter_bases():
    """Retorna os nomes de todas as abas (bases)"""
    planilha = abrir_planilha()
    return [aba.title for aba in planilha.worksheets()]
