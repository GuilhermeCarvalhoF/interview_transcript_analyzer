##########
# Imports
##########

import streamlit as st
from backend.transcriber import transcriptor
from backend.summarizer import summarize_text
from backend.interview_parser import extract_elements
import tempfile

##########
# Page Config & Styling
##########

st.set_page_config(page_title="Interview Analyzer", layout="centered")
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 16px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
        }

        .stDownloadButton>button {
            background-color: #2196F3;
            color: white;
            padding: 10px 16px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
        }

        .reportview-container .main .block-container{
            max-width: 800px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)


st.title("🎙️ Interview Transcript Analyzer")
st.markdown("Upload an interview recording and extract a summary, skills, tools, and candidate experience.")

##########
# File Upload
##########

uploaded_file = st.file_uploader("📂 Choose an audio file", type=["mp3", "wav", "m4a", "ogg"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    st.audio(uploaded_file, format="audio/mp3")

    with st.spinner("🔍 Transcribing audio..."):
        transcript = transcriptor(temp_path)

    st.success("✅ Transcription completed!")

    if st.button("🧠 Analyze Interview"):
        with st.spinner("🔎 Analyzing content..."):
            summary = summarize_text(transcript)
            details = extract_elements(transcript)

        ##########
        # Tabs for output
        ##########

        tab1, tab2, tab3 = st.tabs(["📜 Transcript", "📝 Summary", "💼 Candidate Highlights"])

        with tab1:
            st.markdown(transcript)

        with tab2:
            st.markdown(summary)

        with tab3:
            st.markdown(f"**Skills Mentioned:** {', '.join(details['skills']) or 'None'}")
            st.markdown(f"**Tools/Technologies:** {', '.join(details['tools']) or 'None'}")
            st.markdown("**Experience Mentions:**")
            if details["experience_phrases"]:
                for xp in details["experience_phrases"]:
                    st.markdown(f"- {xp}")
            else:
                st.markdown("- None found")

        ##########
        # Download report
        ##########

        st.subheader("📥 Download Full Report")

        report_content = f"""
Interview Summary:
{summary}

Skills Mentioned: {', '.join(details['skills']) or 'None'}
Tools/Technologies: {', '.join(details['tools']) or 'None'}

Experience Mentions:
{chr(10).join(['- ' + xp for xp in details['experience_phrases']]) or '- None found'}

Full Transcript:
{transcript}
"""

        st.download_button(
            label="💾 Download Report as .pdf",
            data=report_content,
            file_name="interview_report.pdf",
            mime="text/plain"
        )
