import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Ferias Empresariales en Uruguay",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header con logo y título
logo_url = "https://www.ccsu.org.uy/sites/default/files/logo.png"  # Reemplaza con el URL correcto del logo
st.markdown(
    f"""
    <div style="display:flex; align-items:center;">
        <img src="{logo_url}" width="120" style="margin-right:20px;">
        <h1 style="color:#0B3C5D;">Ferias Empresariales en Uruguay</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<p style="color:#333; font-size:16px;">
Esta plataforma ofrece información sobre las principales ferias y exposiciones en Uruguay para **empresas extranjeras**, facilitando oportunidades de networking y negocios.
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# Cargar CSV
df = pd.read_csv("ferias_uruguay.csv")

# Filtros en sidebar para mayor formalidad
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

# Mostrar resultados con formato de tarjeta serio
for _, feria in df_filtrado.iterrows():
    with st.container():
        st.markdown(
            f"""
            <div style="border:1px solid #ccc; padding:15px; border-radius:8px; margin-bottom:15px; background-color:#f9f9f9;">
                <h3 style="color:#0B3C5D;">{feria['Nombre']}</h3>
                <p><strong>Fechas:</strong> {feria['Fecha Inicio']} → {feria['Fecha Fin']}</p>
                <p><strong>Ubicación:</strong> {feria['Ciudad']} – {feria['Venue']}</p>
                <p><strong>Sector:</strong> {feria['Sector']}</p>
                <p><strong>Perfil de participantes:</strong> {feria['Perfil Participantes']}</p>
                <p><strong>Idiomas disponibles:</strong> {feria['Idioma']}</p>
                <a href="{feria['Sitio Oficial']}" target="_blank" style="text-decoration:none;">
                    <div style="text-align:center; background-color:#0B3C5D; color:white; padding:8px 0; border-radius:5px; width:180px;">Más información</div>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
