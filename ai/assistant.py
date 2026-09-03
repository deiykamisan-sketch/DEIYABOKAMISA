"""Human-approved AI answer workflow."""
from dataclasses import dataclass
@dataclass
class AnswerSuggestion:
    question:str
    answer:str
    approved:bool=False
    def approve(self): self.approved=True; return self
def fallback_suggestion(question):
    return AnswerSuggestion(question, 'AI provider is not configured. The lecturer should answer this question.')
