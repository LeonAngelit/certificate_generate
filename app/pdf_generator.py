import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from PyPDF2 import PdfReader, PdfWriter

def create_custom_pdf(name, score, date, countries, logo_path, template_path, output_path):
    overlay_filename = "overlay.pdf"
    page_size = landscape(A4)
    c = canvas.Canvas(overlay_filename, pagesize=page_size)

    # Name
    c.setFont("Helvetica-Bold", 24)
    c.drawString(376, 300, name)

    # Score
    c.setFont("Helvetica-Bold", 14)
    c.drawString(470, 266, score)

    # Country lines
    y = 213
    for i, country_text in enumerate(countries[:5]):
        text = country_text
        c.drawString(310, y, text)
        y -= 17

    # Date
    c.setFont("Helvetica-Bold", 18)
    c.drawString(325, 85, date)

    # Logo
    c.drawImage(logo_path, x=30, y=500, width=220, height=86, mask='auto')

    c.save()

    # Merge with template
    template_pdf = PdfReader(open(template_path, "rb"))
    overlay_pdf = PdfReader(open(overlay_filename, "rb"))

    writer = PdfWriter()
    template_page = template_pdf.pages[0]
    overlay_page = overlay_pdf.pages[0]
    template_page.merge_page(overlay_page)
    writer.add_page(template_page)

    with open(output_path, "wb") as output_file:
        writer.write(output_file)

def parse_args():
    parser = argparse.ArgumentParser(description="Generate a custom PDF with dynamic text and logo.")
    parser.add_argument("--name", required=True, help="Name to appear on PDF.")
    parser.add_argument("--score", required=True, help="Score to display.")
    parser.add_argument("--date", required=True, help="Date in dd/mm/yyyy format.")
    parser.add_argument("--countries", required=True, nargs='+', help="Country entries, e.g., 'País 1: 999 puntos'")
    parser.add_argument("--logo", default="./templates/logo.png", help="Path to logo image.")
    parser.add_argument("--template", default="./templates/template.pdf", help="Path to template PDF.")
    parser.add_argument("--output", default="final_output.pdf", help="Output PDF filename.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    create_custom_pdf(
        name=args.name,
        score=args.score,
        date=args.date,
        countries=args.countries,
        logo_path=args.logo,
        template_path=args.template,
        output_path=args.output
    )
