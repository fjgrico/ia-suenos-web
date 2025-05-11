import streamlit as st
import os
from audiorecorder import audiorecorder
from openai import OpenAI
from tempfile import NamedTemporaryFile

# 🔐 Cargar API key desde variable de entorno o secrets.toml (en local)
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.stop()
client = OpenAI(api_key=api_key)

# 🎨 Configurar página
st.set_page_config(page_title="💤 Suenia | Interpretador de Sueños", layout="centered")

# 💤 Encabezado
st.markdown("<h1 style='text-align: center;'>💤 Suenia</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Interpreta tus sueños con Inteligencia Artificial</h3>", unsafe_allow_html=True)
st.markdown("---")

# 📝 Estado inicial
if "texto_sueno" not in st.session_state:
    st.session_state.texto_sueno = ""

# ✍️ Cuadro editable siempre visible
st.subheader("✍️ Escribe o revisa aquí tu sueño:")
texto_editado = st.text_area("📝", value=st.session_state.texto_sueno, height=150, key="input_sueno")

# 🎙️ Grabadora
st.subheader("🎙️ O graba tu sueño con tu voz:")
audio = audiorecorder("🎤 Iniciar grabación", "⏹️ Detener grabación", key="grabadora")

if len(audio) > 0:
    st.audio(audio.export().read(), format="audio/wav")
    audio_bytes = audio.export().read()

    with NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_path = tmp_file.name

    with st.spinner("🎧 Transcribiendo tu audio..."):
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=open(tmp_path, "rb"),
            response_format="text"
        )
        st.session_state.texto_sueno = transcription
        texto_editado = transcription
        st.success("✅ Transcripción lista")

# 🔮 Interpretación
st.markdown("---")
st.subheader("🔮 Interpretar el sueño")

if st.button("✨ Analizar sueño con IA", key="interpretar_btn") and texto_editado.strip():
    with st.spinner("🧠 Analizando desde distintas perspectivas..."):

        prompt = f"""
Eres un intérprete de sueños experto. A partir del siguiente sueño:
\"\"\"{texto_editado}\"\"\"

Proporciona una interpretación desde cada uno de estos enfoques:
1. Freudiana
2. Jungiana
3. Emocional
4. Espiritual
5. Chamánica
6. Taoísta/Budista
7. Nativo Americano (Hopi)
8. Africana Ancestral
9. Profesional/Vocacional
10. Familiar y Amorosa

Después, incluye:
- Una conclusión general del sueño.
- Una reflexión personal para el soñador.
- Tres preguntas para seguir explorando su significado.
"""

        respuesta = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.85
        )

        interpretacion = respuesta.choices[0].message.content
        st.markdown("## 🧠 Interpretación completa")
        st.markdown(interpretacion)

# 👣 Footer
st.markdown("---")
st.markdown("<small>🔗 Suenia – Interpretador de sueños con IA | Mentor Digital Pro</small>", unsafe_allow_html=True)
