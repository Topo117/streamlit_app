import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Dashboard: Cobertura de Agua por Distrito")
file_path = "Indicadores_de_Cobertura_en_el_Servicio_de_Agua_Potable_en_el_Departamento_de_Cusco_2016_2019.csv"

try:
    data = pd.read_csv(file_path, sep=';', encoding='utf-8')
except UnicodeDecodeError:
    data = pd.read_csv(file_path, sep=';', encoding='latin1')

data['FECHA_CORTE'] = pd.to_datetime(data['FECHA_CORTE'], format='%Y%m%d', errors='coerce')
st.subheader("Procesamiento de datos")
data['PORCENTAJE_CON_COBERTURA'] = (data['POBLACION_CON_COBERTURA'] / data['TOTAL_POBLACION']) * 100
data['PORCENTAJE_SIN_COBERTURA'] = (data['POBLACION_SIN_COBERTURA'] / data['TOTAL_POBLACION']) * 100

# Filtrar distritos con población sin cobertura
distritos_con_problemas = data[data['POBLACION_SIN_COBERTURA'] > 0]

# Mostrar resumen
st.subheader("Resumen del Dataset")
st.write(f"Total de departamentos: {data['DEPARTAMENTO'].nunique()}")
st.write(f"Total de provincias: {data['PROVINCIA'].nunique()}")
st.write(f"Total de distritos: {data['DISTRITO'].nunique()}")
st.write(f"Distritos con población sin cobertura: {distritos_con_problemas['DISTRITO'].nunique()}")

st.subheader("Análisis por Distrito")
distrito_seleccionado = st.selectbox(
    "Selecciona un distrito para analizar",
    distritos_con_problemas['DISTRITO'].unique()
)

distrito_data = distritos_con_problemas[distritos_con_problemas['DISTRITO'] == distrito_seleccionado]

total_con_cobertura = distrito_data['POBLACION_CON_COBERTURA'].sum()
total_sin_cobertura = distrito_data['POBLACION_SIN_COBERTURA'].sum()

# Gráfico comparativo
st.subheader(f"Distribución de Cobertura de Agua en {distrito_seleccionado}")
fig, ax = plt.subplots()
labels = ['Con Acceso a Agua', 'Sin Acceso a Agua']
sizes = [total_con_cobertura, total_sin_cobertura]
colors = ['blue', 'red']
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Asegura que el gráfico sea un círculo
plt.title(f"Población sin agua vs población con agua en {distrito_seleccionado}")
st.pyplot(fig)

# Tabla de datos del distrito seleccionado
st.subheader("Datos del Distrito Seleccionado")
st.dataframe(distrito_data)

# Conclusiones
st.subheader("Conclusiones")
st.write("""
- Este gráfico compara la población con y sin acceso a agua en el distrito seleccionado.
- Solo se muestran distritos donde al menos una parte de la población no tiene acceso a agua.
- Puedes seleccionar diferentes distritos para ver sus detalles.
""")
