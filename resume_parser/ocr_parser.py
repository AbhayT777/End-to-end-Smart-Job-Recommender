import pytesseract
from PIL import Image
from pdf2image import convert_from_path


def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)  # No need for poppler_path in Docker
    full_text = ""
    for image in images:
        text = pytesseract.image_to_string(image)
        full_text += text + "\n"
    return full_text
