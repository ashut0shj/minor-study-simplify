from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors



fileName = 'flash.pdf'
documentTitle = 'sample'
title = 'Flash Cards'
textLines = [
    'Technology makes us aware of',
    'the world around us.',
]



pdf = canvas.Canvas(fileName)

pdf.setTitle(documentTitle)

pdf.setFont('Courier-Bold', 18)
pdf.drawCentredString(300, 770, title)

pdf.line(30, 710, 550, 710)

text = pdf.beginText(40, 680)
text.setFont("Courier", 12)
text.setFillColor(colors.black)
for line in textLines:
    text.textLine(line)
pdf.drawText(text)

pdf.save()