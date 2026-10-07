from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


def generate_certificate(
    recipient_name: str,
    event_name: str,
    date: str,
    output_path: str
):
    width, height = A4

    pdf = canvas.Canvas(output_path, pagesize=A4)

    # Title
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        width / 2,
        height - 70 * mm,
        "CERTIFICATE"
    )

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(
        width / 2,
        height - 85 * mm,
        "OF PARTICIPATION"
    )

    # Description
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(
        width / 2,
        height - 115 * mm,
        "This certificate is proudly presented to"
    )

    # Recipient name
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(
        width / 2,
        height - 135 * mm,
        recipient_name
    )

    # Event
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(
        width / 2,
        height - 160 * mm,
        f"for participating in {event_name}"
    )

    # Date
    pdf.drawCentredString(
        width / 2,
        height - 180 * mm,
        f"Date: {date}"
    )

    pdf.save()
    
