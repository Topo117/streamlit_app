import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Cobertura de Agua Potable - Cusco", initial_sidebar_state="expanded")

st.sidebar.image("logo.png", width=60)
st.sidebar.title("Ingeniería Ambiental - 2024")
st.sidebar.write("Integrantes:")
st.sidebar.write("* Karla Mayve Ordinola Zapata")
st.sidebar.write("* Héctor Raúl Huarcaya Chipana")
st.sidebar.write("* Oscar Manuel Herrera Tumba")

menu_options = [
    "Default - Información inicial",
    "Provincias con mayor población sin cobertura de agua",
    "Distribución del porcentaje de cobertura en todos los distritos",
    "Relación entre población total y porcentaje de cobertura en distritos",
    "Acerca de los distritos"
]

menu_selection = st.sidebar.selectbox("Seleccione una opción", menu_options)

file_path = "Indicadores_de_Cobertura_en_el_Servicio_de_Agua_Potable_en_el_Departamento_de_Cusco_2016_2019.csv"
try:
    data = pd.read_csv(file_path, sep=';', encoding='utf-8')
except UnicodeDecodeError:
    data = pd.read_csv(file_path, sep=';', encoding='latin1')

data['FECHA_CORTE'] = pd.to_datetime(data['FECHA_CORTE'], format='%Y%m%d', errors='coerce')
data['PORCENTAJE_CON_COBERTURA'] = (data['POBLACION_CON_COBERTURA'] / data['TOTAL_POBLACION']) * 100
data['PORCENTAJE_SIN_COBERTURA'] = (data['POBLACION_SIN_COBERTURA'] / data['TOTAL_POBLACION']) * 100

if menu_selection == "Información inicial":
    st.title("Cobertura de agua potable del departamento de Cusco del Perú")
    st.image("placeholder.png", use_container_width=True)
    st.write("""
        La base de datos de la cobertura en los servicios de agua potable en el departamento de Cusco corresponde a la información de los indicadores de cobertura del departamento mencionado. Dicha información, recopila la información de cobertura de agua potable de los distritos del departamento que se encuentra en el país del Perú.
        La información fue proporcionada por la plataforma nacional de datos libres del gobierno del Perú.

        **¿Qué buscamos?**  
        Con la página se desea brindar la información del dataset de una forma más gráfica y directa para una comprensión más eficiente.

        **¿Por qué es importante el agua potable?**  
        El agua potable, es de importancia fundamental para impedir y reducir la propagación de enfermedades relacionadas con la falta de saneamiento y la salud.

        **¿Cómo influye la toma de datos de la cobertura de agua potable en la población?**  
        Al saber los datos que se tienen acerca la cobertura del agua potable en una población o región se puede dar a conocer sus niveles de saneamiento, salud de las personas que viven en el lugar y el qué tanto están comprometido a excitar enfermedades por el defecto de cobertura. Le permite a las entidades poder tomar acción con respecto a la falta de cobertura o el poder informar a la población acerca de los niveles de salubridad que tiene el agua con la que preparan sus alimentos, la que se usa para cosechar sus alimentos y la que beben en el día a día.
    """)
    github_url = "https://github.com/Topo117/streamlit_app"
    st.markdown(f"""
        <a href="{github_url}" target="_blank" style="text-decoration: none;">
            <button style="display: flex; align-items: center; background-color: #24292e; color: white; padding: 10px 20px; margin-bottom: 10px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">
                <svg xmlns="http://www.w3.org/2000/svg" fill="white" viewBox="0 0 24 24" width="20px" height="20px" style="margin-right: 10px;">
                    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.207 11.387.6.113.793-.262.793-.583v-2.18c-3.338.727-4.042-1.416-4.042-1.416-.546-1.387-1.334-1.755-1.334-1.755-1.09-.746.084-.73.084-.73 1.204.084 1.838 1.24 1.838 1.24 1.07 1.833 2.806 1.304 3.492.996.108-.775.418-1.305.762-1.605-2.665-.304-5.467-1.33-5.467-5.93 0-1.31.467-2.383 1.24-3.223-.124-.303-.537-1.524.118-3.176 0 0 1.01-.324 3.31 1.23.957-.267 1.983-.4 3.003-.404 1.02.004 2.047.137 3.006.404 2.297-1.554 3.306-1.23 3.306-1.23.657 1.653.244 2.874.12 3.176.77.84 1.24 1.913 1.24 3.223 0 4.61-2.807 5.623-5.48 5.92.43.372.814 1.103.814 2.222v3.293c0 .322.192.698.8.583C20.565 21.796 24 17.3 24 12 24 5.37 18.63 0 12 0z"/>
                </svg>
                Ir a código del Proyecto
            </button>
        </a>
    """, unsafe_allow_html=True)

elif menu_selection == "Provincias con mayor población sin cobertura de agua":
    st.title("Provincias con mayor población sin cobertura de agua")
    provincia_sin_cobertura = data.groupby('PROVINCIA')['POBLACION_SIN_COBERTURA'].sum().reset_index()
    top5_provincias = provincia_sin_cobertura.sort_values(by='POBLACION_SIN_COBERTURA', ascending=False).head(5)

    fig, ax = plt.subplots()
    ax.bar(top5_provincias['PROVINCIA'], top5_provincias['POBLACION_SIN_COBERTURA'], color='orange')
    plt.xticks(rotation=45)
    plt.ylabel('Población sin Cobertura')
    plt.title('Top 5 Provincias con Mayor Población sin Cobertura')
    st.pyplot(fig)

    st.write("El gráfico de barras presenta las provincias con mayor cantidad de población sin cobertura de agua.")

elif menu_selection == "Distribución del porcentaje de cobertura en todos los distritos":
    st.title("Distribución del porcentaje de cobertura en todos los distritos")
    fig, ax = plt.subplots()
    ax.hist(data['PORCENTAJE_CON_COBERTURA'], bins=20, color='green', edgecolor='black')
    plt.xlabel('Porcentaje de Cobertura')
    plt.ylabel('Número de Distritos')
    plt.title('Distribución de Cobertura en Distritos')
    st.pyplot(fig)

    st.write("El histograma indica cómo se distribuye el porcentaje de cobertura entre todos los distritos. Se puede visualizar que un gran número de distritos se encuentra con un alto porcentaje de cobertura, mientras que pocos tienen un muy bajo porcentaje de cobertura.")

elif menu_selection == "Relación entre población total y porcentaje de cobertura en distritos":
    st.title("Relación entre población total y porcentaje de cobertura en distritos")
    fig, ax = plt.subplots()
    ax.scatter(data['TOTAL_POBLACION'], data['PORCENTAJE_CON_COBERTURA'], alpha=0.5)
    plt.xlabel('Población Total')
    plt.ylabel('Porcentaje de Cobertura')
    plt.title('Población vs Cobertura')
    st.pyplot(fig)

    st.write("El scatter plot permite visualizar la relación entre la población total de los distritos y su porcentaje de cobertura.")

elif menu_selection == "Acerca de los distritos":
    distritos_con_problemas = data[data['POBLACION_SIN_COBERTURA'] > 0]

    st.title("Análisis por Distrito")
    distrito_seleccionado = st.selectbox(
        "Selecciona un distrito para analizar",
        distritos_con_problemas['DISTRITO'].unique()
    )

    st.subheader("Resumen del Dataset")
    st.write(f"Total de departamentos: {data['DEPARTAMENTO'].nunique()}")
    st.write(f"Total de provincias: {data['PROVINCIA'].nunique()}")
    st.write(f"Total de distritos: {data['DISTRITO'].nunique()}")
    st.write(f"Distritos con población sin cobertura: {data[data['POBLACION_SIN_COBERTURA'] > 0]['DISTRITO'].nunique()}")

    distrito_data = distritos_con_problemas[distritos_con_problemas['DISTRITO'] == distrito_seleccionado]

    # Gráfico 1
    st.subheader(f"Distribución de Cobertura de Agua en {distrito_seleccionado}")
    total_con_cobertura = distrito_data['POBLACION_CON_COBERTURA'].sum()
    total_sin_cobertura = distrito_data['POBLACION_SIN_COBERTURA'].sum()

    fig1, ax1 = plt.subplots()
    labels = ['Con Acceso a Agua', 'Sin Acceso a Agua']
    sizes = [total_con_cobertura, total_sin_cobertura]
    colors = ['blue', 'red']
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    st.write("El gráfico de torta muestra la distribución de población con y sin acceso a agua en el distrito seleccionado.")

    # Gráfico 3
    st.subheader(f"Evolución de Cobertura en {distrito_seleccionado}")
    distrito_data_sorted = distrito_data.sort_values('ANIO')

    fig3, ax3 = plt.subplots()
    ax3.plot(
        distrito_data_sorted['ANIO'],
        distrito_data_sorted['PORCENTAJE_CON_COBERTURA'],
        marker='o', linestyle='-', color='blue'
    )

    ax3.set_xticks(distrito_data_sorted['ANIO'])
    ax3.set_xlabel('Año')
    ax3.set_ylabel('Porcentaje de Cobertura')
    plt.title(f"Evolución de Cobertura en {distrito_seleccionado}")
    st.pyplot(fig3)

    st.write("El gráfico de línea muestra cómo ha cambiado la cobertura en el distrito seleccionado a lo largo del tiempo.")

    # Tabla
    distrito_data_all = data[data['DISTRITO'] == distrito_seleccionado]
    st.subheader("Datos del Distrito Seleccionado")
    st.dataframe(distrito_data_all)
