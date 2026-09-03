"""OCR adapter with an explicit optional dependency."""
def recognize_image(image):
    try: import pytesseract
    except ImportError as exc: raise RuntimeError('Install pytesseract and the Tesseract application to enable OCR') from exc
    return pytesseract.image_to_string(image).strip()
