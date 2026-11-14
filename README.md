# 📈 Dashboard Comercial de Ventas

Dashboard interactivo de análisis de ventas de una tienda, construido con **Streamlit**, **pandas** y **seaborn**.

## 🎛️ Funcionalidades

- KPIs: ventas totales, unidades vendidas, mejor vendedor y producto estrella
- Filtros por producto, vendedor y rango de fechas
- Gráficos: barras (seaborn), circulares y tendencia temporal
- Exportación del reporte filtrado a Excel
- Basado en el notebook `Analisis_Ventas_y_Dashboard_Comercial.ipynb`

## 🚀 Ejecución local

```bash
pip install -r requirements.txt
streamlit run dashboard_ventas.py
```

## ☁️ Despliegue en Streamlit Cloud

1. Sube este repositorio a GitHub
2. Entra a [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Selecciona el repositorio, la rama `main` y el archivo `dashboard_ventas.py`
4. ¡Listo! Streamlit instalará automáticamente las dependencias desde `requirements.txt`

## 📁 Estructura

```
├── dashboard_ventas.py                        # Aplicación Streamlit
├── Analisis_Ventas_y_Dashboard_Comercial.ipynb # Notebook de análisis (Colab)
└── requirements.txt                           # Dependencias
```
