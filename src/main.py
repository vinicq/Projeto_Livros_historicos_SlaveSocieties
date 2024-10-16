import sys
import os

# Adiciona o diretório src ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import requests
import sqlite3
import logging
from datetime import datetime
from services.api_service import baixar_dados_apis
from services.file_service import processar_livro_especifico, processar_livros
from services.database_service import inicializar_banco_dados, verificar_todos_livros_baixados
from ai.test_ai import teste_aplicar_ocr  # Importa a função de teste de OCR
from services.file_service import baixar_imagens_via_manifest

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
    configurar_logger()
    conn = inicializar_banco_dados()

    # Baixar dados das APIs com a conexão 'conn'
    paroquia_data, forum_data, forum_mlor = baixar_dados_apis(conn)

    # Perguntar ao usuário qual conjunto de dados deseja processar
    escolha = input("Qual conjunto de dados deseja processar? 1 para Paróquia de Nossa Senhora dos Milagres, 2 para Fórum Nivaldo de Farias Brito ou 3 para Fórum Miguel Levino de Oliveira Ramos: ")

    if escolha == '1':
        pasta_base = r"livros\Paraiba\paroquia_de_nossa_senhora_dos_milagres"
        livros_data = paroquia_data
    elif escolha == '2':
        pasta_base = r"livros\Paraiba\arquivo_do_forum_nivaldo_de_farias_brito"
        livros_data = forum_data
    elif escolha == '3':
        pasta_base = r"livros\Paraiba\Mamanguape\arquivo_do_forum_miguel_levino_de_oliveira_ramos"
        livros_data = forum_mlor
        # Processo especial para Fórum Miguel Levino de Oliveira Ramos
        for livro in livros_data:
            processar_livro_especifico(livro, pasta_base, conn)
            
            # Verificar se o campo 'id' existe antes de tentar baixar as imagens
            if 'id' in livro:
                baixar_imagens_via_manifest(livro['id'], pasta_base, conn)
            else:
                logging.error(f"Livro sem campo 'id': {livro}")
    else:
        print("Escolha inválida.")
        return

    # Listar os livros e obter a escolha do usuário
    escolha_livro = obter_escolha_livro(livros_data)

    if escolha_livro.isdigit():
        escolha_livro = int(escolha_livro)

        if escolha_livro == len(livros_data) + 1:
            # Baixar todos os livros
            processar_livros(livros_data, pasta_base, conn)
        elif 1 <= escolha_livro <= len(livros_data):
            # Baixar o livro escolhido
            livro_escolhido = livros_data[escolha_livro - 1]
            processar_livro_especifico(livro_escolhido, pasta_base, conn)
        else:
            print("Escolha inválida.")
    else:
        print("Escolha inválida. Por favor, insira um número válido.")

    # Perguntar ao usuário se deseja executar a parte de IA
    escolha_ia = input("Deseja executar a parte de IA? (s/n): ")
    if escolha_ia.lower() == 's':
        teste_aplicar_ocr()  # Chama a função de teste de OCR

    verificar_todos_livros_baixados(conn)
    conn.close()

if __name__ == "__main__":
    main()
