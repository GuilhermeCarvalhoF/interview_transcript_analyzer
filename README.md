##### Interview Transcript Analyzer

A Streamlit-based web application that transcribes interview audio recordings and extracts structured HR insights, including candidate skills, tools, and experience. Designed for human resources teams to streamline candidate evaluation and support building an ATS (Applicant Tracking System).


##### Features

-  Upload audio recordings (`.mp3`, `.wav`, `.m4a`, `.ogg`)
-  Automatic transcription using OpenAI Whisper
-  Summarization using HuggingFace Transformers
-  Extracts:
-  Mentioned skills
-  Tools and technologies
-  Relevant experience phrases
-  Generate and download a professional PDF report
-  Export summaries for documentation or compliance
-  Simple, elegant, and responsive user interface


#### Tech Stack

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [OpenAI Whisper](https://github.com/openai/whisper) for transcription
- [HuggingFace Transformers](https://huggingface.co/transformers/) for summarization
- [spaCy](https://spacy.io/) for NLP parsing
- [FPDF](https://pyfpdf.github.io/fpdf2/) for PDF generation

---

#### Installation

**Clone the repository:**

git clone https://github.com/your-username/interview_transcript_analyzer.git
cd interview_transcript_analyzer
