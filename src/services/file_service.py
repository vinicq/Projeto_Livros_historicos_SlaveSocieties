import os
import re
import logging
import time
import requests
import json
import sqlite3
import traceback
from services.database_service import atualizar_banco_dados, verificar_manifest_no_banco, inserir_manifest
from unidecode import unidecode

# Função para verificar quais páginas já foram baixadas para um livro
def obter_paginas_existentes(id_livro, pasta_base):
    livro_path = os.path.join(pasta_base, str(id_livro))
    paginas_existentes = []
    
    if os.path.exists(livro_path):
        paginas_existentes = [int(f.split('.')[0]) for f in os.listdir(livro_path) if f.endswith('.jpg')]
    
    return paginas_existentes

# Função principal para processar o livro, baseada no modo (com manifest ou sem)
def processar_livro(livro, pasta_base, modo, conn):
    id_livro = livro['id']
    titulo = livro['fields'].get('title', 'Título desconhecido').replace(" ", "_").replace("/", "_")
    descricao = livro['fields'].get('description', 'Sem descrição disponível')

    # Criar a pasta e salvar a descrição do livro
    livro_path = criar_pasta_e_descricao(titulo, descricao, pasta_base, id_livro)

    # Escolher o modo de download (com manifest IIIF ou download direto)
    if modo == "IIIF_manifest":
        baixar_imagens_via_manifest(id_livro, livro_path, conn)
    else:
        paginas_existentes = obter_paginas_existentes(id_livro, pasta_base)
        total_paginas_esperadas = int(livro['fields'].get('images', '0'))
        baixar_imagens(id_livro, livro_path, paginas_existentes, total_paginas_esperadas)

# Lista de tuplas com títulos e caminhos
mapa_pastas_lista = [
    ("Paroquia de Nossa Senhora dos Milagres", "livros/Paraiba/Sao_Joao_do_Cariri/Paroquia_de_Nossa_Senhora_dos_Milagres"),
    ("Arquivo do Fórum Nivaldo de Farias Brito", "livros/Paraiba/Sao_Joao_do_Cariri/arquivo_do_forum_nivaldo_de_farias_brito"),
    ("Mamanguape", "livros/Paraiba/Mamanguape"),
    ("Arquivo Histórico da Paraíba", "livros/Paraiba/Joao_Pessoa/Arquivo_Historico_Paraiba"),
    ("Fórum Judicial de João Pessoa", "livros/Paraiba/Joao_Pessoa/Forum_Judicial_Joao_Pessoa"),
    ("Memorial do Tribunal de Justiça da Paraíba", "livros/Paraiba/Joao_Pessoa/Memorial_Tribunal_Paraiba"),
    ("Instituto Histórico e Geográfico Paraibano", "livros/Paraiba/Joao_Pessoa/Instituto_Historico_Paraibano"),
]

# Função para criar a pasta do livro e salvar a descrição
def criar_pasta_e_descricao(titulo, descricao, pasta_base, id_livro):
    # Sanitizar o título do livro
    titulo_sanitizado = sanitizar_titulo(titulo)

    # Log para verificar a sanitização do título
    logging.info(f"Título sanitizado: '{titulo_sanitizado}'")

    # Tenta encontrar o caminho correspondente no mapa de pastas
    livro_path = encontrar_pasta_correspondente(titulo_sanitizado)

    # Se não encontrou, gera um erro (pode alterar para outro comportamento)
    if livro_path is None:
        mensagem_erro = f"Título '{titulo_sanitizado}' não encontrado no mapeamento. Usando caminho genérico."
        logging.warning(mensagem_erro)
        livro_path = os.path.join(pasta_base, 'Outros')

    # Garante que o caminho seja concatenado com o diretório base
    livro_path = os.path.join(pasta_base, livro_path, titulo_sanitizado)
    logging.info(f"Usando caminho: {livro_path}")

    # Cria a pasta se não existir
    if not os.path.exists(livro_path):
        os.makedirs(livro_path)
        logging.info(f"Pasta criada para o livro {titulo_sanitizado} (ID: {id_livro})")

    # Salva a descrição do livro em um arquivo texto
    caminho_arquivo_descricao = os.path.join(livro_path, 'descricao.txt')
    with open(caminho_arquivo_descricao, 'w', encoding='utf-8') as f:
        f.write(descricao)
        logging.info(f"Descrição salva em {caminho_arquivo_descricao}")

    return livro_path

# Função para sanitizar o título
def sanitizar_titulo(titulo):
    return unidecode(re.sub(r'[\\/*?:"<>|]', "", titulo.replace(" ", "_")))

# Função para encontrar a pasta correspondente no mapa
def encontrar_pasta_correspondente(titulo_sanitizado):
    for titulo_map, path in mapa_pastas_lista:
        if titulo_sanitizado == unidecode(titulo_map).replace(" ", "_"):
            return path
    return None


# Função com retry para downloads
def baixar_com_retry(url, max_retries=3, wait_seconds=5):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            retries += 1
            logging.error(f"Erro ao baixar {url}, tentativa {retries}/{max_retries}: {e}")
            time.sleep(wait_seconds)
    return None  # Se falhar todas as tentativas

# Função para baixar imagens diretamente (sem manifest IIIF)
def baixar_imagens(id_livro, livro_path, paginas_existentes, total_paginas_esperadas):
    pagina = 1
    total_paginas = len(paginas_existentes)
    
    while total_paginas < total_paginas_esperadas:
        url_imagem = f"https://images.slavesocieties.org/iiif/3/{id_livro}-{pagina:04d}.jpg/full/1500,2000/0/default.jpg"
        if pagina in paginas_existentes:
            pagina += 1
            continue
        
        response = baixar_com_retry(url_imagem)
        if response:
            caminho_pagina = os.path.join(livro_path, f"{pagina:04d}.jpg")
            
            # Verificar se a página já existe antes de salvar
            if not os.path.exists(caminho_pagina):
                with open(caminho_pagina, 'wb') as f:
                    f.write(response.content)
                logging.info(f"Baixada página {pagina} do livro {id_livro}")
                total_paginas += 1
            pagina += 1
        else:
            logging.error(f"Erro ao baixar a página {pagina}, todas as tentativas falharam.")
            break

# Função para baixar imagens via manifest IIIF
def baixar_imagens_via_manifest(id_livro, livro_path, conn):
    urls_imagens = baixar_e_salvar_manifest(conn, id_livro)  # Obtém as URLs das imagens do banco ou faz o download

    if not urls_imagens:
        logging.error(f"Não foi possível obter imagens do livro ID {id_livro}.")
        return

    total_paginas = 0
    total_tamanho = 0

    for i, url_imagem in enumerate(urls_imagens):
        response = baixar_com_retry(url_imagem)
        if response:
            tamanho = len(response.content)
            total_tamanho += tamanho

            caminho_pagina = os.path.join(livro_path, f"{i+1:04d}.jpg")
            
            # Verificar se a página já existe antes de salvar
            if not os.path.exists(caminho_pagina):
                with open(caminho_pagina, 'wb') as f:
                    f.write(response.content)
                logging.info(f"Download da página {i+1} concluído para o livro ID {id_livro}.")
                total_paginas += 1
        else:
            logging.error(f"Erro ao baixar a página {i+1}, todas as tentativas falharam.")
            break

    # Atualizar o banco de dados com o progresso do download
    atualizar_banco_dados(conn, os.path.basename(livro_path), total_paginas, True, total_tamanho)

# Função para baixar e salvar manifest IIIF
def baixar_e_salvar_manifest(conn, id_livro, retries=3, delay=5):
    url_manifest = f"https://s3.amazonaws.com/iiif.slavesocieties.org/manifest/{id_livro}.json"
    
    for tentativa in range(retries):
        try:
            response = requests.get(url_manifest)
            response.raise_for_status()
            manifest = response.json()
            
            imagens = manifest['sequences'][0]['canvases']
            urls_imagens = [canvas['images'][0]['resource']['@id'] for canvas in imagens]

            pasta_livro = os.path.join('livros', manifest['label'].replace(" ", "_"))
            if not os.path.exists(pasta_livro):
                os.makedirs(pasta_livro)

            for idx, url_imagem in enumerate(urls_imagens, start=1):
                nome_arquivo = f"{str(idx).zfill(4)}.jpg"
                caminho_arquivo = os.path.join(pasta_livro, nome_arquivo)
                
                img_response = requests.get(url_imagem)
                with open(caminho_arquivo, 'wb') as img_file:
                    img_file.write(img_response.content)
                
                logging.info(f"Baixada página {idx} do livro {id_livro} ({manifest['label']})")

            cursor = conn.cursor()
            for url in urls_imagens:
                cursor.execute(
                    "INSERT INTO manifests (id_livro, url_imagem) VALUES (?, ?)",
                    (id_livro, url)
                )
            conn.commit()
            logging.info(f"Manifest do livro ID {id_livro} ({manifest['label']}) baixado e salvo no banco de dados.")

            caminho_json = os.path.join(pasta_livro, 'manifest.json')
            with open(caminho_json, 'w', encoding='utf-8') as json_file:
                json.dump(manifest, json_file, ensure_ascii=False, indent=4)
            logging.info(f"Manifest IIIF do livro ID {id_livro} ({manifest['label']}) salvo em {caminho_json}.")

            return urls_imagens
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao baixar o manifest IIIF: {e}. Tentativa {tentativa+1}/{retries}")
            if tentativa < retries - 1:
                time.sleep(delay)
            else:
                logging.error(f"Falha ao baixar o manifest IIIF após {retries} tentativas.")
                logging.error(traceback.format_exc())
                return None
        
        except sqlite3.IntegrityError as e:
            logging.error(f"Erro de integridade ao inserir no banco de dados: {e}")
            logging.error(traceback.format_exc())
            conn.rollback()
            return None
        
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
            logging.error(traceback.format_exc())
            return None
