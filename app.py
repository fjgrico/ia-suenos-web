import streamlit as st
import os
import requests
import tempfile
from streamlit_audiorecorder import audiorecorder
from utils_gpt import interpretar_sueno
from utils_audio import reproducir_texto_en_audio

# --- Configuración de página ---
st.set_page_config(page_title="💤 Suenia", layout="centered")
st.markdown("<h1 style='text-align: center;'>💤 Suenia</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Interpreta tus sueños con IA</p>", unsafe_allow_html=True)
st.markdown("---")

# --- 1️⃣ Grabación de voz (aparece primero) ---
st.subheader("🎙️ Graba tu sueño con tu voz")
audio_bytes = audiorecorder("🎤 Iniciar grabación", "⏹️ Detener grabación", key="recorder")

texto_transcrito = ""
if isinstance(audio_bytes, (bytes, bytearray)) and len(audio_bytes) > 0:
    # Mostrar reproductor del audio que acabas de grabar
    st.audio(audio_bytes, format="audio/wav")
    # Guardar a fichero temporal para enviar al backend
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        ruta_audio = tmp.name
    # Enviar al backend
    with st.spinner("🎧 Transcribiendo tu audio..."):
        resp = requests.post(
            "https://grabador-backend.onrender.com/transcribir",
            files={"audio": open(ruta_audio, "rb")}
        )
        if resp.status_code == 200:
            texto_transcrito = resp.json().get("transcripcion", "").strip()
            st.success("✅ Transcripción lista")
        else:
            st.error(f"❌ Error {resp.status_code} al transcribir")

# --- 2️⃣ Caja de texto editable (después de grabar) ---
st.subheader("✍️ Escribe o revisa aquí tu sueño")
sueno = st.text_area("📝 Tu sueño:", value=texto_transcrito, height=150, key="input_sueno")

# --- 3️⃣ Botón de interpretación ---
st.markdown("---")
if st.button("🔮 Interpretar el sueño"):
    if not sueno.strip():
        st.warning("Por favor, graba o escribe tu sueño antes de interpretar.")
    else:
        with st.spinner("🧠 Analizando con IA..."):
            interpretacion = interpretar_sueno(sueno)
        st.markdown("### 🧠 Interpretación del Sueño")
        st.write(interpretacion)
        if st.checkbox("🔊 Escuchar interpretación"):
            audio_file = reproducir_texto_en_audio(interpretacion)
            if audio_file:
                st.audio(audio_file)

# --- Footer ---
st.markdown("---")
st.markdown(
    "<small>🔗 Suenia – Interpretador de sueños con IA | Mentor Digital Pro</small>",
    unsafe_allow_html=True
)
