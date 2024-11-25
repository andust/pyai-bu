import io
from pypdf import PdfReader


def pdf_to_text(file_data_content: bytes) -> list[str]:
    pages_text = []
    pdf_file = io.BytesIO(file_data_content)
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        pages_text.append(page.extract_text())

    return pages_text
