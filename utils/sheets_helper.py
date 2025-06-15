import streamlit as st
import gspread
import pandas as pd
from google.oauth2 import service_account

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Usar o secrets direto
creds_dict = st.secrets["creds"]
creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

SPREADSHEET_ID = st.secrets["spreadsheet_id"]  # Vamos guardar no secrets

class SheetsHelper:
    def __init__(self):
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(SPREADSHEET_ID).sheet1

    def inserir_ocorrencia(self, registro: dict):
        try:
            linha = [
                registro["Data"],
                registro["Horário"],
                registro["Local"],
                registro["Base Responsável"],
                registro["Tipo de Ocorrência"],
                registro["Observações"]
            ]
            self.sheet.append_row(linha)
            return True
        except Exception as e:
            print("Erro ao inserir:", e)
            return False

    def ler_todas_ocorrencias(self, mestre=False, base=None):
        try:
            dados = self.sheet.get_all_records()
            df = pd.DataFrame(dados)
            if not mestre and base:
                df = df[df['Base Responsável'] == base]
            return df
        except Exception as e:
            print("Erro ao ler dados:", e)
            return pd.DataFrame()
