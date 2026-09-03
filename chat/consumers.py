"""Chat payload sanitation."""
from .services import MAX_MESSAGE_LENGTH
def clean_message(value):
    if not isinstance(value,str): raise ValueError('Message must be text')
    value=' '.join(value.split())[:MAX_MESSAGE_LENGTH]
    if not value: raise ValueError('Message cannot be empty')
    return value
