# app.py
import streamlit as st
from utils.pdf_generator import gerar_pdf
from utils.sheets_helper import carregar_dados, inserir_ocorrencia, conectar

# Configurações iniciais
st.set_page_config(page_title="Sistema GCM Guarulhos", layout="wide")

# Testa conexão com Google Sheets
try:
    conectar()
    st.success("✅ Conectado com sucesso à planilha!")
except Exception as e:
    st.error("❌ Erro ao conectar à planilha:")
    st.exception(e)
    st.stop()

# Banco de usuários (base + login mestre)
USUARIOS = {
    "base1": "senha1",
    "base2": "senha2",
    "mestre": "master123"
}

def login():
    st.title("🔐 Login - Sistema GCM Guarulhos")
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

    st.sidebar.title("📋 Menu")
    if user == "mestre":
        st.sidebar.write("🔑 Login Mestre - acesso total")
        opc = st.sidebar.selectbox("O que deseja fazer?", ["Ver dados", "Gerar relatório PDF"])
    else:
        st.sidebar.write(f"👮‍♂️ Base: {user}")
        opc = st.sidebar.selectbox("O que deseja fazer?", ["Enviar ocorrência", "Gerar relatório PDF"])

    if opc == "Enviar ocorrência":
        st.header("📌 Registrar Ocorrência")

        with st.form("form_ocorrencia", clear_on_submit=True):
            data = st.date_input("Data")
            horario = st.time_input("Horário")
            local = st.text_input("Local")
            base_responsavel = user
            tipo = st.selectbox("Tipo de Ocorrência", [
                "Abordagem", "Veículo Recolhido", "Crime",
                "Prisão em Flagrante", "Procurado Capturado"
            ])
            observacoes = st.text_area("Observações")

            enviar = st.form_submit_button("Enviar")
            if enviar:
                registro = {
                    "data": data.strftime("%d/%m/%Y"),
                    "horario": horario.strftime("%H:%M:%S"),
                    "local": local,
                    "base": base_responsavel,
                    "tipo": tipo,
                    "observacoes": observacoes
                }
                try:
                    sucesso = inserir_ocorrencia(registro, base_responsavel)
                    st.success("✅ Ocorrência registrada com sucesso!")
                except Exception as e:
                    st.error("❌ Erro ao registrar ocorrência:")
                    st.exception(e)

    elif opc == "Gerar relatório PDF":
        st.header("📄 Relatório PDF")
        try:
            dados = carregar_dados("todas" if user == "mestre" else user)
            if not dados.empty:
                pdf_bytes = gerar_pdf(dados)
                st.download_button(
                    label="⬇️ Baixar Relatório PDF",
                    data=pdf_bytes,
                    file_name="relatorio_ocorrencias.pdf",
                    mime="application/pdf"
                )
            else:
                st.info("Nenhuma ocorrência encontrada.")
        except Exception as e:
            st.error("Erro ao gerar relatório:")
            st.exception(e)

    elif opc == "Ver dados" and user == "mestre":
        st.header("📊 Dados de todas as bases")
        try:
            dados = carregar_dados("todas")
            st.dataframe(dados)
        except Exception as e:
            st.error("Erro ao carregar dados:")
            st.exception(e)

if __name__ == "__main__":
    if "login" not in st.session_state:
        st.session_state["login"] = None
    main()
