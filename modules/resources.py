import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_worksheet_pdf():
    """Generates a downloadable PDF worksheet for teachers."""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, 750, "Graph Explorer — Student Practice Worksheet")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 720, "Name: ______________________     Date: ____________")
    
    questions = [
        "1. Plot y = 2x - 3. What is the y-intercept?",
        "2. Find the roots of y = x^2 - 4.",
        "3. Determine the vertex of y = -(x - 2)^2 + 3. Is it a maximum or minimum?",
        "4. How does increasing coefficient 'a' affect y = a*sin(x)?",
        "5. Calculate the gradient of y = 3x^2 at x = 2."
    ]
    
    y = 660
    for q in questions:
        p.drawString(50, y, q)
        p.rect(50, y - 45, 500, 35)  # Box for student answer
        y -= 75
        
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
