# app.py
import streamlit as st
from utils.sheets_helper import carregar_dados, inserir_ocorrencia, conectar
from utils.pdf_generator import gerar_pdf

st.set_page_config(page_title="Sistema GCM Guarulhos", layout="wide")

# Testa conexão
try:
    conectar()
    st.success("✅ Conectado à planilha Google Sheets!")
except Exception as e:
    st.error("Erro ao conectar à planilha:")
    st.exception(e)
    st.stop()

# Banco de usuários
USUARIOS = {
    "base1": "senha1",
    "base2": "senha2",
    "base3": "senha3",
    "base4": "senha4",
    "base5": "senha5",
    "base6": "senha6",
    "base7": "senha7",
    "base8": "senha8",
    "mestre": "master123"
}

def login():
    st.title("🔐 Sistema GCM Guarulhos")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            st.session_state["login"] = usuario
            st.success(f"Bem-vindo(a), {usuario}!")
        else:
            st.error("Usuário ou senha inválidos")
    if "login" not in st.session_state or st.session_state["login"] is None:
        st.stop()

def main():
    login()
    usuario = st.session_state["login"]

    st.sidebar.title("📋 Menu")
    if usuario == "mestre":
        opcao = st.sidebar.selectbox("Escolha:", ["Ver dados", "Gerar PDF"])
    else:
        opcao = st.sidebar.selectbox("Escolha:", ["Registrar serviço", "Gerar PDF"])

    if opcao == "Registrar serviço":
        st.header("📌 Registrar Dia de Serviço")
        with st.form("form_servico", clear_on_submit=True):
            data = st.date_input("Data")
            natureza1 = st.text_input("Natureza 1")
            qtd1 = st.number_input("Qtde 1", min_value=0, value=0)
            natureza2 = st.text_input("Natureza 2")
            qtd2 = st.number_input("Qtde 2", min_value=0, value=0)
            natureza3 = st.text_input("Natureza 3")
            qtd3 = st.number_input("Qtde 3", min_value=0, value=0)
            observacoes = st.text_area("Observações")
            responsavel = st.text_input("Responsável pelo preenchimento")
            cf = st.text_input("C.F.")
            latitude = st.text_input("Latitude")
            longitude = st.text_input("Longitude")

            enviar = st.form_submit_button("Enviar")
            if enviar:
                registro = {
                    "data": data.strftime("%d/%m/%Y"),
                    "natureza1": natureza1,
                    "qtd1": qtd1,
                    "natureza2": natureza2,
                    "qtd2": qtd2,
                    "natureza3": natureza3,
                    "qtd3": qtd3,
                    "observacoes": observacoes,
                    "responsavel": responsavel,
                    "cf": cf,
                    "latitude": latitude,
                    "longitude": longitude
                }
                try:
                    if inserir_ocorrencia(registro, usuario):
                        st.success("✅ Registro enviado com sucesso!")
                    else:
                        st.error("Erro ao registrar dados.")
                except Exception as e:
                    st.error("Erro inesperado ao registrar:")
                    st.exception(e)

    elif opcao == "Gerar PDF":
        st.header("📄 Relatório PDF")
        dados = carregar_dados("todas" if usuario == "mestre" else usuario)
        if not dados.empty:
            pdf = gerar_pdf(dados)
            st.download_button("📥 Baixar PDF", pdf, "relatorio_servico.pdf", "application/pdf")
        else:
            st.warning("Nenhum dado disponível.")

    elif opcao == "Ver dados" and usuario == "mestre":
        st.header("📊 Dados de todas as bases")
        dados = carregar_dados("todas")
        st.dataframe(dados)

if __name__ == "__main__":
    if "login" not in st.session_state:
        st.session_state["login"] = None
    main()
