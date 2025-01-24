import streamlit as st
import folium
from streamlit_folium import st_folium

# Título do aplicativo
st.title("Mapa com Círculo")

# Cria um mapa centrado em uma localização inicial
m = folium.Map(location=[-23.5505, -46.6333], zoom_start=10)

# Adiciona a funcionalidade de desenhar um círculo no mapa
draw = folium.plugins.Draw(
    draw_options={
        "circle": True,
        "circlemarker": False,
        "marker": False,
        "polygon": False,
        "polyline": False,
        "rectangle": False,
    }
)
m.add_child(draw)

# Exibe o mapa no Streamlit
map_data = st_folium(m, width=700, height=500)

# Verifica se um círculo foi desenhado
if map_data.get("last_active_drawing"):
    circle_data = map_data["last_active_drawing"]["geometry"]
    center = circle_data["coordinates"][::-1]  # Inverte para obter [lat, lon]
    radius_meters = map_data["last_active_drawing"]["properties"]["radius"]

    # Converte o raio de metros para quilômetros
    radius_km = radius_meters / 1000

    # Exibe as informações do círculo
    st.write(f"**Centro do Círculo (Lat, Lon):** {center}")
    st.write(f"**Raio do Círculo:** {radius_km:.2f} km")