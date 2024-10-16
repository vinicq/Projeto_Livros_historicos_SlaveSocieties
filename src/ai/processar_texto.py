import nltk  # Certifique-se de instalar a biblioteca nltk
from nltk.tokenize import word_tokenize

def processar_texto(texto):
    # Tokenização do texto
    palavras = word_tokenize(texto)
    print(f"Número de palavras: {len(palavras)}")
    
    # Aqui você pode adicionar mais lógica de processamento, como análise de sentimentos, etc.
    print(texto)  # Para fins de depuração


