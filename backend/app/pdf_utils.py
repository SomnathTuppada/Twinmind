import pdfplumber

def extract_text_from_pdf(path):
    texts = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            t = page.extract_text() or ""
            texts.append({"page": i, "text": t})
    return texts
