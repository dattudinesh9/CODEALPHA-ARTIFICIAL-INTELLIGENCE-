# translation_app.py
import streamlit as st
import requests
from gtts import gTTS
import io
import base64

st.set_page_config(page_title="AI Translator", page_icon="🌐")

st.title("🌐 AI Language Translation Tool")
st.markdown("---")

# Language options
languages = {
    'English': 'en', 'Hindi': 'hi', 'Spanish': 'es',
    'French': 'fr', 'German': 'de', 'Japanese': 'ja',
    'Chinese': 'zh', 'Russian': 'ru', 'Arabic': 'ar'
}

# Layout using columns
col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("From:", languages.keys(), index=0)

with col2:
    target_lang = st.selectbox("To:", languages.keys(), index=1)

# Text input
text = st.text_area("Enter text:", height=150)

if st.button("Translate", type="primary"):
    if text:
        with st.spinner("Translating..."):
            # Translation API call
            url = "https://api.mymemory.translated.net/get"
            params = {
                'q': text,
                'langpair': f'{languages[source_lang]}|{languages[target_lang]}'
            }

            response = requests.get(url, params=params)
            translated = response.json()['responseData']['translatedText']

            # Display result
            st.success("Translation complete!")

            col3, col4 = st.columns(2)
            with col3:
                st.info(f"**{source_lang}:**")
                st.write(text)
            with col4:
                st.info(f"**{target_lang}:**")
                st.write(translated)

            # Copy button (Streamlit has built-in)
            st.code(translated, language="text")
    else:
        st.warning("Please enter text to translate")
