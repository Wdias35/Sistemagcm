import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils.sheets_helper import carregar_dados

st.set_page_config(page_title="Mapa de Calor GCM", layout="wide")
st.title("🌍 Mapa de Calor das Ocorrências")

# Carrega os dados
user = st.session_state.get("login", None)
if not user:
    st.warning("Por favor, faça login na página principal.")
    st.stop()

dados = carregar_dados("todas" if user == "mestre" else user)

# Simulador de coordenadas (caso não tenha latitude/longitude na planilha)
# ATENÇÃO: isso é apenas ilustrativo para gerar o mapa
import random
def gerar_coords_fake(local):
    random.seed(local)  # mesma cidade/rua gera mesmos pontos
    lat = -23.47 + random.uniform(-0.02, 0.02)
    lon = -46.52 + random.uniform(-0.02, 0.02)
    return lat, lon

# Adiciona coordenadas simuladas
if "latitude" not in dados.columns or "longitude" not in dados.columns:
    latitudes = []
    longitudes = []
    for _, row in dados.iterrows():
        lat, lon = gerar_coords_fake(row.get("local", "Guarulhos"))
        latitudes.append(lat)
        longitudes.append(lon)
    dados["latitude"] = latitudes
    dados["longitude"] = longitudes

# Gera o mapa
m = folium.Map(location=[-23.47, -46.52], zoom_start=12)

from folium.plugins import Heat
