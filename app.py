import streamlit as st
import requests
import tempfile
from streamlit_audiorecorder import audiorecorder
from utils_gpt import interpretar_sueno
from utils_audio import reproducir_texto_en_audio

st.set_page_config(page_title="💤 Suenia", layout="centered")
st.markdown("<h1 style='text-align: center;'>💤 Suenia</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Interpreta tus sueños con IA</p>", unsafe_allow_html=True)
st.markdown("---")

# 1️⃣ GRABACIÓN DE VOZ (aparece primero)
st.subheader("🎙️ Graba tu sueño con tu voz")
audio_bytes = audiorecorder("🎤 Iniciar grabación", "⏹️ Detener grabación", key="recorder")
usar_audio = isinstance(audio_bytes, (bytes, bytearray)) and len(audio_bytes) > 0

# Si hay audio, reproducir y transcribir
if usar_audio:
    st.audio(audio_bytes, format="audio/wav")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        audio_path = tmp.name
    with st.spinner("🎧 Transcribiendo..."):
        resp = requests.post("https://grabador-backend.onrender.com/transcribir",
                             files={"audio": open(audio_path, "rb")})
        resp.raise_for_status()
        texto = resp.json().get("transcripcion", "").strip()
    st.success("✅ Transcripción lista")
else:
    texto = ""

# 2️⃣ CAJA DE TEXTO (después de grabar)
st.subheader("✍️ Escribe o revisa aquí tu sueño")
sueno = st.text_area("📝 Tu sueño:", value=texto, height=150)

# 3️⃣ BOTÓN DE INTERPRETAR
st.markdown("---")
if st.button("🔮 Interpretar el sueño"):
    if not sueno.strip():
        st.warning("Por favor, graba o escribe tu sueño antes de interpretar.")
    else:
        with st.spinner("🧠 Analizando..."):
            interpretacion = interpretar_sueno(sueno)
        st.markdown("### 🧠 Interpretación")
        st.write(interpretacion)
        if st.checkbox("🔊 Escuchar interpretación"):
            audio_file = reproducir_texto_en_audio(interpretacion)
            if audio_file:
                st.audio(audio_file)
