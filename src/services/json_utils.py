import json
import logging

def obter_titulo_do_json(caminho_json, id_livro):
    """Busca o título de um livro no arquivo JSON com base no ID."""
    try:
        # Abre o arquivo JSON
        with open(caminho_json, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Verifica se há dados de livros no JSON
        if 'hits' in data and 'hit' in data['hits']:
            livros_data = data['hits']['hit']
            # Procura o livro com o ID correspondente
            for livro in livros_data:
                if livro['id'] == id_livro:
                    return livro['fields']['title']  # Retorna o título do livro
        logging.error(f"Livro com ID {id_livro} não encontrado no arquivo JSON.")
        return None
    except Exception as e:
        logging.error(f"Erro ao buscar título no JSON: {e}")
        return None
