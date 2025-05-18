import streamlit.components.v1 as components

def audio_recorder():
    html = """
    <div style="text-align:center">
      <button id="rec">🎤 Grabar</button>
    </div>
    <script>
      let mediaRecorder;
      let audioChunks = [];
      let recording = false;
      const recButton = document.getElementById('rec');
      recButton.onclick = async () => {
        if (!recording) {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.start();
          audioChunks = [];
          recording = true;
          recButton.textContent = '⏹️ Detener';
          mediaRecorder.addEventListener('dataavailable', e => audioChunks.push(e.data));
          mediaRecorder.addEventListener('stop', () => {
            const blob = new Blob(audioChunks);
            const reader = new FileReader();
            reader.readAsDataURL(blob);
            reader.onloadend = () => {
              const base64 = reader.result.split(',')[1];
              window.parent.streamlit.setComponentValue(base64);
              recButton.textContent = '🎤 Grabar';
              recording = false;
            };
          });
        } else {
          mediaRecorder.stop();
        }
      };
    </script>
    """
    return components.html(html, height=100)
