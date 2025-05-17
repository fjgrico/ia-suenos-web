import streamlit as st
import requests
import tempfile
from streamlit_audiorecorder import audiorecorder
from utils_gpt import interpretar_sueno
from utils_audio import reproducir_texto_en_audio

st.set_page_config(page_title="💤 Suenia | Interpretación de Sueños", layout="centered")

# Título de la app
st.markdown("<h1 style='text-align: center;'>💤 Suenia</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Interpreta tus sueños con Inteligencia Artificial</p>", unsafe_allow_html=True)
st.markdown("---")

# 1️⃣ Grabación de voz
st.subheader("🎙️ Graba tu sueño con tu voz")

# Usamos streamlit-audiorecorder para capturar bytes de audio
audio_bytes = audiorecorder("Iniciar grabación", "Detener grabación", key="recorder")

# Validar si hay audio grabado
usar_audio = isinstance(audio_bytes, (bytes, bytearray)) and len(audio_bytes) > 0

# 2️⃣ Transcripción y edición de texto
st.subheader("📝 Transcripción / Edita tu sueño aquí")
if usar_audio:
    try:
        # Guardar temporalmente como WAV
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            tmpfile.write(audio_bytes)
            audio_path = tmpfile.name

        # Enviar al backend para transcribir
        files = {"audio": open(audio_path, 'rb')}
        response = requests.post("https://grabador-backend.onrender.com/transcribir", files=files)
        response.raise_for_status()
        texto = response.json().get("transcripcion", "").strip()
    except Exception as e:
        st.error(f"❌ Error al transcribir audio: {e}")
        texto = ""
else:
    texto = ""

# Caja de texto editable con la transcripción o vacía
sueno = st.text_area("Escribe o corrige tu sueño:", value=texto, height=150)

# 3️⃣ Botón para interpretar
if st.button("🔮 Interpretar el sueño"):
    if not sueno.strip():
        st.warning("Por favor, graba o escribe tu sueño antes de interpretar.")
    else:
        with st.spinner("Interpretando..."):
            interpretacion = interpretar_sueno(sueno)
        # Mostrar interpretación
        st.markdown("### 🧠 Interpretación del Sueño:")
        st.write(interpretacion)
        # Opción de escuchar la interpretación
        if st.checkbox("🔊 Escuchar interpretación en voz"):
            audio_file = reproducir_texto_en_audio(interpretacion)
            if audio_file:
                st.audio(audio_file)
