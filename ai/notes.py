"""Generate structured lecture notes from a transcript."""
from .summarizer import summarize
def build_notes(title,transcript):
    return {'title':title,'summary':summarize(transcript),'transcript':transcript,
            'review_questions':['What was the main concept?','Which example was demonstrated?','What should be reviewed next?']}
