from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO

def gerar_pdf(dados):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elementos = []

    styles = getSampleStyleSheet()
    titulo = Paragraph("Relatório de Ocorrências - GCM Guarulhos", styles["Title"])
    elementos.append(titulo)
    elementos.append(Spacer(1, 12))

    if dados.empty:
        elementos.append(Paragraph("Nenhuma ocorrência encontrada.", styles["Normal"]))
    else:
        # Converte DataFrame em lista de listas (tabela)
        #tabela_dados = [list(dados.columns)] + dados.values.tolist()
        # Converte DataFrame em lista de listas (tabela), forçando texto
tabela_dados = [list(map(str, dados.columns))] + dados.astype(str).values.tolist()

        tabela = Table(tabela_dados, repeatRows=1)

        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),   # Cabeçalho cinza
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),        # Texto preto no cabeçalho
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),                 # Alinhamento à esquerda
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),     # Cabeçalho em negrito
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),              # Espaçamento abaixo do cabeçalho
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),        # Grade em todas as células
        ]))

        elementos.append(tabela)

    doc.build(elementos)
    buffer.seek(0)
    return buffer
