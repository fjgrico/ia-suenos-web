import streamlit as st
import base64
import requests
import tempfile
from audio_recorder_component import audio_recorder
from utils_gpt import interpretar_sueno
from utils_audio import reproducir_texto_en_audio

# Configuración de la página
st.set_page_config(page_title="💤 Suenia", layout="centered")

# Encabezado
st.title("💤 Suenia")
st.subheader("Interpretación de sueños con Inteligencia Artificial")
st.markdown("---")

# 1️⃣ Grabación de voz (se ve primero)
st.markdown("## 🎙️ Graba tu sueño con tu voz")
audio_base64 = audio_recorder()

# 2️⃣ Transcripción automática tras grabar
if audio_base64:
    try:
        audio_bytes = base64.b64decode(audio_base64)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        response = requests.post(
            "https://grabador-backend.onrender.com/transcribir",
            files={"audio": open(tmp_path, "rb")}
        )
        response.raise_for_status()
        st.session_state.transcripcion = response.json().get("transcripcion", "")
        st.success("✅ Transcripción lista")
    except Exception as e:
        st.error(f"❌ Error al transcribir: {e}")
        st.session_state.transcripcion = ""
else:
    if "transcripcion" not in st.session_state:
        st.session_state.transcripcion = ""

# 3️⃣ Caja de texto editable (después de grabar)
st.markdown("## ✍️ Escribe o corrige tu sueño")
sueno = st.text_area(
    "Tu sueño:", 
    value=st.session_state.transcripcion, 
    height=150, 
    key="input_sueno"
)

# 4️⃣ Botón de interpretar
st.markdown("---")
if st.button("🔮 Interpretar el sueño"):
    if not sueno.strip():
        st.warning("Por favor, graba o escribe tu sueño antes de interpretar.")
    else:
        with st.spinner("🧠 Interpretando tu sueño..."):
            resultado = interpretar_sueno(sueno)
        st.markdown("### 🧠 Interpretación")
        st.write(resultado)
        if st.checkbox("🔊 Escuchar interpretación"):
            audio_file = reproducir_texto_en_audio(resultado)
            if audio_file:
                st.audio(audio_file)

# Pie de página
st.markdown("---")
st.markdown(
    "<small>🔗 Suenia – Interpretador de sueños con IA | Mentor Digital Pro</small>",
    unsafe_allow_html=True
)
