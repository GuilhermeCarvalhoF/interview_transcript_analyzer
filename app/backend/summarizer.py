#########
## imports
#########

from transformers import pipeline

############
## summarizer model
############
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

############
## functions
############
def summarize_text(transcript: str) -> str:
    # since bart model has a limit of tokens I truncate the text to 3000 characters
    if len(transcript) > 3000:
        transcript = transcript[:3000]
    summary = summarizer(transcript, max_length=150, min_length=40, do_sample=False)
    return summary[0]["summary_text"]
