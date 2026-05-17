from xhtml2pdf import pisa
from flask import render_template
import os

def generate_pdf_report(company_name, report_data):

    rendered = render_template(
        "report_template.html",
        company_name=company_name,
        report=report_data
    )

    os.makedirs("reports", exist_ok=True)

    pdf_path = f"reports/{company_name}.pdf"

    with open(pdf_path, "w+b") as pdf_file:

        pisa.CreatePDF(
            rendered,
            dest=pdf_file
        )

    return pdf_path