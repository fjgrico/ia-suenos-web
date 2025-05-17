import streamlit as st
import base64
import requests
import tempfile
from audio_recorder_component import audio_recorder
from utils_gpt import interpretar_sueno
from utils_audio import reproducir_texto_en_audio

st.set_page_config(page_title="💤 Suenia | Interpretación de Sueños", layout="centered")

st.markdown("<h1 style='text-align: center;'>💤 Suenia</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Interpreta tus sueños con IA</p>", unsafe_allow_html=True)
st.markdown("---")

# 1️⃣ GRABACIÓN DE VOZ
st.subheader("🎙️ Graba tu sueño con tu voz")
audio_base64 = audio_recorder()

# Solo mostrar el botón de detener si el componente devuelve base64
usar_audio = isinstance(audio_base64, str) and len(audio_base64) > 0

# 2️⃣ TRANSCRIPCIÓN Y EDITAR TEXTO
st.subheader("✍️ Escribe o revisa aquí tu sueño")
if usar_audio:
    # Convertir base64 a texto transcrito
    try:
        audio_bytes = base64.b64decode(audio_base64)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
            f.write(audio_bytes)
            ruta = f.name

        files = {"audio": open(ruta, "rb")}
        resp = requests.post("https://grabador-backend.onrender.com/transcribir", files=files)
        resp.raise_for_status()
        texto = resp.json().get("transcripcion", "")
    except Exception as e:
        st.error(f"❌ No se pudo transcribir: {e}")
        texto = ""
else:
    texto = ""

# Caja de texto editable con la transcripción (o vacía si no hay)
sueno = st.text_area("📝 Tu sueño:", value=texto, height=150)

# 3️⃣ BOTÓN PARA INTERPRETAR
if st.button("🔮 Interpretar el sueño"):
    if not sueno.strip():
        st.warning("Escribe o graba tu sueño antes de interpretar.")
    else:
        with st.spinner("Analizando..."):
            interpretacion = interpretar_sueno(sueno)
        st.markdown("### 🧠 Interpretación")
        st.write(interpretacion)

        if st.checkbox("🔊 Escuchar interpretación"):
            audio_file = reproducir_texto_en_audio(interpretacion)
            if audio_file:
                st.audio(audio_file)
