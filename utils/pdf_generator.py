from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def gerar_pdf(dados):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4
    x = 40
    y = altura - 50
    linha_altura = 15

    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, "Relatório Diário de Ocorrências - GCM Guarulhos")
    y -= 30

    c.setFont("Helvetica", 10)

    if dados.empty:
        c.drawString(x, y, "Nenhuma ocorrência registrada.")
    else:
        colunas = dados.columns.tolist()
        for idx, col in enumerate(colunas):
            c.drawString(x + idx * 70, y, col[:12])
        y -= linha_altura

        for _, row in dados.iterrows():
            for idx, valor in enumerate(row):
                c.drawString(x + idx * 70, y, str(valor)[:12])
            y -= linha_altura
            if y < 50:
                c.showPage()
                y = altura - 50

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
