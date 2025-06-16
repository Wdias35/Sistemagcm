import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# 1) Defina os scopes antes de usar
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

class SheetsHelper:
    def __init__(self):
        # 2) Leia o dicionário de credenciais direto do secrets.toml
        creds_dict = st.secrets["creds"]

        # 3) Crie o objeto de credencial com os scopes
        credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

        # 4) Autentique-se com gspread
        client = gspread.authorize(credentials)

        # 5) Pegue o sheet_id do secrets
        sheet_id = st.secrets["sheet_id"]

        # 6) Abra a planilha
        self.sheet = client.open_by_key(sheet_id).sheet1

    def inserir_ocorrencia(self, registro):
        try:
            self.sheet.append_row(list(registro.values()))
            return True
        except Exception:
            return False

    def ler_todas_ocorrencias(self, mestre=False):
        try:
            data = self.sheet.get_all_records()
            return data
        except Exception:
            return []