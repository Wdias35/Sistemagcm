# ✅ app.py
import streamlit as st
import pandas as pd
from utils.sheets_helper import carregar_dados, inserir_ocorrencia
from utils.pdf_generator import gerar_pdf

def login():
    st.title("Login - Sistema GCM Guarulhos")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        if usuario and senha:
            st.session_state.usuario = usuario
            st.success(f"Bem-vindo(a), {usuario}!")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos")

def logout():
    if st.sidebar.button("🔒 Sair"):
        st.session_state.clear()
        st.experimental_rerun()

def montar_formulario():
    st.subheader("📋 Registrar Ocorrência")
    data = st.date_input("Data")
    horario = st.time_input("Horário")
    local = st.text_input("Local")
    tipo = st.selectbox("Tipo de Ocorrência", [
        "Abordagem", "Veículo Recolhido", "Crime", "Prisão em Flagrante", "Procurado Capturado"])
    observacoes = st.text_area("Observações")

    if st.button("✅ Registrar Ocorrência"):
        registro = {
            "data": str(data),
            "horario": str(horario),
            "local": local,
            "base": st.session_state.usuario,
            "tipo": tipo,
            "observacoes": observacoes
        }
        sucesso = inserir_ocorrencia(registro, st.session_state.usuario)
        if sucesso:
            st.success("Ocorrência registrada com sucesso!")
        else:
            st.error("Erro ao registrar ocorrência.")

def visualizar_dados():
    st.subheader("📊 Ocorrências Registradas")

    if st.session_state.usuario == "mestre":
        dados = carregar_dados("todas")
    else:
        dados = carregar_dados(st.session_state.usuario)

    if dados is not None and not dados.empty:
        st.dataframe(dados, use_container_width=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.download_button("📥 Exportar como PDF", gerar_pdf(dados), file_name="relatorio_ocorrencias.pdf"):
                st.success("PDF gerado com sucesso!")
        with col2:
            st.download_button("📥 Baixar CSV", dados.to_csv(index=False).encode('utf-8'), file_name="ocorrencias.csv")
    else:
        st.info("Nenhuma ocorrência registrada ainda.")

def main():
    st.set_page_config(page_title="Sistema GCM Guarulhos", layout="wide")
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Bras%C3%A3o_de_Guarulhos.svg/1200px-Bras%C3%A3o_de_Guarulhos.svg.png", width=100)
    st.sidebar.title("📌 Menu")
    
    if "usuario" not in st.session_state:
        login()
        return

    st.sidebar.success(f"Usuário: {st.session_state.usuario}")
    logout()

    st.title(f"🔐 Sistema GCM Guarulhos - Base: {st.session_state.usuario}")
    st.markdown("---")

    montar_formulario()
    st.markdown("---")
    visualizar_dados()

if __name__ == "__main__":
    main()
