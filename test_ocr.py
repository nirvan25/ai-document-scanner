from scanner.ocr import extract_text

text = extract_text("output/receipt.png")

print(text)