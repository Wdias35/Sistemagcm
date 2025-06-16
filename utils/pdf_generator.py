from fpdf import FPDF

class PDFGenerator:
    def gerar_pdf(self, dados):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "Relatório de Ocorrências", ln=True, align="C")
        for d in dados:
            linha = ", ".join([f"{k}: {v}" for k, v in d.items()])
            pdf.multi_cell(0, 10, linha)
        return pdf.output(dest='S').encode('latin-1')