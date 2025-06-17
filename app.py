# ✅ app.py
import streamlit as st
from utils.sheets_helper import carregar_dados, inserir_ocorrencia

def login():
    st.title("Login - Sistema GCM Guarulhos")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario and senha:
            st.session_state.usuario = usuario
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos")

def montar_formulario():
    st.subheader("Registrar Ocorrência")
    data = st.date_input("Data")
    horario = st.time_input("Horário")
    local = st.text_input("Local")
    tipo = st.selectbox("Tipo de Ocorrência", [
        "Abordagem", "Veículo Recolhido", "Crime", "Prisão em Flagrante", "Procurado Capturado"])
    observacoes = st.text_area("Observações")

    if st.button("Registrar Ocorrência"):
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

def main():
    st.set_page_config(page_title="Sistema GCM Guarulhos", layout="wide")
    if "usuario" not in st.session_state:
        login()
        return

    st.title(f"📄 Sistema GCM - Base: {st.session_state.usuario}")
    montar_formulario()
    dados = carregar_dados(st.session_state.usuario)
    if dados:
        st.subheader("Ocorrências Registradas")
        st.dataframe(dados)

if __name__ == "__main__":
    main()
