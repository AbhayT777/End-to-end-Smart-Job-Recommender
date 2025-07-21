import pytesseract
from PIL import Image
from pdf2image import convert_from_path


def extract_text_from_image(image_path):
    image = Image.open(image_path).convert("L")  # Convert to grayscale for faster OCR
    return pytesseract.image_to_string(image)


def extract_text_from_pdf(pdf_path):
    # Convert only the first few pages if needed (optional), or increase DPI for better quality
    images = convert_from_path(pdf_path, dpi=200)  # Lower DPI = faster but still accurate
    full_text = []

    for image in images:
        image = image.convert("L")  # Grayscale improves speed & OCR accuracy
        text = pytesseract.image_to_string(image)
        full_text.append(text)

    return "\n".join(full_text)
