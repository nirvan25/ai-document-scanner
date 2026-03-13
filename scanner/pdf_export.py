from fpdf import FPDF


def create_pdf(image_path, text, output_pdf):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    # Add scanned image
    pdf.image(image_path, x=10, y=10, w=190)

    pdf.ln(140)

    # Fix unicode characters
    clean_text = text.encode("latin-1", "replace").decode("latin-1")

    for line in clean_text.split("\n"):
        pdf.cell(0, 8, txt=line, ln=True)

    pdf.output(output_pdf)