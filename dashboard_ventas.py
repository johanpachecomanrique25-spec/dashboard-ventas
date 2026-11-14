"""
📈 Dashboard Comercial de Ventas - Streamlit
Ejecutar con: streamlit run dashboard_ventas.py
"""

from io import BytesIO

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ──────────────────────────────────────────────
# Configuración de la página
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Comercial de Ventas",
    page_icon="📈",
    layout="wide",
)

sns.set_style("whitegrid")


# ──────────────────────────────────────────────
# 1. Importación de datos
# ──────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    datos = {
        "Fecha": [
            "2026-01-10", "2026-01-11", "2026-01-12", "2026-01-13",
            "2026-01-14", "2026-01-15", "2026-01-16", "2026-01-17",
        ],
        "Producto": [
            "Laptop", "Mouse", "Teclado", "Monitor",
            "Laptop", "Mouse", "Monitor", "Teclado",
        ],
        "Vendedor": [
            "Ana", "Luis", "Ana", "Carlos",
            "Luis", "Ana", "Carlos", "Luis",
        ],
        "Ventas": [3500, 80, 150, 900, 4200, 100, 950, 180],
        "Cantidad": [1, 2, 1, 1, 1, 3, 1, 2],
    }
    df = pd.DataFrame(datos)
    df["Fecha"] = pd.to_datetime(df["Fecha"])  # 5. Convertir fechas
    return df


df = cargar_datos()

# ──────────────────────────────────────────────
# Barra lateral (filtros)
# ──────────────────────────────────────────────
st.sidebar.header("🎛️ Filtros")

productos = st.sidebar.multiselect(
    "Producto",
    options=sorted(df["Producto"].unique()),
    default=sorted(df["Producto"].unique()),
)

vendedores = st.sidebar.multiselect(
    "Vendedor",
    options=sorted(df["Vendedor"].unique()),
    default=sorted(df["Vendedor"].unique()),
)

rango_fechas = st.sidebar.date_input(
    "Rango de fechas",
    value=(df["Fecha"].min().date(), df["Fecha"].max().date()),
    min_value=df["Fecha"].min().date(),
    max_value=df["Fecha"].max().date(),
)

# Aplicar filtros
df_filtro = df[
    (df["Producto"].isin(productos))
    & (df["Vendedor"].isin(vendedores))
    & (df["Fecha"].dt.date >= rango_fechas[0])
    & (df["Fecha"].dt.date <= rango_fechas[-1])
]

st.sidebar.divider()
buffer = BytesIO()
df_filtro.to_excel(buffer, index=False, engine="openpyxl")
st.sidebar.download_button(
    label="⬇️ Descargar reporte (Excel)",
    data=buffer.getvalue(),
    file_name="reporte_ventas.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

# Si el filtro queda vacío
if df_filtro.empty:
    st.warning("⚠️ No hay datos con los filtros seleccionados.")
    st.stop()

# ──────────────────────────────────────────────
# Título
# ──────────────────────────────────────────────
st.title("📈 Dashboard Comercial de Ventas")
st.caption("Análisis de ventas de la tienda — SENATI")

# ──────────────────────────────────────────────
# 6. KPIs principales
# ──────────────────────────────────────────────
ventas_totales = df_filtro["Ventas"].sum()
unidades = df_filtro["Cantidad"].sum()
ticket_promedio = df_filtro["Ventas"].sum() / df_filtro["Cantidad"].sum()
mejor_vendedor = df_filtro.groupby("Vendedor")["Ventas"].sum().idxmax()
mejor_producto = df_filtro.groupby("Producto")["Ventas"].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Ventas totales", f"S/ {ventas_totales:,.0f}")
col2.metric("📦 Unidades vendidas", f"{unidades:,.0f}")
col3.metric("🏆 Mejor vendedor", mejor_vendedor)
col4.metric("⭐ Producto estrella", mejor_producto)

st.divider()

# ──────────────────────────────────────────────
# 7-8. KPI por producto + gráfico profesional
# ──────────────────────────────────────────────
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("🛒 Ventas por producto")
    ventas_producto = df_filtro.groupby("Producto")["Ventas"].sum().sort_values(ascending=False)
    st.dataframe(ventas_producto.rename("Ingresos").to_frame().style.format("{:,.0f}"))

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(
        x=ventas_producto.index,
        y=ventas_producto.values,
        palette="Blues_d",
        hue=ventas_producto.index,
        legend=False,
        ax=ax1,
    )
    ax1.set_title("Ventas por Producto")
    ax1.set_xlabel("Producto")
    ax1.set_ylabel("Ingresos")
    st.pyplot(fig1)

with col_der:
    st.subheader("🏆 Participación por vendedor")
    ventas_vendedor = df_filtro.groupby("Vendedor")["Ventas"].sum().sort_values(ascending=False)
    st.dataframe(ventas_vendedor.rename("Ventas").to_frame().style.format("{:,.0f}"))

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    ventas_vendedor.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax2,
    )
    ax2.set_title("Participación por vendedor")
    ax2.set_ylabel("")
    st.pyplot(fig2)

st.divider()

# ──────────────────────────────────────────────
# 6. Producto más vendido (cantidad)
# ──────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📦 Cantidad vendida por producto")
    producto_mas_vendido = df_filtro.groupby("Producto")["Cantidad"].sum()
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    producto_mas_vendido.plot(kind="bar", color="skyblue", ax=ax3)
    ax3.set_title("Cantidad vendida por producto")
    ax3.set_xlabel("Producto")
    ax3.set_ylabel("Cantidad")
    ax3.grid(True)
    st.pyplot(fig3)

with col_b:
    st.subheader("💰 Participación de ingresos")
    ingresos = df_filtro.groupby("Producto")["Ventas"].sum()
    fig4, ax4 = plt.subplots(figsize=(6, 5))
    ingresos.plot(kind="pie", autopct="%1.1f%%", ax=ax4)
    ax4.set_title("Participación de ingresos")
    ax4.set_ylabel("")
    st.pyplot(fig4)

st.divider()

# ──────────────────────────────────────────────
# 12-13. Análisis temporal y tendencia
# ──────────────────────────────────────────────
st.subheader("📅 Tendencia de ventas")
ventas_fecha = df_filtro.groupby("Fecha")["Ventas"].sum()

fig5, ax5 = plt.subplots(figsize=(10, 5))
ax5.plot(ventas_fecha.index, ventas_fecha.values, marker="o", color="tab:blue")
ax5.set_title("Tendencia de Ventas")
ax5.set_xlabel("Fecha")
ax5.set_ylabel("Ventas")
ax5.grid(True)
st.pyplot(fig5)

st.divider()

# ──────────────────────────────────────────────
# Tabla de datos completa
# ──────────────────────────────────────────────
st.subheader("📋 Datos completos")
st.dataframe(df_filtro, use_container_width=True)
