from fpdf import FPDF

class PDFGenerator:
    def gerar_pdf(self, dados):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Relatório de Ocorrências", ln=1, align='C')

        if dados.empty:
            pdf.cell(200, 10, txt="Nenhum dado para exibir.", ln=1)
        else:
            colunas = dados.columns.tolist()
            largura_col = 190 // len(colunas)
            for c in colunas:
                pdf.cell(largura_col, 10, c, 1, 0, 'C')
            pdf.ln()

            for index, row in dados.iterrows():
                for c in colunas:
                    pdf.cell(largura_col, 10, str(row[c]), 1, 0, 'C')
                pdf.ln()

        return pdf.output(dest='S').encode('latin1')

