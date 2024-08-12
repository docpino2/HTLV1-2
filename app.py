import streamlit as st
import pandas as pd
from io import BytesIO

# Define la función de clasificación y recomendación
def clasificar_y_recomendar(row):
    recomendaciones = []
    grupos_riesgo = []

    # Grupo Riesgo 1 - Notificación Roja
    if row['resultado'] == 'REACTIVO':
        grupos_riesgo.append('Notificación Roja')
        recomendaciones.append("Requiere seguimiento por Hematología y Medicina Interna. Recomendable realizar tamizaje activo para HTLV en familiares de primer grado de consanguinidad.")

    # Grupo Riesgo 2 - Notificación Amarilla
    if (row['resultado'] in ['REACTIVO', 'positivo']) and \
       (row.get('Lactancia Materna', 'No') == 'Si') and \
       (row.get('En embarazo actual', 'No') == 'Si') and \
       (row.get('Desea tener Hijos', 'No') == 'si'):
        grupos_riesgo.append('Notificación Amarilla')
        recomendaciones.append("Se sugiere asesoría epidemiológica, pediátrica y obstétrica según aplique.")

    # Grupo Riesgo 3 - Notificación Verde
    if row.get('Hijo de madre con tamizaje HTLV', 'No') in ['positivo', 'reactivo']:
        grupos_riesgo.append('Notificación Verde')
        recomendaciones.append("Requiere seguimiento por Hematología y Medicina Interna.")

    return pd.Series({
        'Grupos de Riesgo': ', '.join(grupos_riesgo) if grupos_riesgo else 'Sin Riesgo',
        'Recomendaciones': ' '.join(recomendaciones) if recomendaciones else 'No se requiere acción'
    })

# Aplicación Streamlit
def main():
    st.title('Clasificación y Recomendación HTLV')

    uploaded_file = st.file_uploader("Sube tu archivo Excel", type="xlsx")
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write("Datos cargados:", df.head())

        # Aplicar la función de clasificación y recomendación
        resultados = df.apply(clasificar_y_recomendar, axis=1)
        df = pd.concat([df, resultados], axis=1)

        st.write("Datos con clasificación y recomendaciones:", df)

        # Guardar el DataFrame a un archivo Excel en memoria
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        buffer.seek(0)

        # Descargar el archivo con los resultados
        st.download_button(
            label="Descargar archivo con resultados",
            data=buffer,
            file_name="Base_madreHTLV_resultados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
