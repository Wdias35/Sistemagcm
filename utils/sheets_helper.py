import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from utils.sheets_helper import sheetsHelper
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = 'SEU_ID_DA_PLANILHA_AQUI'  # Substitua pelo ID da sua planilha

class SheetsHelper:
    def __init__(self):
        creds = Credentials.from_service_account_file('creds.json', scopes=SCOPES)
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

    def ler_todas_ocorrencias(self, mestre=False):
        try:
            dados = self.sheet.get_all_records()
            df = pd.DataFrame(dados)
            if not mestre:
                # Filtar por base responsável se não for mestre
                if 'Base Responsável' in df.columns:
                    df = df[df['Base Responsável'] == 'base1']  # Ajuste conforme usuário logado
            return df
        except Exception as e:
            print("Erro ao ler dados:", e)
            return pd.DataFrame()
