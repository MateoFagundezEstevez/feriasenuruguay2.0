import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Ferias Empresariales en Uruguay",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar logo local
logo = Image.open("logo_ccsuy.png")

# Header con logo y título
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo, width=120)
with col2:
    st.markdown(
        '<h1 style="color:#0B3C5D; margin-top:20px;">Ferias Empresariales en Uruguay</h1>',
        unsafe_allow_html=True
    )

# Subtítulo
st.markdown(
    """
    <p style="color:#333; font-size:16px;">
    Plataforma oficial de la Cámara de Comercio y Servicios del Uruguay (CCSUy) para mostrar ferias empresariales en Uruguay.  
    Información para empresas extranjeras interesadas en networking, negocios y expansión internacional.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# Cargar dataset
df = pd.read_csv("ferias_uruguay.csv")

# Sidebar - filtros
st.sidebar.header("Filtros de búsqueda")
sector = st.sidebar.selectbox("Sector", ["Todos"] + sorted(df["Sector"].unique().tolist()))
ciudad = st.sidebar.selectbox("Ciudad", ["Todos"] + sorted(df["Ciudad"].unique().tolist()))
meses = sorted(set([datetime.strptime(fecha, "%Y-%m-%d").strftime("%B %Y") for fecha in df["Fecha Inicio"]]))
mes = st.sidebar.selectbox("Mes", ["Todos"] + meses)

# Aplicar filtros
df_filtrado = df.copy()
if sector != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Sector"] == sector]
if ciudad != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Ciudad"] == ciudad]
if mes != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Fecha Inicio"].apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%B %Y") == mes
    )]

# Mostrar resultados
if df_filtrado.empty:
    st.warning("⚠️ No se encontraron ferias con esos criterios.")
else:
    for _, feria in df_filtrado.iterrows():
        with st.container():
            st.markdown(
                f"""
                <div style="border:1px solid #ccc; padding:20px; border-radius:8px; margin-bottom:15px; background-color:#f9f9f9;">
                    <h3 style="color:#0B3C5D;">{feria['Nombre']}</h3>
                    <p><strong>Fechas:</strong> {feria['Fecha Inicio']} → {feria['Fecha Fin']}</p>
                    <p><strong>Ubicación:</strong> {feria['Ciudad']} – {feria['Venue']}</p>
                    <p><strong>Sector:</strong> {feria['Sector']}</p>
                    <p><strong>Perfil de participantes:</strong> {feria['Perfil Participantes']}</p>
                    <p><strong>Idiomas disponibles:</strong> {feria['Idioma']}</p>
                    <a href="{feria['Sitio Oficial']}" target="_blank" style="text-decoration:none;">
                        <div style="text-align:center; background-color:#0B3C5D; color:white; padding:10px 0; border-radius:5px; width:200px; margin-top:10px;">Más información</div>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
