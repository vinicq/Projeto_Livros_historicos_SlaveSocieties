import requests
import os
import json
import logging
from services.database_service import inserir_livros

def baixar_dados_apis(conn):
    api_paroquia_de_nossa_senhora_dos_milagres = "https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Par%C3%B3quia%20de%20Nossa%20Senhora%20dos%20Milagres%27&q.parser=structured&size=10000"
    api_arquivo_do_forum_nivaldo_de_farias_brito = "https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Arquivo%20do%20F%C3%B3rum%20Nivaldo%20de%20Farias%20Brito%27&q.parser=structured&size=10000"

    paroquia_data = baixar_livros(api_paroquia_de_nossa_senhora_dos_milagres, "paroquia_de_nossa_senhora_dos_milagres.json")
    forum_data = baixar_livros(api_arquivo_do_forum_nivaldo_de_farias_brito, "arquivo_do_forum_nivaldo_de_farias_brito.json")

    # Inserindo dados no banco de dados
    inserir_livros(conn, paroquia_data)
    inserir_livros(conn, forum_data)

    return paroquia_data, forum_data

def baixar_livros(api_url, json_filename):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data_path = os.path.join('src', 'data')
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        with open(os.path.join(data_path, json_filename), 'w') as f:
            f.write(response.text)
        logging.info(f"Dados baixados e salvos em {json_filename}")
        return json.loads(response.text)['hits']['hit']
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao acessar a API: {e}")
        return []