import requests
import os
import json
import logging
from services.database_service import inserir_livros

def baixar_dados_apis(conn):
    api_paroquia_de_nossa_senhora_dos_milagres = "https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Par%C3%B3quia%20de%20Nossa%20Senhora%20dos%20Milagres%27&q.parser=structured&size=10000"
    api_arquivo_do_forum_nivaldo_de_farias_brito = "https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Arquivo%20do%20F%C3%B3rum%20Nivaldo%20de%20Farias%20Brito%27&q.parser=structured&size=10000"
    api_arquivo_do_forum_miguel_levino_de_oliveira_ramos = "https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Arquivo%20do%20F%C3%B3rum%20Miguel%20Levino%20de%20Oliveira%20Ramos%27&q.parser=structured&size=10000"

    # Baixar dados das APIs e salvar localmente
    paroquia_data = baixar_livros(api_paroquia_de_nossa_senhora_dos_milagres, "paroquia_de_nossa_senhora_dos_milagres.json")
    forum_data = baixar_livros(api_arquivo_do_forum_nivaldo_de_farias_brito, "arquivo_do_forum_nivaldo_de_farias_brito.json")
    forum_mlor = baixar_livros(api_arquivo_do_forum_miguel_levino_de_oliveira_ramos, "arquivo_do_forum_miguel_levino_de_oliveira_ramos.json")

    # Inserindo dados no banco de dados
    inserir_livros(conn, paroquia_data)
    inserir_livros(conn, forum_data)
    inserir_livros(conn, forum_mlor)

    return paroquia_data, forum_data, forum_mlor

def baixar_livros(api_url, json_filename):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data_path = os.path.join('src', 'data')
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        # Aqui especificamos o encoding como 'utf-8'
        with open(os.path.join(data_path, json_filename), 'w', encoding='utf-8') as f:
            f.write(response.text)
        logging.info(f"Dados baixados e salvos em {json_filename}")
        return json.loads(response.text)['hits']['hit']
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao acessar a API: {e}")
        return []
    
def baixar_manifest_iiif(id_iiif):
    """Baixa o arquivo IIIF manifest e retorna as URLs das melhores imagens"""
    url_manifest = f"https://s3.amazonaws.com/iiif.slavesocieties.org/manifest/{id_iiif}.json"
    
    try:
        response = requests.get(url_manifest)
        response.raise_for_status()
        manifest = response.json()
        
        imagens = manifest['sequences'][0]['canvases']
        urls_imagens = [canvas['images'][0]['resource']['@id'] for canvas in imagens]  # URLs das imagens em alta resolução
        
        return urls_imagens
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao baixar o manifest IIIF {id_iiif}: {e}")
        return []

