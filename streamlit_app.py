import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import tempfile
import webbrowser
import whisper
from playsound import playsound
from language_map import get_language_names, get_code_by_name, get_name_by_code, detect_language_code, is_voice_supported
import time

# Load Whisper model
whisper_model = whisper.load_model("base")
translator = Translator()

# KAI text rotation variants
kai_variants = ["KAI", "काई", "ਕਾਈ", "కాయి", "கை", "ಕೈ", "കൈ", "كاي", "カイ", "凯"]
kai_index = 0

st.set_page_config(page_title="kalakrit KAI", layout="wide")
st.markdown("""
    <style>
        .title-text {font-size: 36px; font-weight: bold; color: black;}
        .subtitle-text {font-size: 28px; font-weight: bold; color: black;}
        .support-title {font-size: 22px; font-weight: bold; color: black;}
        .card {border-radius: 10px; background-color: #FFFFFF; padding: 20px; margin: 10px;}
        .mic-btn, .speak-btn, .email-btn, .call-btn {
            background-color: #FF6D2F;
            border: none;
            padding: 10px 20px;
            color: white;
            font-weight: bold;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 8])
with col1:
    st.markdown('<span class="title-text">kalakrit</span>', unsafe_allow_html=True)
with col2:
    kai_placeholder = st.empty()

def rotate_kai():
    global kai_index
    kai_placeholder.markdown(f'<span class="subtitle-text">{kai_variants[kai_index]}</span>', unsafe_allow_html=True)
    kai_index = (kai_index + 1) % len(kai_variants)

rotate_kai()

# Language input and output section
col_in, col_out = st.columns(2)

with col_in:
    st.markdown("### 🎤 Input")
    if st.button("Start Speaking"):
        with st.spinner("Listening..."):
            r = sr.Recognizer()
            audio_path = os.path.join(tempfile.gettempdir(), "input.wav")
            with sr.Microphone() as source:
                audio = r.listen(source)
                with open(audio_path, "wb") as f:
                    f.write(audio.get_wav_data())
            try:
                result = whisper_model.transcribe(audio_path)
                user_text = result["text"]
                st.markdown(f"**Input Detected:** {user_text}")
                from_lang_code = detect_language_code(user_text)
                from_lang_name = get_name_by_code(from_lang_code)
                st.markdown(f"**Detected Language:** {from_lang_name}")

                st.info("Please speak the target language name...")
                with sr.Microphone() as source:
                    lang_audio = r.listen(source)
                    with open("lang_input.wav", "wb") as f:
                        f.write(lang_audio.get_wav_data())

                lang_result = whisper_model.transcribe("lang_input.wav")
                lang_name = lang_result["text"].strip()
                lang_code = get_code_by_name(lang_name)
                st.markdown(f"**Target Language:** {lang_name}")

                if not lang_code:
                    st.error("Could not detect or support this target language.")
                else:
                    translated = translator.translate(user_text, dest=lang_code).text
                    st.success(f"**Translated Text:** {translated}")
                    if is_voice_supported(lang_name):
                        tts = gTTS(text=translated, lang=lang_code)
                        temp_path = os.path.join(tempfile.gettempdir(), "output.mp3")
                        tts.save(temp_path)
                        playsound(temp_path)
                        os.remove(temp_path)
            except Exception as e:
                st.error(f"Error: {str(e)}")

with col_out:
    st.markdown("### 🔊 Output")
    st.write("You will hear the translated voice here if successful.")

# Support Section
st.markdown('<div class="support-title">Need Help? We\'re Here for You</div>', unsafe_allow_html=True)
col_w, col_c = st.columns(2)

with col_w:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Write to Us**")
    st.write("Reach us via email for translation help, app support, or collaboration queries.")
    if st.button("Write an Email"):
        webbrowser.open_new_tab("mailto:lokalisuno@kalakrit.in")
    st.markdown('</div>', unsafe_allow_html=True)

with col_c:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Call Support Helpline**")
    st.write("Available 7 days a week for urgent support or inquiries.")
    if st.button("Give us a call"):
        st.info("Call us at 7042190859")
    st.markdown('</div>', unsafe_allow_html=True)

# Hamburger Menu - top-right
with st.sidebar:
    st.header("☰ Menu")
    st.markdown("### About Us")
    st.info("Kalakrit KAI is an advanced multilingual voice translator...")

    st.markdown("### Partner with Kalakrit")
    st.info("Partner with us for EdTech, media, and education solutions.")

    st.markdown("### Services We Provide")
    st.info("Real-time translation, dubbing, voice-over, and more.")

    st.markdown("### Social Handles")
    st.markdown("[Instagram](https://www.instagram.com/kalakrit.in)")
    st.markdown("[Facebook](https://www.facebook.com/Kalakritofficial/)")
    st.markdown("[YouTube](https://www.youtube.com/@Kalakrit)")
    st.markdown("[LinkedIn](https://www.linkedin.com/company/kalakrit)")

# Footer
st.markdown("---")
st.markdown("<center><strong>kalakrit Studios</strong></center>", unsafe_allow_html=True)

# Auto KAI rotation every 3 seconds
import asyncio
async def auto_rotate():
    while True:
        rotate_kai()
        await asyncio.sleep(3)

# Only run on script launch
if kai_index == 1:
    asyncio.run(auto_rotate())
