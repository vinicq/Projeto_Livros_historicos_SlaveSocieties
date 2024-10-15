# Projeto de Livros Históricos

Este projeto automatiza o processo de download, verificação, armazenamento e análise de dados relacionados a livros históricos disponíveis via uma API pública. Ele utiliza **Python** para a automação, manipulação de arquivos e banco de dados, com a integração de bibliotecas específicas para facilitar o processamento das imagens e geração de relatórios.

## Tecnologias Utilizadas

- **Python** (v3.8 ou superior): Linguagem de programação utilizada para o desenvolvimento do projeto.
- **Requests**: Biblioteca para fazer requisições HTTP.
- **Pillow**: Biblioteca para manipulação de imagens.
- **SQLite3**: Banco de dados local para armazenar informações dos livros.
- **Pandas**: Para manipulação e análise de dados, incluindo a geração de arquivos Excel.
- **dotenv**: Para gerenciar variáveis de ambiente, se necessário.

## Pré-requisitos

Antes de rodar o projeto, certifique-se de que os seguintes itens estão instalados no seu sistema:

1. **Python** (v3.8 ou superior) - [Instale o Python](https://www.python.org/downloads/)
2. **Git** (para gerenciamento de código) - [Instale o Git](https://git-scm.com/)

## Configurando o Ambiente

### 1. Criar um Ambiente Virtual

Para isolar as dependências do projeto, é recomendável criar um ambiente virtual. Siga os passos abaixo:

- Abra o terminal ou o PowerShell e navegue até o diretório do seu projeto:

```bash
cd C:\Projetos\Projeto_livros_historicos
```

- Crie um novo ambiente virtual:

```bash
python -m venv .venv
```

- Ative o ambiente virtual:

  - Para Windows:
    ```bash
    .venv\Scripts\activate
    ```

  - Para macOS/Linux:
    ```bash
    source .venv/bin/activate
    ```

### 2. Instalar as Dependências

Com o ambiente virtual ativado, instale as dependências necessárias usando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Executando o Projeto

### 1. Gerando o arquivo `livros.json`

Para começar, é necessário gerar o arquivo `livros.json`, que contém os metadados dos livros:

```bash
python scripts/gerar_livros.py
```

Este script irá buscar dados da API e gerar o arquivo `livros.json` dentro do diretório `data`.

### 2. Baixando os Livros

Após gerar o arquivo `livros.json`, execute o seguinte comando para iniciar o download dos livros:

```bash
python src/index.py
```

Este script irá:
- Baixar os livros especificados no `livros.json`.
- Salvar os arquivos na pasta `livros`.
- Verificar a integridade das imagens.
- Gerar logs com informações dos arquivos baixados.

### 3. Gerando o Banco de Dados

Para organizar os dados em um banco de dados SQLite, execute:

```bash
python scripts/gerar_banco_dados.py
```

Este script irá:
- Ler os arquivos na pasta `livros`.
- Criar um banco de dados SQLite na pasta `pageObject`.
- Armazenar informações sobre cada livro, incluindo nome, quantidade de arquivos e tamanho.

### 4. Exportando para Excel

Para exportar os dados dos livros para um arquivo Excel, o script `gerar_banco_dados.py` já inclui a funcionalidade de gerar um arquivo `.xlsx` na pasta `logs`. O nome do arquivo incluirá a data de geração para facilitar a organização, por exemplo:

```
logs/livros_info_2024-10-11.xlsx
```

## Estrutura do Projeto

O projeto é organizado da seguinte forma:

```
Projeto_livros_historicos/
├── data/                   # Arquivos de dados (e.g., livros.json)
├── logs/                   # Logs e arquivos Excel gerados
├── livros/                 # Livros baixados (imagens)
├── pageObject/             # Banco de dados SQLite
├── scripts/                # Scripts utilitários
├── src/                    # Código principal do projeto
│   ├── config/             # Configuração
│   ├── services/           # Serviços de download e manipulação de arquivos
│   ├── utils/              # Utilitários
└── README.md               # Instruções do projeto
```

## Problemas Comuns e Soluções

1. **Erro ao conectar à API**

   Verifique se o `api_url` no arquivo `config.py` está correto e acessível. Se necessário, atualize para um URL alternativo.

2. **Falha ao baixar imagens**

   Se uma imagem não baixar corretamente, o script tentará novamente até o limite definido em `retry_attempts`. Verifique se há problemas de rede ou com a API.

3. **Banco de dados não gerado**

   Certifique-se de que a pasta `pageObject` existe e que o script possui permissão para gravar arquivos.

4. **Dependências faltando**

   Se o projeto reclamar de dependências não encontradas, execute `pip install -r requirements.txt` para instalar novamente todas as dependências.

## Melhorias Futuras

1. **Adição de Testes Automatizados**: Implementar testes para garantir a integridade dos scripts e a funcionalidade dos serviços.
2. **Integração com outras fontes de dados**: Possibilitar o download de livros de outras APIs.
3. **Interface Gráfica**: Criar uma interface para facilitar a interação com o projeto.

## Conclusão

Este projeto fornece uma base para automação de download, verificação e análise de dados históricos. Com as bibliotecas e serviços configurados corretamente, ele facilita o processo de coleta e organização dos dados para fins de estudo ou preservação.
