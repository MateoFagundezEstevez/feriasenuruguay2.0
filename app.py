import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración inicial
st.set_page_config(page_title="Ferias Empresariales en Uruguay", layout="wide")

# Leer dataset
df = pd.read_csv("ferias_uruguay.csv")

# Cabecera
st.title("🌎 Ferias Empresariales en Uruguay")
st.markdown("""
Descubre las principales **ferias y exposiciones de Uruguay** para empresas extranjeras.  
Oportunidades de **networking, negocios y expansión internacional** en distintos sectores.
""")

st.markdown("---")

# Filtros
col1, col2, col3 = st.columns(3)

with col1:
    sector = st.selectbox("📌 Filtrar por sector", ["Todos"] + sorted(df["Sector"].unique().tolist()))
with col2:
    ciudad = st.selectbox("📍 Filtrar por ciudad", ["Todos"] + sorted(df["Ciudad"].unique().tolist()))
with col3:
    meses = sorted(set([datetime.strptime(fecha, "%Y-%m-%d").strftime("%B %Y") for fecha in df["Fecha Inicio"]]))
    mes = st.selectbox("📅 Filtrar por mes", ["Todos"] + meses)

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
            st.subheader(f"📌 {feria['Nombre']}")
            colA, colB = st.columns([2, 3])

            with colA:
                st.write(f"📅 **{feria['Fecha Inicio']} → {feria['Fecha Fin']}**")
                st.write(f"📍 **{feria['Ciudad']}** – {feria['Venue']}")
                st.write(f"🏷️ **Sector:** {feria['Sector']}")
                st.write(f"👥 **Perfil de participantes:** {feria['Perfil Participantes']}")
                st.write(f"🌐 **Idiomas disponibles:** {feria['Idioma']}")

            with colB:
                st.markdown(f"[🔗 Más información en el sitio oficial]({feria['Sitio Oficial']})")

            st.markdown("---")
