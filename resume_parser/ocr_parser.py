import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os

# Set this if tesseract is not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path, poppler_path=r"C:\Users\abhay\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin")
    full_text = ""
    for image in images:
        text = pytesseract.image_to_string(image)
        full_text += text + "\n"
    return full_text
