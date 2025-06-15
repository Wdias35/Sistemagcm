import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

class SheetsHelper:
    def __init__(self):
        creds_dict = st.secrets["creds"]
        credentials = Credentials.from_service_account_info(creds_dict)
        client = gspread.authorize(credentials)
        self.sheet = client.open_by_key("1K8YAEd9bSBS4W-fMgWQ_uMPfHJF22UFpSe-Ihv5CSnM").sheet1

    def inserir_ocorrencia(self, registro):
        try:
            self.sheet.append_row(list(registro.values()))
            return True
        except:
            return False

    def ler_todas_ocorrencias(self, mestre=False):
        try:
            data = self.sheet.get_all_records()
            if mestre:
                return data
            return data  # Filtragem por base se quiser
        except:
            return []
