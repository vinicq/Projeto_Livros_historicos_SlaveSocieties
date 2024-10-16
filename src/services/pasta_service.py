import os
import logging
from services.database_service import conectar_banco

def listar_pastas(pasta_principal):
    """Lista as pastas na pasta principal."""
    return [d for d in os.listdir(pasta_principal) if os.path.isdir(os.path.join(pasta_principal, d))]

def listar_imagens(pasta):
    """Lista os arquivos .jpg na pasta especificada."""
    return [f for f in os.listdir(pasta) if f.endswith('.jpg')]

def main():
    pasta_principal = r'C:\Projetos\Projeto_livros_historicos\livros'  # Caminho para a pasta principal
    pastas = listar_pastas(pasta_principal)

    if not pastas:
        print("Nenhuma pasta encontrada na pasta principal.")
        return

    print("Pastas encontradas:")
    for index, pasta in enumerate(pastas):
        print(f"{index + 1} - {pasta}")

    escolha = int(input("Escolha uma pasta pelo número: ")) - 1

    if escolha < 0 or escolha >= len(pastas):
        print("Escolha inválida.")
        return

    pasta_selecionada = os.path.join(pasta_principal, pastas[escolha])
    imagens = listar_imagens(pasta_selecionada)

    if not imagens:
        print("Nenhum arquivo .jpg encontrado na pasta selecionada.")
    else:
        print("Arquivos .jpg encontrados:")
        for img in imagens:
            print(img)

    # Conectar ao banco de dados
    conn = conectar_banco('livros.db')
    if conn:
        # Aqui você pode realizar operações com o banco de dados, como associar IDs
        pass

if __name__ == "__main__":
    main()

