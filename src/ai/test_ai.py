from ai.ocr import aplicar_ocr
from ai.processar_texto import processar_texto
from InquirerPy import prompt
import os

def listar_livros(pasta):
    # Lista todos os arquivos de imagem na pasta especificada
    return [f for f in os.listdir(pasta) if f.endswith(('.jpg', '.png'))]

def teste_aplicar_ocr():
    pasta_livros = r'C:\Projetos\Projeto_livros_historicos\livros\Paraiba'  # Substitua pelo caminho da sua pasta de livros
    livros = listar_livros(pasta_livros)

    # Se não houver livros, avise o usuário
    if not livros:
        print("Nenhum livro encontrado na pasta.")
        return

    # Cria uma lista de opções para o menu
    opcoes = [{'name': livro, 'value': livro} for livro in livros]
    opcoes.append({'name': 'Todos os livros', 'value': 'todos'})

    # Pergunta ao usuário qual livro ele deseja ler
    pergunta = {
        'type': 'list',
        'name': 'livro',
        'message': 'Escolha um livro para ler:',
        'choices': opcoes
    }

    resposta = prompt([pergunta])
    livro_selecionado = resposta['livro']

    if livro_selecionado == 'todos':
        for livro in livros:
            caminho = os.path.join(pasta_livros, livro)
            try:
                texto = aplicar_ocr(caminho)
                print(f"Texto extraído de {livro}:", texto)
                processar_texto(texto)
            except Exception as e:
                print(f"Erro ao processar {livro}: {e}")
    else:
        caminho = os.path.join(pasta_livros, livro_selecionado)
        try:
            texto = aplicar_ocr(caminho)
            print("Texto extraído:", texto)
            processar_texto(texto)
        except Exception as e:
            print(f"Erro ao processar {livro_selecionado}: {e}")

# Chame a função de teste
if __name__ == "__main__":
    teste_aplicar_ocr()
