import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Escopos de acesso
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Credenciais e autenticação
creds_dict = st.secrets["creds"]
credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
client = gspread.authorize(credentials)

# Nome da planilha
SHEET_NAME = "SistemaGCM"

def abrir_planilha():
    return client.open(SHEET_NAME)

def carregar_dados(nome_aba):
    planilha = abrir_planilha()
    aba = planilha.worksheet(nome_aba)
    return aba.get_all_records()

def inserir_ocorrencia(registro):
    try:
        planilha = abrir_planilha()
        aba = planilha.worksheet("Página1")  # Ou nome da aba que está usando
        aba.append_row([
            registro["Data"],
            registro["Horário"],
            registro["Local"],
            registro["Base Responsável"],
            registro["Tipo de Ocorrência"],
            registro["Observações"]
        ])
        return True
    except Exception as e:
        st.error(f"Erro ao inserir ocorrência: {e}")
        return False

def obter_bases():
    planilha = abrir_planilha()
    return [aba.title for aba in planilha.worksheets()]

def ler_todas_ocorrencias(mestre=False):
    planilha = abrir_planilha()
    abas = planilha.worksheets()
    todas_ocorrencias = []

    for aba in abas:
        if not mestre and aba.title != st.session_state["login"]:
            continue
        dados = aba.get_all_records()
        for d in dados:
            d["Base"] = aba.title
            todas_ocorrencias.append(d)
    
    return todas_ocorrencias
