import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from utils.sheets_helper import carregar_dados
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

st.set_page_config(page_title="Mapa de Calor - GCM", layout="wide")

st.title("Mapa de Calor das Ocorrências")

# Carrega os dados
user = st.session_state.get("login", "base1")  # padrão se não estiver logado
dados = carregar_dados("todas" if user == "mestre" else user)

if dados.empty:
    st.warning("Nenhuma ocorrência encontrada para gerar o mapa.")
    st.stop()

# Inicializa geolocalizador
geolocator = Nominatim(user_agent="sistemagcm-mapa")

@st.cache_data(show_spinner=False)
def geocodificar(endereco):
    try:
        local = geolocator.geocode(endereco + ", Guarulhos, SP", timeout=10)
        if local:
            return (local.latitude, local.longitude)
    except GeocoderTimedOut:
        pass
    return None

# Gera coordenadas
st.info("Gerando coordenadas geográficas...")

heat_data = []
erros = 0

for idx, row in dados.iterrows():
    endereco = row.get("local", "")
    coords = geocodificar(endereco)
    if coords:
        heat_data.append(coords)
    else:
        erros += 1

if not heat_data:
    st.error("❌ Não foi possível localizar nenhum endereço. Verifique se os locais das ocorrências estão completos, como:\n\n`Rua Exemplo, 123 - Guarulhos, SP`")
    st.stop()

# Cria o mapa
mapa = folium.Map(location=[-23.4694, -46.5765], zoom_start=12)
HeatMap(heat_data).add_to(mapa)

st.success(f"✔️ {len(heat_data)} locais geocodificados com sucesso.")
if erros:
    st.warning(f"Aviso: {erros} locais não foram encontrados.")

# Exibe o mapa
st_folium(mapa, width=1000, height=600)
