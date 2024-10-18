# image_utils.py

import os
import json
import re
import logging
from unidecode import unidecode
import requests
from services.utils import obter_titulo_do_json
# Função para sanitizar o título
def sanitizar_titulo(titulo):
    if titulo:
        return unidecode(re.sub(r'[\\/*?:"<>|]', "", titulo.replace(" ", "_").lower()))
    else:
        logging.warning("Título não encontrado ou inválido.")
        return "titulo_desconhecido"

# Função para obter páginas existentes
def obter_paginas_existentes(id_livro, pasta_base):
    caminho_livro = os.path.join(pasta_base, id_livro)
    if not os.path.exists(caminho_livro):
        return []
    
    arquivos_existentes = os.listdir(caminho_livro)
    paginas = [int(re.search(r'(\d+)', arquivo).group(0)) for arquivo in arquivos_existentes if re.search(r'(\d+)', arquivo)]
    return sorted(paginas)


def salvar_imagens(conn, id_livro, pasta, urls_imagens, caminho_json):
    """Função para salvar imagens em uma pasta."""
    from services.shared_services import obter_titulo_do_json  # Importe dentro da função

    titulo_livro = obter_titulo_do_json(caminho_json, id_livro)

    if not titulo_livro:
        logging.error(f"Não foi possível obter o título para o livro com ID {id_livro}.")
        return
    
    titulo_sanitizado = sanitizar_titulo(titulo_livro)
    caminho_pasta = os.path.join(pasta, titulo_sanitizado)
    
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)
    
    for i, url_imagem in enumerate(urls_imagens):
        try:
            nome_imagem_completo = url_imagem.split('/')[-5]
            nome_imagem = nome_imagem_completo.split('-')[-1]
            imagem_path = os.path.join(caminho_pasta, nome_imagem)

            # Baixar a imagem
            response = requests.get(url_imagem)
            response.raise_for_status()

            # Salvar a imagem no caminho especificado
            with open(imagem_path, 'wb') as f:
                f.write(response.content)
            
            logging.info(f"Salvando imagem {i+1} de {len(urls_imagens)}: {url_imagem}")
        except Exception as e:
            logging.error(f"Erro ao salvar imagem {i+1} para o livro {id_livro}: {e}")
