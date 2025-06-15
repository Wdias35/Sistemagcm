from google.oauth2.service_account import Credentials
import gspread
import streamlit as st

class SheetsHelper:
    def __init__(self):
        # Pega o dict do secrets
        creds_dict = st.secrets["creds"]
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(st.secrets["creds"], scopes=scopes)

        client = gspread.authorize(creds)

        # Pega o ID da planilha também dos secrets
        self.sheet = client.open_by_key(st.secrets["sheet_id"]).sheet1

    def inserir_ocorrencia(self, dados):
        try:
            self.sheet.append_row(list(dados.values()))
            return True
        except Exception as e:
            st.error(f"Erro ao inserir ocorrência: {e}")
            return False

    def ler_todas_ocorrencias(self, mestre=False):
        try:
            dados = self.sheet.get_all_records()
            if mestre:
                return dados
            else:
                # Filtro por base
                base = st.session_state["login"]
                return [d for d in dados if d["Base Responsável"] == base]
        except Exception as e:
            st.error(f"Erro ao ler ocorrências: {e}")
            return []
