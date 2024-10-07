import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import streamlit as st
import os

# Mapping for language display
LANGUAGE_OPTIONS = {
    "Hindi": "hi-IN",
    "Kannada": "kn-IN",
    "Telugu": "te-IN",
    "Tamil": "ta-IN",
    "Malayalam": "ml-IN",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Russian": "ru"
}

# Speech Recognition Function
def recognize_speech(language_code):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak something.")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language=language_code)
            st.success(f"Recognized Speech: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")

    return None

# Translation Function
def translate_text(input_text, target_language_code='en'):
    try:
        translation = GoogleTranslator(source='auto', target=target_language_code).translate(input_text)
        return translation
    except Exception as e:
        st.error(f"Translation error: {e}")
        return None

# Text-to-Speech Function using gTTS
def text_to_speech(text, language_code='en'):
    try:
        tts = gTTS(text=text, lang=language_code)
        tts.save("translated_audio.mp3")
        return "translated_audio.mp3"
    except Exception as e:
        st.error(f"Text-to-Speech error: {e}")
        return None

# Streamlit App UI Layout
def main():
    st.title("🌐 Multilingual Live & Text Translator")

    # Choose between Text and Live Speech Translation
    translation_mode = st.radio("Choose Translation Mode:", ('Text Translation', 'Live Speech Translation'))

    if translation_mode == 'Text Translation':
        st.subheader("Text Translator")

        # Input text for translation
        input_text = st.text_area("Enter text to translate", "")

        # Target language selection (user-friendly)
        target_language_name = st.selectbox(
            "Select target language for translation",
            list(LANGUAGE_OPTIONS.keys())  # Display language names
        )
        target_language_code = LANGUAGE_OPTIONS[target_language_name]  # Get the corresponding language code

        if st.button("Translate Text"):
            if input_text:
                translated_text = translate_text(input_text, target_language_code)
                if translated_text:
                    st.success(f"Translated Text: {translated_text}")
                    st.write("Playing the translated text as speech...")

                    # Convert translated text to speech
                    audio_file = text_to_speech(translated_text, target_language_code)
                    if audio_file:
                        # Use Streamlit's audio player to play the audio
                        audio_bytes = open(audio_file, 'rb').read()
                        st.audio(audio_bytes, format='audio/mp3')

    elif translation_mode == 'Live Speech Translation':
        st.subheader("Live Speech Translator")

        # Select source language for speech recognition
        source_language_name = st.selectbox(
            "Select your language for speech recognition",
            list(LANGUAGE_OPTIONS.keys())  # Display language names
        )
        source_language_code = LANGUAGE_OPTIONS[source_language_name]  # Get the corresponding language code

        # Target language selection (user-friendly)
        target_language_name = st.selectbox(
            "Select target language for translation",
            list(LANGUAGE_OPTIONS.keys())  # Display language names
        )
        target_language_code = LANGUAGE_OPTIONS[target_language_name]  # Get the corresponding language code

        if st.button("Start Listening"):
            input_text = recognize_speech(source_language_code)
            if input_text:
                translated_text = translate_text(input_text, target_language_code)
                if translated_text:
                    st.success(f"Translated Speech: {translated_text}")
                    st.write("Playing the translated text as speech...")

                    # Convert translated text to speech
                    audio_file = text_to_speech(translated_text, target_language_code)
                    if audio_file:
                        # Use Streamlit's audio player to play the audio
                        audio_bytes = open(audio_file, 'rb').read()
                        st.audio(audio_bytes, format='audio/mp3')

if __name__ == "__main__":
    main()
