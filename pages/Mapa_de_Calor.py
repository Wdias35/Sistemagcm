import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
from utils.sheets_helper import carregar_dados

st.set_page_config(page_title="Mapa de Calor - GCM Guarulhos", layout="wide")
st.title("🌍 Mapa de Calor de Ocorrências")

@st.cache_data(ttl=60)
def carregar_ocorrencias():
    return carregar_dados("todas")

try:
    df = carregar_ocorrencias()

    if df.empty:
        st.warning("Nenhuma ocorrência encontrada.")
        st.stop()

    # Verifica se há colunas de latitude e longitude
    if "latitude" not in df.columns or "longitude" not in df.columns:
        st.error("❌ As colunas 'latitude' e 'longitude' não estão presentes na planilha.")
        st.stop()

    # Remove entradas inválidas
    df = df.dropna(subset=["latitude", "longitude"])
    df = df[df["latitude"].astype(str).str.strip() != ""]
    df = df[df["longitude"].astype(str).str.strip() != ""]

    # Converte para float (garante que são números)
    try:
        df["latitude"] = df["latitude"].astype(float)
        df["longitude"] = df["longitude"].astype(float)
    except:
        st.error("❌ Não foi possível converter latitude/longitude para número.")
        st.stop()

    if df.empty:
        st.warning("Nenhuma ocorrência com coordenadas válidas.")
        st.stop()

    # Cria mapa centrado na média das coordenadas
    mapa = folium.Map(
        location=[df["latitude"].mean(), df["longitude"].mean()],
        zoom_start=12
    )

    # Adiciona pontos ao mapa
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=5,
            popup=f"{row['tipo']} - {row['local']}",
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.6
        ).add_to(mapa)

    st.success(f"✅ {len(df)} ocorrências plotadas no mapa.")
    folium_static(mapa, width=1000, height=600)

except Exception as e:
    st.error("❌ Erro ao carregar o mapa:")
    st.exception(e)

