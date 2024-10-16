import os
import re
import logging
from services.database_service import atualizar_banco_dados
import requests
from unidecode import unidecode  # Importando unidecode para remover acentuações

def obter_paginas_existentes(id_livro, pasta_base):
    """Função para verificar as páginas que já foram baixadas para um livro"""
    livro_path = os.path.join(pasta_base, str(id_livro))
    paginas_existentes = []
    
    if os.path.exists(livro_path):
        paginas_existentes = [int(f.split('.')[0]) for f in os.listdir(livro_path) if f.endswith('.jpg')]
    
    return paginas_existentes

def processar_livro_especifico(livro, pasta_base, conn):
    id_livro = livro['id']
    titulo = livro['fields'].get('title', 'Título desconhecido').replace(" ", "_").replace("/", "_")
    descricao = livro['fields'].get('description', 'Sem descrição disponível')
    paginas_existentes = obter_paginas_existentes(id_livro, pasta_base)

    # Log para verificar se a função está sendo chamada
    logging.info(f"Processando livro ID {id_livro}: {titulo}")

    # Chamada para criar a pasta e descrição
    livro_path = criar_pasta_e_descricao(titulo, descricao, pasta_base, id_livro)
    if livro_path is None:
        logging.error(f"Falha ao criar a pasta para o livro ID {id_livro}.")
        return

    # Chamada para baixar as imagens
    total_paginas_esperadas = int(livro['fields'].get('images', '0'))
    baixar_imagens(id_livro, livro_path, paginas_existentes, total_paginas_esperadas, conn)

def processar_livros(livros_data, pasta_base, conn):
    """Função para processar todos os livros"""
    for livro in livros_data:
        id_livro = livro['id']
        titulo = livro['fields'].get('title', 'Título desconhecido').replace(" ", "_").replace("/", "_")
        descricao = livro['fields'].get('description', 'Sem descrição disponível')
        paginas_existentes = obter_paginas_existentes(id_livro, pasta_base)

        # Log para verificar se a função está sendo chamada
        logging.info(f"Processando livro ID {id_livro}: {titulo}")

        # Chamada para criar a pasta e descrição
        livro_path = criar_pasta_e_descricao(titulo, descricao, pasta_base, id_livro)
        if livro_path is None:
            logging.error(f"Falha ao criar a pasta para o livro ID {id_livro}.")
            continue

        # Chamada para baixar as imagens
        total_paginas_esperadas = int(livro['fields'].get('images', '0'))
        baixar_imagens(id_livro, livro_path, paginas_existentes, total_paginas_esperadas, conn)

def criar_pasta_e_descricao(titulo, descricao, pasta_base, id_livro):
    # Criar o nome da pasta sanitizado
    titulo_sanitizado = re.sub(r'[^\w\s]', '', unidecode(titulo)).replace(' ', '_')
    livro_path = os.path.join(pasta_base, titulo_sanitizado)

    # Caso a pasta já exista para o ID, reutilizar a pasta
    if os.path.exists(os.path.join(pasta_base, str(id_livro))):
        livro_path = os.path.join(pasta_base, str(id_livro))
    
    try:
        if not os.path.exists(livro_path):
            os.makedirs(livro_path)
    except Exception as e:
        print(f"Erro ao criar diretório: {e}")
        return None  # Retorna None em caso de erro
    
    try:
        with open(os.path.join(livro_path, 'descricao.txt'), 'w', encoding='utf-8') as f:
            f.write(descricao)
    except Exception as e:
        print(f"Erro ao criar arquivo: {e}")
        return None  # Retorna None em caso de erro
    
    return livro_path

def baixar_imagens(id_livro, livro_path, paginas_existentes, total_paginas_esperadas, conn):
    """Função para baixar as imagens de um livro"""
    pagina = 1
    total_paginas = len(paginas_existentes)
    total_tamanho = 0

    while total_paginas < total_paginas_esperadas:
        if pagina in paginas_existentes:
            pagina += 1
            continue
        
        url_imagem = f"https://images.slavesocieties.org/iiif/3/{id_livro}-{pagina:04d}.jpg/full/1500,2000/0/default.jpg"
        
        # Verifica se a imagem já foi baixada
        if os.path.exists(os.path.join(livro_path, f"{pagina:04d}.jpg")):
            logging.info(f"Imagem {pagina:04d}.jpg já existe. Pulando download.")
            pagina += 1
            total_paginas += 1
            continue
        
        try:
            logging.info(f"Iniciando download da página {pagina} do livro ID {id_livro}: {url_imagem}")
            response = requests.get(url_imagem)
            response.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx e 5xx
            
            tamanho = len(response.content)
            total_tamanho += tamanho
            
            with open(os.path.join(livro_path, f"{pagina:04d}.jpg"), 'wb') as f:
                f.write(response.content)
            
            logging.info(f"Download concluído da página {pagina} do livro ID {id_livro}.")
            pagina += 1
            total_paginas += 1
            
        except requests.exceptions.HTTPError as e:
            logging.error(f"Erro ao baixar a página {pagina} do livro ID {id_livro}: {e}")
            if response.status_code == 404:
                logging.warning(f"Página {pagina} não encontrada. Verificando próxima página.")
                pagina += 1  # Tenta a próxima página
            else:
                break  # Para outros erros, pode ser melhor parar

    # Atualiza o banco de dados com as páginas baixadas
    atualizar_banco_dados(conn, os.path.basename(livro_path), total_paginas, True, total_tamanho)

def baixar_imagens_via_manifest(id_livro, livro_path, conn):
    """Função para baixar as melhores imagens via manifest IIIF"""
    urls_imagens = baixar_manifest_iiif(id_livro)  # Obtém as URLs das melhores imagens
    
    if not urls_imagens:
        logging.error(f"Não foi possível obter imagens do livro ID {id_livro}.")
        return

    total_paginas = 0
    total_tamanho = 0

    for i, url_imagem in enumerate(urls_imagens):
        try:
            logging.info(f"Iniciando download da página {i+1} do livro ID {id_livro}")
            response = requests.get(url_imagem)
            response.raise_for_status()
            
            tamanho = len(response.content)
            total_tamanho += tamanho

            with open(os.path.join(livro_path, f"{i+1:04d}.jpg"), 'wb') as f:
                f.write(response.content)
            
            total_paginas += 1
            logging.info(f"Download da página {i+1} concluído para o livro ID {id_livro}.")
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao baixar a página {i+1} do livro ID {id_livro}: {e}")

    # Atualizar o banco de dados com o progresso do download
    atualizar_banco_dados(conn, os.path.basename(livro_path), total_paginas, True, total_tamanho)

def baixar_manifest_iiif(id_livro):
    """Função para baixar o manifest IIIF e retornar URLs de imagens"""
    url_manifest = f"https://s3.amazonaws.com/iiif.slavesocieties.org/manifest/{id_livro}.json"
    try:
        response = requests.get(url_manifest)
        response.raise_for_status()
        manifest = response.json()
        imagens = manifest['sequences'][0]['canvases']
        urls_imagens = [canvas['images'][0]['resource']['@id'] for canvas in imagens]
        return urls_imagens
    except Exception as e:
        logging.error(f"Erro ao baixar o manifest IIIF: {e}")
        return []
