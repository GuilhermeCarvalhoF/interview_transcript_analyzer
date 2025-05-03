##########
## imports
##########

import streamlit as st
from backend.transcriber import transcriptor
from backend.summarizer import summarize_text

###########
## streamlit app
###########

st.title("Audio Transcriber")
st.subheader("Upload your audio file")

uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a", "ogg"])
if uploaded_file:
    st.audio(uploaded_file)
    with st.spinner("Generating transcription..."):
        transcription = transcriptor(uploaded_file)
        summary = summarize_text(transcription)
    st.subheader("Transcription")
    st.markdown(transcription)
    st.subheader("Summary:")
    st.markdown(summary)
