import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import time
from utils.sheets_helper import carregar_dados

st.set_page_config(page_title="Mapa de Calor", layout="wide")
st.title("🗺️ Mapa de Calor - Ocorrências GCM")

if "login" not in st.session_state or st.session_state["login"] != "mestre":
    st.warning("Acesso permitido apenas para o login mestre.")
    st.stop()

# Carrega dados da planilha
dados = carregar_dados("todas")
if not isinstance(dados, pd.DataFrame) or dados.empty:
    st.info("Nenhuma ocorrência encontrada.")
    st.stop()

geolocator = Nominatim(user_agent="sistema-gcm")
map_data = []

with st.spinner("Gerando coordenadas para os locais informados..."):
    for _, row in dados.iterrows():
        endereco = row.get("local", "")
        if endereco:
            try:
                location = geolocator.geocode(endereco + ", Guarulhos, SP, Brasil")
                if location:
                    map_data.append([location.latitude, location.longitude])
            except:
                continue
            time.sleep(1)

if not map_data:
    st.error("Não foi possível localizar nenhum endereço.")
    st.stop()

m = folium.Map(location=[-23.4786, -46.5272], zoom_start=13)
HeatMap(map_data).add_to(m)

st.success(f"{len(map_data)} ocorrências localizadas.")
st_folium(m, width=800, height=500)
