import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_ID = "SEU_ID_DA_PLANILHA_AQUI"
RANGE_BASES = "Página1"  # ou o nome da aba

creds = Credentials.from_service_account_file("creds.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID)

def inserir_ocorrencia(ocorrencia, base):
    try:
        aba = sheet.worksheet(base) if base != "mestre" else sheet.worksheet("Página1")
        aba.append_row([
            ocorrencia["data"],
            ocorrencia["horario"],
            ocorrencia["local"],
            ocorrencia["base"],
            ocorrencia["tipo"],
            ocorrencia["observacoes"]
        ])
        return True
    except Exception as e:
        print("Erro ao inserir:", e)
        return False

def carregar_dados(base):
    try:
        if base == "mestre" or base == "todas":
            dados_completos = []
            for aba in sheet.worksheets():
                linhas = aba.get_all_values()
                if linhas:
                    df = pd.DataFrame(linhas[1:], columns=linhas[0])
                    dados_completos.append(df)
            if dados_completos:
                return pd.concat(dados_completos, ignore_index=True)
            return pd.DataFrame()
        else:
            aba = sheet.worksheet(base)
            linhas = aba.get_all_values()
            if not linhas:
                return pd.DataFrame()
            return pd.DataFrame(linhas[1:], columns=linhas[0])
    except Exception as e:
        print("Erro ao carregar dados:", e)
        return pd.DataFrame()
