import streamlit as st
from gtts import gTTS
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
from pydub import AudioSegment
import tempfile
import io

st.set_page_config(page_title="VocalBridge", page_icon="🎙️", layout="centered")

st.title("🎙️ VocalBridge")
st.caption("Speech-to-Text & Text-to-Speech System")

tab1, tab2 = st.tabs(["🔊 Text to Speech", "📝 Speech to Text"])

with tab1:
    st.subheader("Convert Text to Speech")
    text_input = st.text_area("Enter your text:", height=150, placeholder="Type something here...")
    lang = st.selectbox("Select language", options=["en", "te", "hi"],
                         format_func=lambda x: {"en": "English", "te": "Telugu", "hi": "Hindi"}[x])

    if st.button("🔁 Convert to Speech", use_container_width=True):
        if not text_input.strip():
            st.warning("Please enter some text first.")
        else:
            with st.spinner("Generating audio..."):
                tts = gTTS(text=text_input, lang=lang)
                temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                tts.save(temp_path)
            st.success("Audio generated successfully!")
            st.audio(temp_path, format="audio/mp3")

with tab2:
    st.subheader("Convert Speech to Text")
    st.write("🎤 Click the mic below and speak:")

    audio_bytes = audio_recorder(text="", icon_size="3x", pause_threshold=2.0)

    if audio_bytes is not None:
        st.audio(audio_bytes, format="audio/wav")

        with st.spinner("Transcribing..."):
            try:
                # Convert recorded bytes (webm/wav) to proper WAV using pydub
                audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
                wav_io = io.BytesIO()
                audio_segment.export(wav_io, format="wav")
                wav_io.seek(0)

                recognizer = sr.Recognizer()
                with sr.AudioFile(wav_io) as source:
                    audio_data = recognizer.record(source)

                result_text = recognizer.recognize_google(audio_data)
                st.success("Transcription complete!")
                st.info(result_text)

            except sr.UnknownValueError:
                st.error("Could not understand the audio. Please speak clearly and try again.")
            except sr.RequestError:
                st.error("Speech recognition service unavailable. Check your internet connection.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.markdown("---")
st.caption("VocalBridge | Built using Python, SpeechRecognition, gTTS and Streamlit")