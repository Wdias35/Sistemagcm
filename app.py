import streamlit as st
from utils.sheets_helper import SheetsHelper
from utils.pdf_generator import gerar_pdf
from datetime import datetime

st.set_page_config(page_title="Sistema GCM Guarulhos", layout="centered")

# Login simples por base
usuarios = {
    "base1": "123",
    "base2": "123",
    "base3": "123",
}

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if st.session_state.usuario is None:
    st.title("Login - Sistema GCM Guarulhos")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario in usuarios and usuarios[usuario] == senha:
            st.session_state.usuario = usuario
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")
else:
    base_logada = st.session_state.usuario
    st.sidebar.success(f"Bem-vindo(a), {base_logada}!")
    sh = SheetsHelper()

    st.title("Registro de Ocorrências - GCM Guarulhos")

    # Exibe dados existentes da base
    try:
        dados = sh.carregar_dados(base_logada)
        st.subheader("Ocorrências registradas")
        st.dataframe(dados)
    except Exception as e:
        st.error("Erro ao carregar os dados da planilha")

    st.subheader("Nova Ocorrência")
    with st.form("form_ocorrencia"):
        data = st.date_input("Data", datetime.today())
        horario = st.time_input("Horário")
        local = st.text_input("Local")
        tipo = st.selectbox("Tipo de Ocorrência", ["Abordagem", "Veículo Recolhido", "Crime", "Prisão em Flagrante", "Procurado Capturado"])
        observacoes = st.text_area("Observações")
        enviar = st.form_submit_button("Enviar")

    if enviar:
        registro = [
            data.strftime("%d/%m/%Y"),
            horario.strftime("%H:%M"),
            local,
            base_logada,
            tipo,
            observacoes
        ]
        try:
            sucesso = sh.inserir_ocorrencia(base_logada, registro)
            if sucesso:
                st.success("Ocorrência registrada com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao registrar ocorrência.")
        except Exception as e:
            st.error(f"Erro ao inserir ocorrência: {e}")

    st.markdown("---")
    st.subheader("Exportar relatório PDF")
    if st.button("Gerar PDF"):
        try:
            gerar_pdf(base_logada, dados)
            with open("relatorio.pdf", "rb") as f:
                st.download_button("Clique para baixar o relatório", f, file_name="relatorio.pdf")
        except:
            st.error("Erro ao gerar PDF.")
