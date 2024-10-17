import sqlite3
import logging
import requests
import time
from services.image_utils import salvar_imagens
from services.utils import obter_titulo_do_json

def verificar_manifest_no_banco(conn, id_livro):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM manifests WHERE id_livro = ?", (id_livro,))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        logging.error(f"Erro ao verificar manifest no banco de dados: {e}")
        return False



