import sys
import os

# Adiciona o diretório src ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import requests
import sqlite3
import logging
from datetime import datetime
from services.api_service import baixar_dados_apis
from services.file_service import processar_livro
from services.database_service import inicializar_banco_dados
from ai.test_ai import teste_aplicar_ocr  # Importa a função de teste de OCR
from services.file_service import processar_livro, verificar_manifest_no_banco, baixar_e_salvar_manifest
from services.file_service import processar_livro, processar_livros


def configurar_logger():
    log_path = 'logs'
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_filename = os.path.join(log_path, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    logging.basicConfig(
        filename=log_filename,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

def listar_livros(livros_data):
    """Lista os livros com uma numeração para escolha"""
    for i, livro in enumerate(livros_data, start=1):
        titulo = livro['fields'].get('title', 'Título desconhecido')
        print(f"{i}. {titulo}")
    print(f"{len(livros_data) + 1}. TODOS")  # Adiciona opção para baixar todos

def obter_escolha_livro(livros_data):
    """Exibe a lista de livros e captura a escolha do usuário"""
    listar_livros(livros_data)
    escolha = input("Escolha o número do livro que deseja baixar ou escolha 'TODOS': ")
    return escolha

def main():
    conn = inicializar_banco_dados()
    configurar_logger()

    # Baixar dados das 7 APIs
    (paroquia_data, forum_data, forum_mlor, 
    arquivo_historico_data, forum_judicial_data, 
    memorial_tribunal_data, instituto_historico_data) = baixar_dados_apis(conn)

    # Processar Paróquia de Nossa Senhora dos Milagres
    pasta_base = r"livros\Paraiba\Sao_Joao_do_Cariri\Paroquia de Nossa Senhora dos Milagres"
    for livro in paroquia_data:
        processar_livro(livro, pasta_base, "sem_manifest", conn)

    # Processar Arquivo do Fórum Nivaldo de Farias Brito
    pasta_base = r"livros\Paraiba\Sao_Joao_do_Cariri\arquivo_do_forum_nivaldo_de_farias_brito"
    for livro in forum_data:
        processar_livro(livro, pasta_base, "sem_manifest", conn)

    # Processar Arquivo do Fórum Miguel Levino de Oliveira Ramos
    pasta_base = r"livros\Paraiba\Mamanguape"
    for livro in forum_mlor:
        processar_livro(livro, pasta_base, "IIIF_manifest", conn)

    # Processar Arquivo Histórico da Paraíba
    pasta_base = r"livros\Paraiba\João Pessoa\Arquivo Historico Paraiba"
    for livro in arquivo_historico_data:
        processar_livro(livro, pasta_base, "sem_manifest", conn)

    # Processar Fórum Judicial de João Pessoa
    pasta_base = r"livros\Paraiba\João Pessoa\Forum Judicial Joao Pessoa"
    for livro in forum_judicial_data:
        processar_livro(livro, pasta_base, "IIIF_manifest", conn)

    # Processar Memorial do Tribunal de Justiça da Paraíba
    pasta_base = r"livros\Paraiba\João Pessoa\Memorial Tribunal Paraiba"
    for livro in memorial_tribunal_data:
        processar_livro(livro, pasta_base, "IIIF_manifest", conn)

    # Processar Instituto Histórico e Geográfico Paraibano
    pasta_base = r"livros\Paraiba\João Pessoa\Instituto Historico Paraibano"
    for livro in instituto_historico_data:
        processar_livro(livro, pasta_base, "sem_manifest", conn)

    conn.close()

if __name__ == "__main__":
    main()