import streamlit as st
from utils.pdf_generator import gerar_pdf
from utils.sheets_helper import carregar_dados, inserir_ocorrencia

st.set_page_config(page_title="Sistema GCM Guarulhos", layout="wide")

USUARIOS = {
    "base1": "senha1",
    "base2": "senha2",
    "mestre": "master123"
}

def login():
    st.title("Login - Sistema GCM Guarulhos")
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
    user = st.session_state["login"]

    st.sidebar.title("Menu")
    if user == "mestre":
        opc = st.sidebar.selectbox("Escolha:", ["Ver dados", "Gerar relatório PDF"])
    else:
        opc = st.sidebar.selectbox("Escolha:", ["Enviar ocorrência", "Gerar relatório PDF"])

    if opc == "Enviar ocorrência":
        st.header("Registrar Ocorrência")

        with st.form("form_ocorrencia", clear_on_submit=True):
            data = st.date_input("Data")
            horario = st.time_input("Horário")
            local = st.text_input("Local")
            tipo = st.selectbox("Tipo", ["Abordagem", "Veículo Recolhido", "Crime", "Prisão em Flagrante", "Procurado Capturado"])
            observacoes = st.text_area("Observações")
            latitude = st.text_input("Latitude (ex: -23.4543)")
            longitude = st.text_input("Longitude (ex: -46.5333)")

            enviar = st.form_submit_button("Enviar")
            if enviar:
                registro = {
                    "data": data.strftime("%d/%m/%Y"),
                    "horario": horario.strftime("%H:%M:%S"),
                    "local": local,
                    "base": user,
                    "tipo": tipo,
                    "observacoes": observacoes,
                    "latitude": latitude,
                    "longitude": longitude
                }
                if inserir_ocorrencia(registro, user):
                    st.success("Ocorrência registrada com sucesso!")
                else:
                    st.error("Erro ao registrar ocorrência.")

    elif opc == "Gerar relatório PDF":
        dados = carregar_dados("todas" if user == "mestre" else user)
        if not dados.empty:
            pdf_bytes = gerar_pdf(dados)
            st.download_button("Baixar PDF", pdf_bytes, "relatorio_ocorrencias.pdf", "application/pdf")
        else:
            st.info("Nenhuma ocorrência encontrada.")

    elif opc == "Ver dados" and user == "mestre":
        dados = carregar_dados("todas")
        st.dataframe(dados)

if __name__ == "__main__":
    if "login" not in st.session_state:
        st.session_state["login"] = None
    main()
