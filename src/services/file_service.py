# file_service.py

import os
import json
import logging
import requests
from services.shared_services import verificar_manifest_no_banco
from services.image_utils import salvar_imagens, sanitizar_titulo
from services.image_utils import obter_paginas_existentes, salvar_imagens, obter_titulo_do_json




# Função para carregar dados de um arquivo JSON
def carregar_dados_json(caminho_json):
    if os.path.exists(caminho_json):
        try:
            with open(caminho_json, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            return dados
        except json.JSONDecodeError:
            logging.error(f"Erro ao decodificar o arquivo JSON: {caminho_json}")
            return None
    else:
        logging.error(f"O arquivo JSON não foi encontrado: {caminho_json}")
        return None


def criar_pasta_e_descricao(id_livro, descricao, pasta_base, caminho_json):
    """
    Cria uma pasta para o livro baseado no título extraído do JSON e salva uma descrição.
    """
    # Buscar o título correto no JSON
    titulo_livro = obter_titulo_do_json(id_livro, caminho_json)
    
    # Sanitizar o título do livro
    titulo_sanitizado = sanitizar_titulo(titulo_livro)
    
    # Criar o caminho completo para salvar o livro
    livro_path = os.path.join(pasta_base, titulo_sanitizado)
    
    # Criar a pasta se não existir
    if not os.path.exists(livro_path):
        os.makedirs(livro_path)
        logging.info(f"Pasta {livro_path} criada com sucesso.")
    else:
        logging.info(f"Pasta {livro_path} já existe.")
    
    # Salvar a descrição em um arquivo
    caminho_arquivo_descricao = os.path.join(livro_path, 'descricao.txt')
    with open(caminho_arquivo_descricao, 'w', encoding='utf-8') as f:
        f.write(descricao)
    
    return livro_path


def processar_livro(livro, pasta_base, modo, conn, caminho_json):
    try:
        # Carregar dados do arquivo JSON
        dados_json = carregar_dados_json(caminho_json)
        if dados_json is None:
            logging.error(f"Não foi possível carregar os dados do JSON: {caminho_json}")
            return

        id_livro = str(livro['id'])
        descricao = livro.get('fields', {}).get('description', 'Sem descrição disponível')

        livro_path = criar_pasta_e_descricao(id_livro, descricao, pasta_base, caminho_json)

        if modo == "IIIF_manifest":
            if not verificar_manifest_no_banco(conn, id_livro):
                baixar_e_salvar_manifest(conn, id_livro, livro_path, caminho_json)
            else:
                logging.info(f"Manifest do livro ID {id_livro} já está no banco de dados.")
        else:
            paginas_existentes = obter_paginas_existentes(id_livro, pasta_base)
            total_paginas_esperadas = int(livro.get('fields', {}).get('images', '0'))
            salvar_imagens(id_livro, livro_path, paginas_existentes, total_paginas_esperadas)

    except Exception as e:
        logging.error(f"Erro ao processar o livro: {e}")

# Função para baixar e salvar o manifesto
def baixar_e_salvar_manifest(conn, id_livro, livro_path, caminho_json):
    """
    Baixa o manifest IIIF de um livro e salva as imagens contidas no manifest.
    """
    url_manifest = f"https://s3.amazonaws.com/iiif.slavesocieties.org/manifest/{id_livro}.json"
    
    try:
        response = requests.get(url_manifest)
        response.raise_for_status()
        manifest = response.json()
        
        if 'sequences' in manifest and len(manifest['sequences']) > 0:
            imagens = manifest['sequences'][0].get('canvases', [])
            if imagens:
                urls_imagens = [canvas['images'][0]['resource']['@id'] for canvas in imagens if 'images' in canvas and 'resource' in canvas['images'][0]]
                salvar_imagens(conn, id_livro, livro_path, urls_imagens, caminho_json)
            else:
                logging.error(f"Manifesto do livro {id_livro} não contém imagens.")
        else:
            logging.error(f"Manifesto do livro {id_livro} não contém sequências ou está vazio.")
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao baixar o manifest IIIF para o livro ID: {id_livro}: {e}")
