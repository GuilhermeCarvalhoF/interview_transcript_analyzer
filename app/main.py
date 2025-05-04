##########
# Imports
##########

import streamlit as st
from backend.transcriber import transcriptor
from backend.summarizer import summarize_text
from backend.interview_parser import extract_elements
from fpdf import FPDF
from io import BytesIO
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
        ## pdf file
        ##########

        def create_pdf(summary, details, transcript):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Interview Report", ln=True)

            pdf.set_font("Arial", '', 12)
            pdf.ln(10)

            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, "Summary", ln=True)
            pdf.set_font("Arial", '', 12)
            for line in summary.strip().split('\n'):
                pdf.multi_cell(0, 8, line)
            pdf.ln(5)

            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, "Skills Mentioned", ln=True)
            pdf.set_font("Arial", '', 12)
            skills = ', '.join(details['skills']) or 'None'
            pdf.multi_cell(0, 8, skills)
            pdf.ln(5)

            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, "Tools & Technologies", ln=True)
            pdf.set_font("Arial", '', 12)
            tools = ', '.join(details['tools']) or 'None'
            pdf.multi_cell(0, 8, tools)
            pdf.ln(5)

            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, "Experience Mentions", ln=True)
            pdf.set_font("Arial", '', 12)
            if details['experience_phrases']:
                for phrase in details['experience_phrases']:
                    pdf.multi_cell(0, 8, f"- {phrase}")
            else:
                pdf.multi_cell(0, 8, "- None found")
            pdf.ln(5)

            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, "Full Transcript", ln=True)
            pdf.set_font("Arial", '', 12)
            pdf.multi_cell(0, 8, transcript)

            pdf.set_y(-15)
            pdf.set_font("Arial", "I", 10)
            pdf.set_text_color(150)
            pdf.cell(0, 10, "Developed by Guilherme Fernandez", 0, 0, "C")

            buffer = BytesIO()
            pdf_bytes = pdf.output(dest='S').encode('latin1') # This change was necessary in order to include latin origin characters
            buffer.write(pdf_bytes)
            buffer.seek(0)
            return buffer

        pdf_buffer = create_pdf(summary, details, transcript)


        ##########
        # Download report
        ##########

        st.download_button(
            label="💾 Download Report as PDF",
            data=pdf_buffer,
            file_name="interview_report.pdf",
            mime="application/pdf"
        )

st.markdown(
    "<hr style='margin-top: 50px;'><div style='text-align: center; color: gray;'>Developed by Guilherme Fernandez</div>",
    unsafe_allow_html=True
)
