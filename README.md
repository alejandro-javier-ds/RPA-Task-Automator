# RPA Task Automator (Web Scraping & Telemetry) 🤖

Bot de automatización industrial desarrollado en Python utilizando Selenium para la extracción masiva de datos, con persistencia de telemetría en SQL Server y monitoreo en tiempo real a través de Streamlit.

## 🛠️ Stack Tecnológico
- **Engine:** Selenium WebDriver (Modo Headless)
- **Driver Management:** WebDriver Manager (Auto-update)
- **Database:** SQL Server (Transact-SQL)
- **Frontend:** Streamlit con barras de progreso dinámicas.
- **Analytics:** Pandas para serialización de datos.

## 🚀 Funcionalidades Clave
- **Automatización Multi-página:** Navegación autónoma por estructuras paginadas.
- **Registro de Telemetría:** Auditoría automática de tiempos de ejecución y volumen de datos en base de datos.
- **Visualización Interactiva:** Dashboard con soporte para modo pantalla completa y scroll de alta densidad.

## 🛡️ Manejo de Errores
El sistema incluye validación de directorios y manejo de excepciones de WebDriver, asegurando que la telemetría se registre incluso si el proceso de extracción falla.