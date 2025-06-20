import altair as alt
import streamlit as st
import pandas as pd
import pydeck as pdk
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

# Banco de usuários
USUARIOS = {
    "base1": "senha1",
    "base2": "senha2",
    "base3": "senha3",
    "base4": "senha4",
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

def exibir_mapa(dados):
    st.header("🗺️ Visualização Geográfica")
    mapa_tipo = st.sidebar.radio("Tipo de mapa", ["Mapa de Calor", "Mapa com Pontos"])
    dados_geo = dados.copy()
    dados_geo = dados_geo[(dados_geo["latitude"] != "") & (dados_geo["longitude"] != "")]
    dados_geo["latitude"] = pd.to_numeric(dados_geo["latitude"], errors="coerce")
    dados_geo["longitude"] = pd.to_numeric(dados_geo["longitude"], errors="coerce")
    dados_geo = dados_geo.dropna(subset=["latitude", "longitude"])

    if dados_geo.empty:
        st.warning("⚠️ Nenhum dado geográfico disponível.")
        return

    if mapa_tipo == "Mapa de Calor":
        layer = pdk.Layer(
            "HeatmapLayer",
            data=dados_geo,
            get_position='[longitude, latitude]',
            aggregation=pdk.types.String("MEAN"),
            get_weight=1,
            radiusPixels=60,
        )
    else:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=dados_geo,
            get_position='[longitude, latitude]',
            get_radius=100,
            get_fill_color='[200, 30, 0, 160]',
            pickable=True,
        )

    view_state = pdk.ViewState(
        latitude=-23.4545,
        longitude=-46.5333,
        zoom=11,
        pitch=0
    )

    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

def main():
    login()
    user = st.session_state["login"]

    st.sidebar.title("📋 Menu")
    if user == "mestre":
        st.sidebar.write("🔑 Login Mestre - acesso total")
        opc = st.sidebar.selectbox("O que deseja fazer?", ["Ver dados", "Dashboard", "Gerar relatório PDF"])
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
            latitude = st.text_area("Latitude")
            longitude = st.text_area("Longitude")

            enviar = st.form_submit_button("Enviar")
            if enviar:
                registro = {
                    "data": data.strftime("%d/%m/%Y"),
                    "horario": horario.strftime("%H:%M:%S"),
                    "local": local,
                    "base": base_responsavel,
                    "tipo": tipo,
                    "observacoes": observacoes,
                    "latitude": latitude,
                    "longitude": longitude
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
                st.write("Prévia dos dados do relatório")
                st.dataframe(dados)

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
            exibir_mapa(dados)
        except Exception as e:
            st.error("Erro ao carregar dados:")
            st.exception(e)

    elif opc == "Dashboard" and user == "mestre":
        st.header("📈 Dashboard de Ocorrências")
        try:
            dados = carregar_dados("todas")
            dados["data"] = pd.to_datetime(dados["data"], format="%d/%m/%Y", errors="coerce")

            st.subheader("Ocorrências por Tipo")
            chart_tipo = alt.Chart(dados).mark_bar().encode(
                x=alt.X("tipo", title="Tipo de Ocorrência"),
                y=alt.Y("count()", title="Quantidade"),
                tooltip=["tipo", "count()"]
            ).properties(width=600)
            st.altair_chart(chart_tipo)

            st.subheader("Ocorrências por Base")
            chart_base = alt.Chart(dados).mark_bar(color="orange").encode(
                x=alt.X("base", title="Base Responsável"),
                y=alt.Y("count()", title="Quantidade"),
                tooltip=["base", "count()"]
            ).properties(width=600)
            st.altair_chart(chart_base)

            st.subheader("Ocorrências por Data")
            chart_data = alt.Chart(dados).mark_bar(color="green").encode(
                x=alt.X("data:T", title="Data"),
                y=alt.Y("count()", title="Total"),
                tooltip=["data", "count()"]
            ).properties(width=700)
            st.altair_chart(chart_data)

        except Exception as e:
            st.error("Erro ao gerar gráficos:")
            st.exception(e)

if __name__ == "__main__":
    if "login" not in st.session_state:
        st.session_state["login"] = None
    main()
