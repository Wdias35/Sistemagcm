from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def gerar_pdf(dados):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    y = altura - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Relatório de Ocorrências - GCM Guarulhos")
    y -= 30

    c.setFont("Helvetica", 10)
    for idx, row in dados.iterrows():
        linha = f"{row.get('Data', '')} - {row.get('Horário', '')} - {row.get('Local', '')} - {row.get('Base Responsável', '')} - {row.get('Tipo de Ocorrência', '')} - {row.get('Latitude', '')} - {row.get('Longitude', '')}"
        c.drawString(50, y, linha)
        y -= 15
        if y < 50:
            c.showPage()
            y = altura - 50

    c.save()
    buffer.seek(0)
    return buffer
