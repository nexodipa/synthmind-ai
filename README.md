# SynthMind AI — Análisis y síntesis de documentos con Gemini

SynthMind AI es un prototipo de aplicación para análisis crítico, extracción estructurada de conceptos y síntesis de documentos densos (PDF, TXT, MD) mediante los modelos Gemini 2.5 (Flash y Pro) de Google. Es un proyecto de portafolio: no tiene demo alojada públicamente y sus resultados son generados por un modelo de lenguaje, por lo que deben revisarse antes de usarse en decisiones legales, financieras o académicas.

Incluye dos interfaces:
1.  **SPA Interactiva (FastAPI + Tailwind CSS)**: Interfaz de una sola página con modo oscuro, tarjetas de conceptos dinámicas, barra de certeza e indicadores paso a paso.
2.  **Dashboard Streamlit**: Una versión alternativa pensada para desplegarse en Streamlit Community Cloud.

---

## 🚀 Requisitos e Instalación Local

### 1. Requisitos Previos
*   **Python 3.10 o superior** instalado.
*   Una **API Key de Gemini** de Google (Consíguela gratis en [Google AI Studio](https://aistudio.google.com/)).

### 2. Instalación de Dependencias
Abre la terminal en esta carpeta y ejecuta:
```bash
pip install -r requirements.txt
```

---

## 💻 Ejecución en Local (Windows)

Hemos creado scripts de ejecución rápida para que no tengas que escribir comandos en la consola:

*   **Para usar la interfaz web moderna (FastAPI)**:
    Haz doble clic en el archivo `start_fastapi.bat`. Se abrirá automáticamente tu navegador en [http://localhost:8000](http://localhost:8000).
*   **Para usar la interfaz de Streamlit**:
    Haz doble clic en el archivo `start_streamlit.bat`.

*(En macOS o Linux, puedes usar los archivos equivalentes `.sh` ejecutando `bash start_fastapi.sh` o `bash start_streamlit.sh` en la terminal).*

---

## ☁️ Guía de Despliegue en la Nube

Los planes gratuitos de Streamlit y Render permiten desplegarlo sin costo de servidor, con límites de uso. El uso de la API de Gemini depende de la cuota de tu propia clave (el nivel gratuito tiene límites y condiciones que pueden cambiar).

### Opción A: Streamlit Community Cloud (Recomendado — 2 Minutos)
1.  Sube esta carpeta a un repositorio público o privado en tu cuenta de **GitHub**.
2.  Inicia sesión en [Streamlit Share](https://share.streamlit.io/).
3.  Haz clic en **"New app"** y vincula tu repositorio de GitHub.
4.  Define el archivo principal (`Main file path`) como `streamlit_app.py`.
5.  Despliega. Tu aplicación estará disponible con un dominio público HTTPS y certificado de seguridad.
6.  *Opcional*: Si no deseas ingresar la API Key manualmente cada vez, ve a **Advanced Settings -> Secrets** en el panel de tu app en Streamlit y añade tu clave:
    ```toml
    GEMINI_API_KEY = "tu_api_key_aqui"
    ```

### Opción B: Render.com (Para el Servidor FastAPI)
1.  Sube la carpeta a un repositorio de **GitHub**.
2.  Crea un nuevo servicio web ("Web Service") en **Render.com**.
3.  Vincula tu repositorio.
4.  Establece el comando de inicio (`Start Command`) como:
    ```bash
    uvicorn app:app --host 0.0.0.0 --port $PORT
    ```
5.  En la pestaña de variables de entorno, añade `GEMINI_API_KEY` con tu clave de Google.

---

## 🧪 Pruebas Unitarias

Para verificar que todos los extractores de PDF y el motor estructurado de Gemini funcionen adecuadamente en tu sistema, puedes ejecutar el set de pruebas con:
```bash
pytest test_app.py
```
