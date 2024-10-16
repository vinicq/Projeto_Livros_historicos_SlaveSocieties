import sys
import os

# Adiciona o diretório 'src' ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import requests
import sqlite3
import logging
from datetime import datetime
from services.api_service import baixar_dados_apis
from services.file_service import processar_livro, verificar_manifest_no_banco, baixar_e_salvar_manifest
from services.database_service import inicializar_banco_dados, verificar_todos_livros_baixados


# Função para configurar o logger, que vai registrar as atividades do sistema
def configurar_logger():
    log_path = 'logs'  # Diretório onde os logs serão salvos
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


# Função para listar os livros disponíveis para o usuário escolher
def listar_livros(livros_data):
    """Lista os livros com uma numeração para escolha"""
    for i, livro in enumerate(livros_data, start=1):
        titulo = livro['fields'].get('title', 'Título desconhecido')
        print(f"{i}. {titulo}")
    print(f"{len(livros_data) + 1}. TODOS")  # Adiciona a opção para baixar todos os livros


# Função para capturar a escolha do usuário sobre qual livro processar
def obter_escolha_livro(livros_data):
    """Exibe a lista de livros e captura a escolha do usuário"""
    listar_livros(livros_data)
    escolha = input("Escolha o número do livro que deseja baixar ou escolha 'TODOS': ")
    return escolha


def main():
    configurar_logger()  # Configurar o sistema de logs
    conn = inicializar_banco_dados()  # Conectar e inicializar o banco de dados

    # Baixar os dados das APIs, mas não processar ainda
    (paroquia_data, forum_data, forum_mlor, 
     arquivo_historico_data, forum_judicial_data, 
     memorial_tribunal_data, instituto_historico_data) = baixar_dados_apis(conn)

    # Perguntar ao usuário qual conjunto de dados deseja processar
    print("1 - Paróquia de Nossa Senhora dos Milagres")
    print("2 - Arquivo do Fórum Nivaldo de Farias Brito")
    print("3 - Arquivo do Fórum Miguel Levino de Oliveira Ramos")
    print("4 - Arquivo Histórico da Paraíba")
    print("5 - Fórum Judicial de João Pessoa")
    print("6 - Memorial do Tribunal de Justiça da Paraíba")
    print("7 - Instituto Histórico e Geográfico Paraibano")
    
    escolha = input("Escolha o número do conjunto de dados que deseja processar: ")

    # Definir a pasta base e os dados conforme a escolha do usuário
    if escolha == '1':
        pasta_base = r"livros\Paraiba\Sao_Joao_do_Cariri\Paroquia_de_Nossa_Senhora_dos_Milagres"
        livros_data = paroquia_data
    elif escolha == '2':
        pasta_base = r"livros\Paraiba\Sao_Joao_do_Cariri\arquivo_do_forum_nivaldo_de_farias_brito"
        livros_data = forum_data
    elif escolha == '3':
        pasta_base = r"livros\Paraiba\Mamanguape\arquivo_do_forum_miguel_levino_de_oliveira_ramos"
        livros_data = forum_mlor
    elif escolha == '4':
        pasta_base = r"livros\Paraiba\Joao_Pessoa\Arquivo_Historico_Paraiba"
        livros_data = arquivo_historico_data
    elif escolha == '5':
        pasta_base = r"livros\Paraiba\Joao_Pessoa\Forum_Judicial_Joao_Pessoa"
        livros_data = forum_judicial_data
    elif escolha == '6':
        pasta_base = r"livros\Paraiba\Joao_Pessoa\Memorial_Tribunal_Paraiba"
        livros_data = memorial_tribunal_data
    elif escolha == '7':
        pasta_base = r"livros\Paraiba\Joao_Pessoa\Instituto_Historico_Paraibano"
        livros_data = instituto_historico_data
    else:
        print("Escolha inválida.")
        return

    # Listar os livros e obter a escolha do usuário
    escolha_livro = obter_escolha_livro(livros_data)

    if escolha_livro.isdigit():
        escolha_livro = int(escolha_livro)
        if escolha_livro == len(livros_data) + 1:
            # Baixar todos os manifests e processar todos os livros
            for livro in livros_data:
                if verificar_manifest_no_banco(conn, livro['id']):
                    logging.info(f"Manifesto do livro {livro['fields']['title']} já existe no banco.")
                else:
                    baixar_e_salvar_manifest(conn, livro['id'])
                processar_livro(livro, pasta_base, "IIIF_manifest" if escolha in ['3', '5', '6'] else "sem_manifest", conn)
        elif 1 <= escolha_livro <= len(livros_data):
            # Processar o livro específico escolhido
            livro_escolhido = livros_data[escolha_livro - 1]
            if verificar_manifest_no_banco(conn, livro_escolhido['id']):
                logging.info(f"Manifesto do livro {livro_escolhido['fields']['title']} já existe no banco.")
            else:
                baixar_e_salvar_manifest(livro_escolhido['id'], livro_escolhido['fields']['title'], conn)
            processar_livro(livro_escolhido, pasta_base, "IIIF_manifest" if escolha in ['3', '5', '6'] else "sem_manifest", conn)
        else:
            print("Escolha inválida.")
    else:
        print("Escolha inválida.")

    verificar_todos_livros_baixados(conn)  # Verifica se todos os livros foram baixados completamente
    conn.close()



# Executa o código principal se o arquivo for rodado diretamente
if __name__ == "__main__":
    main()