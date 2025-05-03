##########
## imports
##########

import streamlit as st
from backend.transcriber import transcriptor
from backend.summarizer import summarize_text

###########
## streamlit app
###########

st.set_page_config(page_title="Interview Analyzer", layout="centered")
st.title("🎙️ Interview Transcript Analyzer")
st.markdown("Upload an interview recording and extract a summary, skills, tools, and candidate experience.")

uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a", "ogg"])
if uploaded_file:
    st.audio(uploaded_file)
    with st.spinner("Generating transcription..."):
        transcription = transcriptor(uploaded_file)
        summary = summarize_text(transcription)
    st.subheader("Transcription")
    st.markdown(transcription)
    st.subheader("📝 Interview Summary")
    st.markdown(summary)
