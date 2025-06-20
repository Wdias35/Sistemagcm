import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils.sheets_helper import carregar_dados

st.set_page_config(page_title="Mapa de Calor - GCM", layout="wide")
st.title("Mapa de Calor das Ocorrências")
@st.cache_data(ttl=60)
def carregar_todos_os_dados():
    return carregar_dados("todas")

dados = carregar_todos_os_dados()


dados = carregar_dados("todas")

if dados.empty:
    st.warning("Nenhuma ocorrência encontrada.")
    st.stop()

# Filtrar dados válidos
dados = dados[dados['latitude'].notnull() & dados['longitude'].notnull()]
dados = dados[dados['latitude'] != ""]
dados = dados[dados['longitude'] != ""]

if dados.empty:
    st.warning("Nenhum dado com latitude/longitude válido.")
    st.stop()

# Criar mapa
mapa = folium.Map(location=[-23.4695, -46.5254], zoom_start=12)

for _, linha in dados.iterrows():
    try:
        lat = float(linha['latitude'])
        lon = float(linha['longitude'])
        folium.CircleMarker(
            location=[lat, lon],
            radius=6,
            fill=True,
            color="blue",
            fill_opacity=0.6,
            popup=f"{linha['tipo']} - {linha['local']}"
        ).add_to(mapa)
    except:
        continue

st_folium(mapa, width=1000, height=600)

