import logging
import requests
import time
import sqlite3
from services.file_service import salvar_imagens
from services.manifest_service import verificar_manifest_no_banco, baixar_e_salvar_manifest



def verificar_manifest_no_banco(conn, id_livro):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM manifests WHERE id_livro = ?", (id_livro,))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        logging.error(f"Erro ao verificar manifest no banco de dados: {e}")
        return False

def baixar_e_salvar_manifest(conn, id_livro, livro_path, max_tentativas=10, timeout=60):
    """
    Baixa o manifest IIIF de um livro e salva as imagens contidas no manifest.
    """
    # Corrigir a URL adicionando 'https://' na frente
    url_manifest = f"https://s3.amazonaws.com/iiif.slavesocieties.org/manifest/{id_livro}.json"
    
    tentativas = 0
    while tentativas < max_tentativas:
        try:
            # Tenta realizar a requisição
            response = requests.get(url_manifest, timeout=timeout)
            response.raise_for_status()  # Levanta exceções para códigos de status HTTP ruins
            manifest = response.json()

            # Verificação da estrutura esperada do manifest
            if 'sequences' in manifest and len(manifest['sequences']) > 0:
                imagens = manifest['sequences'][0].get('canvases', [])
                
                # Verifica se existem imagens e extrai as URLs
                if imagens:
                    urls_imagens = [
                        canvas['images'][0]['resource']['@id']
                        for canvas in imagens
                        if 'images' in canvas and 'resource' in canvas['images'][0]
                    ]
                    salvar_imagens(conn, id_livro, livro_path, urls_imagens)
                else:
                    logging.error(f"Manifesto do livro {id_livro} não contém imagens.")
            else:
                logging.error(f"Manifesto do livro {id_livro} não contém sequências ou está vazio.")
            break  # Se o processo foi bem-sucedido, sai do loop
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao baixar o manifest IIIF para o livro ID: {id_livro}: {e}, tentativa {tentativas+1} de {max_tentativas}")
            tentativas += 1
            time.sleep(2)  # Espera antes de tentar novamente
            if tentativas == max_tentativas:
                logging.error(f"Falha ao baixar o manifest IIIF para o livro ID: {id_livro} após {max_tentativas} tentativas.")
                raise e  # Relevanta a exceção após todas as tentativas falharem
        except (KeyError, ValueError) as json_error:
            # Tratar erros no JSON ou chaves não existentes
            logging.error(f"Erro ao processar o JSON do manifest do livro {id_livro}: {json_error}")
            break  # Não adianta tentar novamente se o erro for de estrutura de dados
        except Exception as gen_error:
            logging.error(f"Erro inesperado ao processar o manifest do livro {id_livro}: {gen_error}")
            raise gen_error  # Relevanta qualquer outro erro inesperado


