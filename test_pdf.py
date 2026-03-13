from scanner.ocr import extract_text
from scanner.pdf_export import create_pdf

image = "output/linkedin_about.png"

text = extract_text(image)

create_pdf(image, text, "output/result.pdf")

print("PDF created successfully!")