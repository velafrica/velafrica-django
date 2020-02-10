import io
import os

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen.canvas import Canvas

from velafrica.core.settings import PROJECT_DIR


# PDF-PLOT

def pdf_page_frame(canvas, logo=None):
    if logo:
        canvas.drawImage(logo, x=657.5, y=471, width=2466 / 15, height=1565 / 15)

    # End Page
    canvas.showPage()


def draw_pdf_page(canvas, table=[], extraordinary=None, title=None, image=None, logo=None, fontsize=12):
    # Header - Title and Logo
    if title:
        canvas.setFont("Helvetica", 32)
        canvas.drawString(x=40, y=510, text=title)

    # Content
    canvas.setFont("Helvetica", fontsize)

    # Table
    y = 450 - fontsize  # origin of coordinates is bottom left
    for (label, value) in table:
        canvas.drawString(40, y, label)

        # breaks lines if too long and then draw line by line
        for line in simpleSplit(text=value, fontName=canvas._fontname, fontSize=canvas._fontsize, maxWidth=130):
            canvas.drawString(175, y, line)
            y -= 15
        y -= 6  # add spacing between two rows

    if extraordinary:
        canvas.drawString(40, y, "Extraordinary:")
        y -= 16
        for line in simpleSplit(text=extraordinary, fontName=canvas._fontname, fontSize=canvas._fontsize, maxWidth=255):
            canvas.drawString(50, y, line)
            y -= 15

    # plot image
    if image:
        try:
            w = 480
            h = image.height / image.width * w  # keep ratio
            canvas.drawImage(image.url, x=321.9, y=450 - h, width=w, height=h)
        except IOError:
            print("Image not found");

    pdf_page_frame(canvas, logo)


def render_bikes_to_pdf_with_reportlab(queryset, fields={}, title=None, subtitle=None):
    buf = io.BytesIO()
    canvas = Canvas(buf, pagesize=landscape(A4))  # W, H = landscape(A4)  # 841.9, 595.27

    logo = os.path.join(PROJECT_DIR, 'frontend', 'static', 'img/velafrica_RGB.jpg')

    # title page
    canvas.setFont("Helvetica", 28)
    canvas.drawCentredString(text=title, x=841.9/2, y=300)
    canvas.setFont("Helvetica", 20)
    canvas.drawCentredString(text=subtitle, x=841.9/2, y=270)
    pdf_page_frame(canvas, logo)

    # bike pages
    for bike in queryset:
        draw_pdf_page(
            canvas=canvas,
            table=[
                (label, "{}".format(bike.__getattribute__(key)))
                for key, label in fields.items()
                if bike.__getattribute__(key)  # if not blank
            ],
            extraordinary=bike.extraordinary,
            image=bike.image,
            logo=logo,
            title="A+ Bike"
        )

    # Close the PDF object cleanly
    canvas.save()
    buf.seek(0)

    return buf.getvalue()
