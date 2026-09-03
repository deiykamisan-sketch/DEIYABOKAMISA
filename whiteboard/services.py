"""Whiteboard event validation and snapshot services."""

MAX_CANVAS_DATA_LENGTH = 6_000_000

def valid_canvas_image(value):
    return value.startswith('data:image/png;base64,') and len(value) <= MAX_CANVAS_DATA_LENGTH
