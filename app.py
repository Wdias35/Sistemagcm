import streamlit as st
from utils.sheets_helper import carregar_dados, inserir_ocorrencia
from datetime import datetime

st.set_page_config(page_title="Sistema GCM Guarulhos", layout="wide")
st.title("🔐 Login - Sistema GCM Guarulhos")

with st.form("login"):
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    login_btn = st.form_submit_button("Entrar")

usuarios_validos = {"base1": "123", "base2": "456", "base3": "789"}

if login_btn:
    if usuario in usuarios_validos and senha == usuarios_validos[usuario]:
        st.success(f"Bem-vindo(a), {usuario}!")

        aba = st.sidebar.radio("Escolha uma opção", ["Registrar Ocorrência", "Visualizar Dados"])

        if aba == "Registrar Ocorrência":
            st.subheader("📋 Registrar Nova Ocorrência")
            with st.form("form_ocorrencia"):
                data = st.date_input("Data", value=datetime.now().date())
                horario = st.time_input("Horário", value=datetime.now().time())
                local = st.text_input("Local")
                tipo = st.selectbox("Tipo de Ocorrência", ["Abordagem", "Veículo Recolhido", "Crime", "Prisão em Flagrante", "Procurado Capturado"])
                obs = st.text_area("Observações")
                enviar = st.form_submit_button("Salvar Ocorrência")

            if enviar:
                registro = {
                    "Data": str(data),
                    "Horário": str(horario),
                    "Local": local,
                    "Base Responsável": usuario,
                    "Tipo de Ocorrência": tipo,
                    "Observações": obs
                }
                sucesso = inserir_ocorrencia(registro)
                if sucesso:
                    st.success("Ocorrência registrada com sucesso!")
                else:
                    st.error("Erro ao registrar ocorrência.")

        elif aba == "Visualizar Dados":
            st.subheader("📊 Ocorrências da sua Base")
            df = carregar_dados(usuario)
            st.dataframe(df)
    else:
        st.error("Usuário ou senha inválidos.")
