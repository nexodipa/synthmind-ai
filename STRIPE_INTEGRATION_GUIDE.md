# 💳 Guía de Integración de Pagos con Stripe: SynthMind AI

Esta guía explica cómo vincular tu enlace de cobro de **Stripe** con SynthMind AI para comenzar a recibir pagos cuando tus usuarios agoten sus 3 análisis gratuitos.

---

## ⚡ Paso 1: Obtener tu Enlace de Cobro en Stripe (2 Minutos)

1. Ingresa a [Stripe.com](https://stripe.com) y crea una cuenta gratuita (o inicia sesión).
2. En el panel principal de Stripe, busca la barra de búsqueda o ve a la sección **Productos** -> **Enlaces de pago** (*Payment Links*).
3. Haz clic en **"Nuevo enlace de pago"** (*New Payment Link*).
4. Configura el producto:
   * **Nombre:** `SynthMind AI Pro`
   * **Tipo de precio:** Recurrente (Mensual)
   * **Monto:** `$19.00 USD` (o el precio que desees).
5. Haz clic en **Crear enlace**. Copia el enlace resultante (será algo como `https://buy.stripe.com/test_abcdef123456`).

---

## 🛠️ Paso 2: Vincular el Enlace a tu Aplicación

Hemos diseñado SynthMind AI para que la integración sea sumamente sencilla:

### Opción A: En Streamlit Community Cloud (Recomendado)
1. Entra a tu app en [share.streamlit.io](https://share.streamlit.io).
2. Haz clic en **Settings** -> **Secrets**.
3. Añade la variable `STRIPE_PAYMENT_LINK`:
   ```toml
   GEMINI_API_KEY = "tu_clave_de_gemini"
   STRIPE_PAYMENT_LINK = "https://buy.stripe.com/tu_enlace_real"
   ```
4. Guarda los cambios.

### Opción B: En el Código Fuente Local (`app.py` y `streamlit_app.py`)
Si deseas cambiar el enlace directamente en el código:
* Abre `app.py` y busca el texto `https://stripe.com`. Reemplázalo por tu enlace de Stripe.
* Abre `streamlit_app.py` y busca el texto `https://stripe.com`. Reemplázalo por tu enlace de Stripe.

---

## 🔒 ¿Cómo funciona el flujo de cobro?
1. El usuario realiza 3 análisis gratuitos en tu web.
2. Al intentar realizar el 4to análisis, el sistema bloquea el botón y muestra la ventana emergente de suscripción.
3. Al hacer clic en **"Activar Licencia Comercial"**, el usuario es redirigido a tu página de pago segura de Stripe.
4. Una vez realizado el pago, Stripe procesa el dinero y te lo deposita directamente a tu cuenta bancaria.
