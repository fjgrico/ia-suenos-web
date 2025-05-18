import streamlit as st
import base64
import requests
import tempfile
from audio_recorder_component import audio_recorder
from utils_gpt import interpretar_sueno
from utils_audio import reproducir_texto_en_audio

# Configuración de la página
st.set_page_config(page_title="💤 Suenia", layout="centered")
st.markdown("<h1 style='text-align: center;'>💤 Suenia</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Interpretación de sueños con IA</p>", unsafe_allow_html=True)
st.markdown("---")

# 1️⃣ Grabación de voz (aparece primero)
st.subheader("🎙️ Graba tu sueño con tu voz")
audio_base64 = audio_recorder()

# Procesar la grabación
texto_transcrito = ""
if isinstance(audio_base64, str) and len(audio_base64) > 10:
    try:
        audio_bytes = base64.b64decode(audio_base64)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(audio_bytes)
            audio_path = tmp.name
        resp = requests.post(
            "https://grabador-backend.onrender.com/transcribir",
            files={"audio": open(audio_path, "rb")}
        )
        resp.raise_for_status()
        texto_transcrito = resp.json().get("transcripcion", "").strip()
        st.success("✅ Transcripción lista")
    except Exception as e:
        st.error(f"❌ Error al transcribir: {e}")

# 2️⃣ Caja de texto editable (después de grabar)
st.subheader("✍️ Escribe o corrige tu sueño")
sueno = st.text_area("📝 Tu sueño:", value=texto_transcrito, height=150)

# 3️⃣ Botón de Interpretar
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

# Pie de página
st.markdown("---")
st.markdown(
    "<small>🔗 Suenia – Interpretador de sueños con IA | Mentor Digital Pro</small>",
    unsafe_allow_html=True
)
