import streamlit as st
import folium
from streamlit_folium import st_folium
from utils.sheets_helper import carregar_dados

st.set_page_config(page_title="Mapa de Calor", layout="wide")

st.title("🌍 Mapa de Ocorrências - GCM Guarulhos")

dados = carregar_dados("todas")

if dados.empty:
    st.warning("Nenhuma ocorrência disponível.")
else:
    dados = dados.dropna(subset=["latitude", "longitude"])

    if "latitude" in dados.columns and "longitude" in dados.columns:
        mapa = folium.Map(location=[-23.4645, -46.5325], zoom_start=12)

        for _, linha in dados.iterrows():
            try:
                lat = float(linha["latitude"])
                lon = float(linha["longitude"])
                popup = f"{linha['tipo']} - {linha['data']}"
                folium.Marker(location=[lat, lon], popup=popup).add_to(mapa)
            except:
                continue

        st_folium(mapa, width=1000, height=600)
    else:
        st.warning("Os dados não contêm colunas de latitude e longitude.")
