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
    summary_text = summary[0]["summary_text"]

    sentences = summary_text.split('. ')
    sentences = [s.strip().rstrip('.') for s in sentences if s.strip()]

    summary_points = []
    decisions = []
    actions = []


    action_keywords = [
        "will", "assigned", "responsible", "needs to", "task", "follow up", "due",
        "to-do", "scheduled", "submit", "send", "deliver", "complete", "prepare",
        "required", "must", "should", "deadline", "action", "finalize", "implement", "coordinate"
    ]

    decision_keywords = [
        "decided", "agreed", "approved", "concluded", "confirmed", "chosen", "voted",
        "selected", "resolved", "final decision", "consensus", "reached an agreement",
        "settled", "opted", "plan is to", "will proceed with"
    ]

    for sentence in sentences:
        s_lower = sentence.lower()
        if any(kw in s_lower for kw in action_keywords):
            actions.append(sentence)
        elif any(kw in s_lower for kw in decision_keywords):
            decisions.append(sentence)
        else:
            summary_points.append(sentence)

    def bullet(lines):
        return '\n'.join(f"- {line}" for line in lines) if lines else "- (none found)"

    return bullet(summary_points)
