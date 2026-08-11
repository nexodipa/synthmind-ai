# 🚀 Guía de Despliegue Paso a Paso: SynthMind AI

Esta guía contiene los pasos exactos y los comandos para que puedas subir tu proyecto a GitHub y desplegarlo de forma 100% gratuita tanto en **Streamlit Community Cloud** (para el dashboard interactivo) como en **Render.com** (para la API de FastAPI).

---

## 📂 Requisito Previo: Subir tu Código a GitHub

Para que las plataformas de hosting gratuitas puedan leer tu código, primero debes tenerlo guardado en un repositorio de GitHub.

### Comandos de Git para Copiar y Pegar:
Abre una terminal o consola de comandos (como PowerShell) **dentro de la carpeta de este proyecto (`synthmind-ai`)** y ejecuta los siguientes comandos en orden:

```bash
# 1. Inicializar Git en esta carpeta
git init

# 2. Registrar todos los archivos del proyecto (excluyendo secretos gracias al archivo .gitignore)
git add .

# 3. Guardar tu primer commit local
git commit -m "feat: primer despliegue de SynthMind AI"

# 4. Establecer la rama principal a "main"
git branch -M main

# 5. Conectar esta carpeta con tu repositorio de GitHub
# (¡REEMPLAZA la URL de abajo con la de tu propio repositorio vacío creado en GitHub!)
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git

# 6. Subir el código a la nube
git push -u origin main
```

---

## 🎨 Opción 1: Despliegue en Streamlit Community Cloud (El más fácil y rápido)
Esta plataforma hospeda tu frontend interactivo de Streamlit de forma gratuita con un enlace público HTTPS.

### Pasos exactos en el Panel de Streamlit Cloud:
1.  Entra en [share.streamlit.io](https://share.streamlit.io) e inicia sesión con tu cuenta de GitHub.
2.  Haz clic en el botón **"Create app"** (o **"New app"**).
3.  Selecciona la opción **"I already have an app"** (Ya tengo una aplicación).
4.  Rellena los campos con los siguientes valores exactos:
    *   **Repository**: `TU_USUARIO/TU_REPOSITORIO` (selecciónalo de la lista)
    *   **Branch**: `main`
    *   **Main file path**: `streamlit_app.py` *(¡Asegúrate de escribir streamlit_app.py!)*
    *   **App URL**: Puedes escribir un nombre personalizado para tu enlace (ej. `analisis-synthmind`).
5.  **Configurar la Gemini API Key de forma segura**:
    *   Antes de hacer clic en Deploy, haz clic en **"Advanced settings..."** (Ajustes avanzados).
    *   En el cuadro de texto de **Secrets**, copia y pega el siguiente bloque exacto, reemplazando la clave con la tuya:
        ```toml
        GEMINI_API_KEY = "Escribe_aqui_tu_clave_de_Google_AI_Studio"
        ```
    *   Haz clic en **Save** (Guardar).
6.  Haz clic en **"Deploy!"** y ¡listo! En 1 o 2 minutos tu aplicación estará en línea.

---

## ⚙️ Opción 2: Despliegue en Render.com (Para el Servidor FastAPI)
Si prefieres utilizar el backend de FastAPI con la SPA (interfaz Tailwind) integrada, puedes alojarlo en Render.

### Parámetros exactos para el Panel de Render:
1.  Crea una cuenta gratuita en [Render.com](https://render.com) e inicia sesión con tu cuenta de GitHub.
2.  En el Dashboard de Render, haz clic en **"New +"** y selecciona **"Web Service"** (Servicio Web).
3.  Selecciona tu repositorio de GitHub de la lista y haz clic en **Connect**.
4.  Configura los siguientes valores exactos en el formulario:
    *   **Name**: `synthmind-backend`
    *   **Language**: `Python 3`
    *   **Branch**: `main`
    *   **Region**: Selecciona la más cercana (ej. Oregon o Frankfurt).
    *   **Build Command**:
        ```bash
        pip install --upgrade pip && pip install -r requirements.txt
        ```
    *   **Start Command**:
        ```bash
        uvicorn app:app --host 0.0.0.0 --port $PORT
        ```
5.  **Configurar Variables de Entorno**:
    *   Baja en la misma página hasta la sección **"Environment Variables"** (o ve a la pestaña **Environment**).
    *   Haz clic en **"Add Environment Variable"** y añade estas dos variables clave:
        1.  **Key**: `GEMINI_API_KEY` | **Value**: `Tu_clave_de_Gemini_AI_Studio_aqui`
        2.  **Key**: `PYTHON_VERSION` | **Value**: `3.11.8`
6.  Haz clic en **"Create Web Service"** al final de la página.
7.  *Nota*: La versión gratuita de Render entra en "modo de suspensión" después de 15 minutos de inactividad. La primera petición que hagas después de un tiempo puede tardar de 30 a 50 segundos en responder mientras el servidor se enciende.

---

## 🔄 ¿Cómo actualizar tu app una vez desplegada?
Si haces cambios en el código localmente y quieres que se actualicen en la nube automáticamente, solo debes abrir la consola en tu carpeta de proyecto y ejecutar:

```bash
git add .
git commit -m "update: descripción de tus cambios"
git push origin main
```
Tanto Streamlit Cloud como Render detectarán la actualización en GitHub y volverán a compilar tu aplicación de forma automática en pocos segundos.
