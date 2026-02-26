import streamlit as st
import pandas as pd
import time
import pyodbc
from engine.bot_core import execute_rpa_pipeline

DB_CONFIG = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=(localdb)\\MSSQLLocalDB;"
    "Database=RPADatabase;"
    "Trusted_Connection=yes;"
)

st.set_page_config(page_title="RPA Control Center", layout="wide")

def get_automation_history():
    try:
        conn = pyodbc.connect(DB_CONFIG)
        query = "SELECT TOP 10 * FROM AutomationLogs ORDER BY ExecutionDate DESC"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

def main():
    st.title("🤖 RPA Task Automator")
    st.markdown("---")

    col1, col2 = st.columns([0.3, 0.7])

    with col1:
        st.subheader("Configuración del Bot")
        target = st.text_input("URL Objetivo", "https://quotes.toscrape.com")
        pages = st.slider("Páginas a procesar", 1, 10, 5)
        
        if st.button("🚀 Lanzar Automatización"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulación de estados para la barra visual
            for i in range(pages):
                step = i + 1
                percent = int((step / pages) * 100)
                status_text.text(f"Procesando página {step} de {pages}...")
                
                # Ejecutamos la lógica del bot (podríamos modularizar más para reportar por página)
                if i == 0: 
                    execute_rpa_pipeline(target, max_pages=pages)
                
                progress_bar.progress(percent)
                time.sleep(0.5)
            
            st.success("BOT_FINISHED: Extracción y Sincronización SQL completada.")
            st.balloons()

    with col2:
        st.subheader("Historial de Ejecución (SQL Server)")
        history = get_automation_history()
        if not history.empty:
            # Usamos dataframe con altura fija para forzar el scroll
            st.dataframe(history, use_container_width=True, height=250)
        else:
            st.info("No se encontraron registros de telemetría.")

        st.subheader("📦 Datos Extraídos del Objetivo")
        try:
            # Quitamos el .head(10) para cargar todo el CSV
            current_data = pd.read_csv("data/extracted_items.csv")
            
            # st.dataframe permite scroll y tiene el boton de "Agrandar" (flechas) arriba a la derecha
            st.dataframe(
                current_data, 
                use_container_width=True, 
                height=500 # Altura inicial, pero se puede expandir
            )
            st.caption(f"Visualizando {len(current_data)} registros extraídos.")
        except:
            st.warning("Esperando ejecución para mostrar datos...")

if __name__ == "__main__":
    main()