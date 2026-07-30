function showTab(tabId) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
  event.target.classList.add('active');
}

async function convertToSpeech() {
  const text = document.getElementById('text-input').value;
  const lang = document.getElementById('lang-select').value;
  const resultDiv = document.getElementById('tts-result');

  if (!text.trim()) {
    resultDiv.innerHTML = '⚠️ Please enter some text first.';
    return;
  }

  resultDiv.innerHTML = 'Generating audio...';

  const res = await fetch('/text-to-speech', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, lang })
  });

  const data = await res.json();

  if (data.audio_url) {
    resultDiv.innerHTML = `<audio controls src="${data.audio_url}"></audio>`;
  } else {
    resultDiv.innerHTML = `❌ ${data.error}`;
  }
}

async function convertToText() {
  const fileInput = document.getElementById('audio-upload');
  const resultDiv = document.getElementById('stt-result');

  if (!fileInput.files.length) {
    resultDiv.innerHTML = '⚠️ Please upload a WAV file first.';
    return;
  }

  const formData = new FormData();
  formData.append('audio', fileInput.files[0]);

  resultDiv.innerHTML = 'Transcribing...';

  const res = await fetch('/speech-to-text', {
    method: 'POST',
    body: formData
  });

  const data = await res.json();

  if (data.text) {
    resultDiv.innerHTML = `<strong>Transcribed:</strong> ${data.text}`;
  } else {
    resultDiv.innerHTML = `❌ ${data.error}`;
  }
}