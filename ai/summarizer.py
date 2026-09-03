"""Deterministic extractive summary fallback for operation without a paid AI API."""
import re
def summarize(text,max_sentences=5):
    sentences=[s.strip() for s in re.split(r'(?<=[.!?])\s+',text) if s.strip()]
    if len(sentences)<=max_sentences:return ' '.join(sentences)
    words=re.findall(r"\b[\w'-]{4,}\b",text.lower()); freq={w:words.count(w) for w in set(words)}
    ranked=sorted(enumerate(sentences),key=lambda x:sum(freq.get(w,0) for w in re.findall(r'\w+',x[1].lower())),reverse=True)[:max_sentences]
    return ' '.join(sentence for _,sentence in sorted(ranked))
