"""Message validation shared by polling now and WebSocket consumers later."""
ALLOWED_EVENTS={'board','chat','hand','presence','offer','answer','ice','recording'}
def validate_event(event):
    if not isinstance(event,dict) or event.get('type') not in ALLOWED_EVENTS: raise ValueError('Unsupported realtime event')
    return event
