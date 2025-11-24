from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io
import argparse
import os
from datetime import datetime

def add_watermark(input_pdf, output_pdf, text):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page in reader.pages:
        # Get page size
        width = page.mediabox.width
        height = page.mediabox.height

        # Create watermark
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(width, height))
        c.setFillAlpha(0.2)
        c.setFillColorRGB(0.7, 0.7, 0.7)
        c.setFont("Helvetica-Bold", 20)

        # add date text
        date_str = datetime.now().strftime("%Y%m%d")

        # Simple repeating grid - GUARANTEED to finish
        offset_x = 180
        offset_y = 180
        for x in range(-100, int(width) + 300, offset_x):
            for y in range(-100, int(height) + 300, offset_y):
                c.saveState()
                c.translate(x, y)
                c.rotate(45)

                c.drawCentredString(0, 0, text)
                # add date below watermark
                c.drawCentredString(0, -20, date_str)

                c.restoreState()

        c.save()
        packet.seek(0)
        watermark = PdfReader(packet).pages[0]

        page.merge_page(watermark)
        writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)
    
    print(f"Watermarked PDF saved as: {output_pdf}")

def cli():
    parser = argparse.ArgumentParser(description="Add watermark to PDF")
    parser.add_argument("-i", "--input", required=True, help="Input PDF file path")
    parser.add_argument("-o", "--output", help="Output PDF file path")
    parser.add_argument("-m", "--watermark", default="CONFIDENTIAL", help="Watermark text")

    args = parser.parse_args()
    if args.output is None:
        base, ext = os.path.splitext(args.input)
        args.output = f"{base}-watermarked{ext}"
    add_watermark(args.input, args.output, args.watermark)

if __name__ == "__main__":
    cli()