import requests
import os
import json
import logging
from services.database_service import inserir_livros

def baixar_livros(api_url, json_filename):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data_path = os.path.join('src', 'data')
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        if response.text.strip() == "":
            logging.error(f"A resposta da API está vazia: {api_url}")
            return []

        with open(os.path.join(data_path, json_filename), 'w', encoding='utf-8') as f:
            f.write(response.text)
        logging.info(f"Dados baixados e salvos em {json_filename}")

        try:
            data = response.json()
            if 'hits' in data and 'hit' in data['hits']:
                return data['hits']['hit']
            else:
                logging.error(f"Formato inesperado no JSON {json_filename}: {data.keys()}")
                return []
        except ValueError as e:
            logging.error(f"Erro ao processar a resposta da API: {e}")
            logging.error(f"Conteúdo retornado: {response.text[:200]}")
            return []
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao acessar a API: {e}")
        return []

def baixar_dados_apis(conn):
    api_paroquia_de_nossa_senhora_dos_milagres = "https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Par%C3%B3quia%20de%20Nossa%20Senhora%20dos%20Milagres%27&q.parser=structured&size=10000"
    api_arquivo_do_forum_nivaldo_de_farias_brito = "https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Arquivo%20do%20F%C3%B3rum%20Nivaldo%20de%20Farias%20Brito%27&q.parser=structured&size=10000"
    api_arquivo_do_forum_miguel_levino_de_oliveira_ramos = "https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Arquivo%20do%20F%C3%B3rum%20Miguel%20Levino%20de%20Oliveira%20Ramos%27&q.parser=structured&size=10000"
    api_arquivo_historico_paraiba = "https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Arquivo%20Hist%C3%B3rico%20do%20Estado%20da%20Para%C3%ADba%27&q.parser=structured&size=10000"
    api_forum_judicial_joao_pessoa = "https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Arquivo%20do%20F%C3%B3rum%20Judicial%20Comarca%20de%20Jo%C3%A3o%20Pessoa%27&q.parser=structured&size=10000"
    api_memorial_tribunal_paraiba = "https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Arquivo%20do%20Memorial%20do%20Tribunal%20de%20Justi%C3%A7a%20da%20Para%C3%ADba%27&q.parser=structured&size=10000"
    api_instituto_historico_paraibano = "https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Instituto%20Hist%C3%B3rico%20e%20Geogr%C3%A1fico%20Paraibano%27&q.parser=structured&size=10000"

    paroquia_data = baixar_livros(api_paroquia_de_nossa_senhora_dos_milagres, "paroquia_de_nossa_senhora_dos_milagres.json")
    forum_data = baixar_livros(api_arquivo_do_forum_nivaldo_de_farias_brito, "arquivo_do_forum_nivaldo_de_farias_brito.json")
    forum_mlor = baixar_livros(api_arquivo_do_forum_miguel_levino_de_oliveira_ramos, "arquivo_do_forum_miguel_levino_de_oliveira_ramos.json")
    arquivo_historico_data = baixar_livros(api_arquivo_historico_paraiba, "arquivo_historico_do_estado_da_paraiba.json")
    forum_judicial_data = baixar_livros(api_forum_judicial_joao_pessoa, "arquivo_do_forum_judicial_comarca_de_joao_pessoa.json")
    memorial_tribunal_data = baixar_livros(api_memorial_tribunal_paraiba, "arquivo_do_memorial_do_tribunal_de_justica_da_paraiba.json")
    instituto_historico_data = baixar_livros(api_instituto_historico_paraibano, "instituto_historico_e_geografico_paraibano.json")

    inserir_livros(conn, paroquia_data)
    inserir_livros(conn, forum_data)
    inserir_livros(conn, forum_mlor)
    inserir_livros(conn, arquivo_historico_data or [])
    inserir_livros(conn, forum_judicial_data or [])
    inserir_livros(conn, memorial_tribunal_data or [])
    inserir_livros(conn, instituto_historico_data or [])

    return (paroquia_data, forum_data, forum_mlor, arquivo_historico_data, forum_judicial_data, memorial_tribunal_data, instituto_historico_data)

def baixar_manifest_iiif_usando_json(json_filename):
    """Função para carregar o JSON salvo e usar o ID do livro para baixar o manifest IIIF"""
    try:
        # Carrega o arquivo JSON salvo
        data_path = os.path.join('src', 'data', json_filename)
        with open(data_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        # Verifica se o JSON tem o campo 'hits' e 'hit'
        if 'hits' in json_data and 'hit' in json_data['hits']:
            livros_data = json_data['hits']['hit']
            
            # Para cada livro no JSON, pega o ID e baixa o manifest IIIF
            for livro in livros_data:
                if 'id' in livro and 'fields' in livro and 'title' in livro['fields']:
                    id_livro = livro['id']
                    titulo_livro = livro['fields']['title']  # Obtém o título do livro
                    logging.info(f"Baixando manifest IIIF para o livro '{titulo_livro}' com ID {id_livro}")
                    baixar_manifest_iiif(id_livro)
                else:
                    logging.error(f"ID ou título não encontrado no livro: {livro}")
        else:
            logging.error(f"Formato do JSON inválido em {json_filename}: Esperado uma lista.")
    except Exception as e:
        logging.error(f"Erro ao processar o JSON {json_filename}: {e}")
        return []

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
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao baixar o manifest IIIF: {e}")
        return []
