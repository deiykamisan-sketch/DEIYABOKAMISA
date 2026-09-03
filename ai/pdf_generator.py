"""Export lecture notes to a readable PDF."""
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet
def create_lecture_pdf(path,notes):
    styles=getSampleStyleSheet(); story=[Paragraph(notes['title'],styles['Title']),Spacer(1,12),Paragraph('Summary',styles['Heading2']),Paragraph(notes['summary'] or 'No summary.',styles['BodyText']),Spacer(1,12),Paragraph('Transcript',styles['Heading2'])]
    story.extend(Paragraph(line,styles['BodyText']) for line in (notes['transcript'] or 'No transcript.').splitlines())
    SimpleDocTemplate(str(path),pagesize=A4).build(story); return path
