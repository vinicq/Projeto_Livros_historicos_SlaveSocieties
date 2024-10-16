import pytesseract
from PIL import Image

# Defina o caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Altere conforme necessário

def aplicar_ocr(caminho_imagem):
    imagem = Image.open(caminho_imagem)
    texto = pytesseract.image_to_string(imagem)
    return texto

