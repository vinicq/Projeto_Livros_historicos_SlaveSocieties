import sys
import os

# Adiciona o caminho 'src' ao Python Path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import requests
import sqlite3
import logging
from datetime import datetime
from services.api_service import baixar_dados_apis
from services.database_service import inicializar_banco_dados, verificar_todos_livros_baixados
from services.file_service import processar_livro, baixar_e_salvar_manifest
from services.shared_services import verificar_manifest_no_banco

# Função para configurar o logger, que vai registrar as atividades do sistema
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


# Função para listar os livros disponíveis para o usuário escolher
def listar_livros(livros_data):
    """Lista os livros com uma numeração para escolha"""
    for i, livro in enumerate(livros_data, start=1):
        titulo = livro['fields'].get('title', 'Título desconhecido')
        print(f"{i}. {titulo}")
    print(f"{len(livros_data) + 1}. TODOS")  # Adiciona opção para baixar todos


# Função para capturar a escolha do usuário sobre qual livro processar
def obter_escolha_livro(livros_data):
    """Exibe a lista de livros e captura a escolha do usuário"""
    listar_livros(livros_data)
    escolha = input("Escolha o número do livro que deseja baixar ou escolha 'TODOS': ")
    return escolha


def criar_pasta_se_necessario(pasta_base):
    """Verifica e cria as pastas necessárias se não existirem"""
    if not os.path.exists(pasta_base):
        os.makedirs(pasta_base)
        logging.info(f"Pasta {pasta_base} criada com sucesso.")
    else:
        logging.info(f"Pasta {pasta_base} já existe.")


def main():
    configurar_logger()  # Configurar o sistema de logs
    conn = inicializar_banco_dados()  # Conectar e inicializar o banco de dados

    # Baixar os dados das APIs
    (paroquia_data, forum_data, forum_mlor, 
     arquivo_historico_data, forum_judicial_data, 
     memorial_tribunal_data, instituto_historico_data) = baixar_dados_apis(conn)

    # Perguntar ao usuário qual conjunto de dados deseja processar
    print("1 - São João do Cariri - Paróquia de Nossa Senhora dos Milagres")
    print("2 - São João do Cariri - Arquivo do Fórum Nivaldo de Farias Brito")
    print("3 - Mamanguape - Arquivo do Fórum Miguel Levino de Oliveira Ramos")
    print("4 - João Pessoa - Arquivo Histórico da Paraíba")
    print("5 - João Pessoa - Fórum Judicial de João Pessoa")
    print("6 - João Pessoa - Memorial do Tribunal de Justiça da Paraíba")
    print("7 - João Pessoa - Instituto Histórico e Geográfico Paraibano")
    
    escolha = input("Escolha o número do conjunto de dados que deseja processar: ")

    # Definir a pasta base e os dados conforme a escolha do usuário
    if escolha == '1':
        pasta_base = os.path.join("livros", "Paraiba", "Sao_Joao_do_Cariri", "Paroquia_de_Nossa_Senhora_dos_Milagres")
        livros_data = paroquia_data
    elif escolha == '2':
        pasta_base = os.path.join("livros", "Paraiba", "Sao_Joao_do_Cariri", "arquivo_do_forum_nivaldo_de_farias_brito")
        livros_data = forum_data
    elif escolha == '3':
        pasta_base = os.path.join("livros", "Paraiba", "Mamanguape", "arquivo_do_forum_miguel_levino_de_oliveira_ramos")
        livros_data = forum_mlor
    elif escolha == '4':
        pasta_base = os.path.join("livros", "Paraiba", "Joao_Pessoa", "Arquivo_Historico_Paraiba")
        livros_data = arquivo_historico_data
    elif escolha == '5':
        pasta_base = os.path.join("livros", "Paraiba", "Joao_Pessoa", "Forum_Judicial_Joao_Pessoa")
        livros_data = forum_judicial_data
    elif escolha == '6':
        pasta_base = os.path.join("livros", "Paraiba", "Joao_Pessoa", "Memorial_Tribunal_Paraiba")
        livros_data = memorial_tribunal_data
    elif escolha == '7':
        pasta_base = os.path.join("livros", "Paraiba", "Joao_Pessoa", "Instituto_Historico_Paraibano")
        livros_data = instituto_historico_data
    else:
        print("Escolha inválida.")
        return

    # Pega o caminho correto do arquivo JSON baseado na escolha do usuário
    base_dir = os.path.join('src', 'data')
    arquivos_json = {
        '1': os.path.join(base_dir, 'paroquia_de_nossa_senhora_dos_milagres.json'),
        '2': os.path.join(base_dir, 'arquivo_do_forum_nivaldo_de_farias_brito.json'),
        '3': os.path.join(base_dir, 'arquivo_do_forum_miguel_levino_de_oliveira_ramos.json'),
        '4': os.path.join(base_dir, 'arquivo_historico_do_estado_da_paraiba.json'),
        '5': os.path.join(base_dir, 'arquivo_do_forum_judicial_comarca_de_joao_pessoa.json'),
        '6': os.path.join(base_dir, 'arquivo_do_memorial_do_tribunal_de_justica_da_paraiba.json'),
        '7': os.path.join(base_dir, 'instituto_historico_e_geografico_paraibano.json')
    }

    # Obtendo o caminho correto do JSON
    caminho_json = arquivos_json.get(escolha)

    # Criar a pasta base antes de processar os livros
    criar_pasta_se_necessario(pasta_base)

    # Listar os livros e obter a escolha do usuário
    escolha_livro = obter_escolha_livro(livros_data)

    # Certifique-se de passar 'caminho_json' corretamente
    if escolha_livro.isdigit():
        escolha_livro = int(escolha_livro)
        if escolha_livro == len(livros_data) + 1:
            # Baixar todos os manifests e processar todos os livros
            for livro in reversed(livros_data):
                if verificar_manifest_no_banco(conn, livro['id']):
                    logging.info(f"Manifesto do livro {livro['fields']['title']} já existe no banco.")
                else:
                    # Adicionando 'caminho_json' na chamada
                    baixar_e_salvar_manifest(conn, livro['id'], livro.get('titulo', pasta_base), caminho_json)
                processar_livro(livro, pasta_base, "IIIF_manifest" if escolha in ['3', '5', '6'] else "sem_manifest", conn, caminho_json)
        elif 1 <= escolha_livro <= len(livros_data):
            # Processar o livro específico escolhido
            livro_escolhido = livros_data[escolha_livro - 1]
            if verificar_manifest_no_banco(conn, livro_escolhido['id']):
                logging.info(f"Manifesto do livro {livro_escolhido['fields']['title']} já existe no banco.")
            else:
                # Adicionando 'caminho_json' na chamada
                baixar_e_salvar_manifest(conn, livro_escolhido['id'], livro_escolhido.get('titulo', pasta_base), caminho_json)
            processar_livro(livro_escolhido, pasta_base, "IIIF_manifest" if escolha in ['3', '5', '6'] else "sem_manifest", conn, caminho_json)
        else:
            print("Escolha inválida.")
    else:
        print("Escolha inválida.")

    verificar_todos_livros_baixados(conn)  # Verifica se todos os livros foram baixados completamente
    conn.close()


if __name__ == "__main__":
    main()
