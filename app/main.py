##########
## imports
##########

import streamlit as st
from backend.transcriber import transcriptor
from backend.summarizer import summarize_text
from backend.interview_parser import extract_elements
import tempfile

###########
## streamlit app
###########

st.set_page_config(page_title="Interview Analyzer", layout="centered")
st.title("🎙️ Interview Transcript Analyzer")
st.markdown("Upload an interview recording and extract a summary, skills, tools, and candidate experience.")

############
## file uploader
############

uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a", "ogg"])


if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    st.audio(uploaded_file, format="audio/mp3")

    # Transcription
    with st.spinner("🔍 Transcribing audio..."):
        transcript = transcriptor(temp_path)

    st.subheader("📜 Transcript")
    st.markdown(transcript)

    # Summary & Info Extraction
    if st.button("🧠 Analyze Interview"):
        with st.spinner("Analyzing content..."):
            summary = summarize_text(transcript)
            details = extract_elements(transcript)

        st.subheader("📝 Interview Summary")
        st.markdown(summary)

        st.subheader("💼 Candidate Highlights")
        st.markdown(f"**Skills Mentioned:** {', '.join(details['skills']) or 'None'}")
        st.markdown(f"**Tools/Technologies:** {', '.join(details['tools']) or 'None'}")

        st.markdown("**Experience Mentions:**")
        if details["experience_phrases"]:
            for xp in details["experience_phrases"]:
                st.markdown(f"- {xp}")
        else:
            st.markdown("- None found")
