# Historical Books Project SlaveSocieties

## Table of Contents

1. [English](#1-english)
    - [Description](#description)
    - [Project Structure](#project-structure)
    - [Libraries and Dependencies](#libraries-and-dependencies)
    - [Installation] (#installation)
    - [How to Run the Project](#how-to-run-the-project)
    - [Logs](#logs)
    - [Detailed File Descriptions](#detailed-file-descriptions)
    - [Contributions](#contributions)
2. [Portuguese](#2-portuguese)
    - [Descrição](#descrição)
    - [Estrutura do Projeto](#estrutura-do-projeto)
    - [Bibliotecas e Dependências](#bibliotecas-e-dependências)
    - [Instalação] (#instalação)
    - [Como Executar o Projeto](#como-executar-o-projeto)
    - [Logs] (#logs-portuguese)
    - [Descrição Detalhada dos Arquivos](#descrição-detalhada-dos-arquivos)
    - [Contribuições](#contribuições)

---

# 1. English

## Description

The **Historical Books Project** is an application developed for extracting, processing, and storing information from digitized historical documents. These documents include court records, inventories, criminal processes, among others. The goal is to facilitate the analysis of the extracted data, storing them in a database for future queries. The project also enables the training of machine learning models to classify and analyze the data.

## Project Structure

The project is organized as follows:

```
historical_books_project/
├── .venv/                        # Virtual environment
├── books/                        # Folder storing images of historical documents
├── logs/                         # Logs generated during execution
├── src/
│   ├── ai/
│   │   ├── model.py              # Training of machine learning models
│   │   ├── ocr.py                # Function to apply OCR (text extraction from images)
│   │   ├── process_text.py       # Processing and tokenizing the extracted text
│   │   └── test_ai.py            # Script for testing OCR and text processing functions
│   ├── data/                     # JSON data extracted from the documents
│   ├── services/
│   │   ├── api_service.py        # Service to download and process data from historical APIs
│   │   ├── database_service.py   # Database service (insert and query data)
│   │   └── file_service.py       # File and directory manipulation
└── main.py                       # Main execution script
├── books.db                      # SQLite database
├── README.md                     # Project documentation
└── requirements.txt              # Project dependencies
```

## Libraries and Dependencies

To ensure the project works correctly, the following libraries must be installed:

- **Pillow (PIL)**: For image manipulation and loading.
- **pytesseract**: To apply OCR (Optical Character Recognition) on images.
- **NLTK**: For natural language processing, such as tokenizing words.
- **Scikit-learn**: To train machine learning models.
- **InquirerPy**: To create interactive command-line interfaces.
- **SQLite3**: To manage the database where historical data is stored.

The dependencies are listed in the `requirements.txt` file. Here is its content:

```
Pillow==9.2.0
pytesseract==0.3.10
nltk==3.6.7
scikit-learn==1.0.2
InquirerPy==0.3.4
```

### Installing Tesseract OCR

In addition to the Python libraries, you will need to install **Tesseract OCR** on your system:

- **Windows**: Download and install Tesseract [here](https://github.com/tesseract-ocr/tesseract).
- **Linux**: Install it using the package manager:
  ```bash
  sudo apt-get install tesseract-ocr
  ```
- **macOS**: Install it using Homebrew:
  ```bash
  brew install tesseract
  ```

## Project Installation

### Prerequisites

- **Python 3.8+** must be installed.
- **Tesseract OCR** must be installed (instructions above).

### How to Install the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/historical_books_project.git
   cd historical_books_project
   ```

2. Create and activate a virtual environment:
   - **Linux/macOS**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows**:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. Install the libraries and dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the path to **Tesseract OCR** in the `src/ai/ocr.py` file:
   - Modify the line:
     ```python
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
     ```
   - Replace it with the correct path on your system.

5. **(Optional)**: To deactivate the virtual environment when finished:
   ```bash
   deactivate
   ```

## How to Run the Project

### Running the Main Script

To run the project, execute the `main.py` file located in the root of the project:
```bash
python main.py
```

This main script orchestrates the entire process of downloading, processing, and storing historical data.

### Running OCR and Text Processing

To test text extraction via OCR, you can run the `test_ai.py` script:
```bash
python src/ai/test_ai.py
```

This command allows you to select a historical document image, apply OCR, and process the extracted text.

## Logs

Execution logs are stored in the `logs/` folder and can be used to check the progress of the process or investigate any errors that may occur.

## Detailed File Descriptions

### 1. `main.py`

This is the **main execution** file for the project. It orchestrates all functions and services, including:

- Initializing the database.
- Setting up the logging system to monitor the process.
- Calling functions that integrate with historical APIs, download the data, process it, and store it.
- Organizing and structuring the downloaded data in local directories and in the SQLite database.

### 2. `src/ai/ocr.py`

This file contains functions that use the **Tesseract OCR** library to extract text from images. OCR is applied to scanned images of historical documents.

- **Main function**:
  - `apply_ocr(image_path)`: Opens an image and applies OCR to extract text, returning the extracted content.

### 3. `src/ai/process_text.py`

This file contains functions for text processing using the **NLTK** library. It tokenizes the text (splitting it into words), which facilitates further analysis.

- **Main function**:
  - `process_text(text)`: Tokenizes the extracted text and displays the content for debugging and analysis.

### 4. `src/ai/model.py`

This file contains functions to train machine learning models using the **scikit-learn** library. The models can be used to recognize patterns in the extracted texts.

- **Main function**:
  - `train_model(data)`: Trains a **Random Forest** classifier based on the provided data and displays the model accuracy.

### 5. `src/ai/test_ai.py`

This file is used to test the OCR and text processing functions. It allows the user to select image files and apply OCR, processing the extracted text.

- **Main functions**:
  - `list_books(folder)`: Lists image files in a specific folder.
  - `test_apply_ocr()`: Allows the user to choose a book (image), apply OCR, and process the extracted text.

### 6. `src/services/api_service.py`

This file contains functions to download historical data from APIs and store it locally and in the database.

- **Main function**:
  - `download_api_data()`: Makes calls to historical APIs, downloading data for processing.

### 7. `src/services/database_service.py`

This file handles the connection to the SQLite database and contains functions to insert and query data.

- **Main functions**:
  - `initialize_database()`: Creates the database structure and initializes the connection.
  - `insert_books(data)`: Inserts the processed data into the database.

### 8. `src/services/file_service.py`

This file contains functions for file and directory manipulation.

- **Main functions**:
  - `process_book()`: Processes the books and organizes files into specific folders.
  - `download_images()`: Downloads the images associated with the books.

## Contributions

Contributions are welcome! Follow these steps to contribute:

1. **Fork** the repository.
2. Create a **branch** for your feature or fix:
   ```bash
   git checkout -b my-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add new feature'
   ```
4. Push the changes to the remote repository:
   ```bash
   git push origin my-feature
   ```
5. Open a **pull request** describing your changes.

---

# 2. Portuguese

## Descrição

O **Projeto Livros Históricos**

 é uma aplicação desenvolvida para a extração, processamento e armazenamento de informações contidas em documentos históricos digitalizados. Esses documentos incluem arquivos de fóruns judiciais, inventários, processos criminais, entre outros. O objetivo é facilitar a análise dos dados extraídos, armazenando-os em um banco de dados para consultas futuras. O projeto também permite o treinamento de modelos de aprendizado de máquina para classificar e analisar os dados.

## Estrutura do Projeto

A estrutura do projeto está organizada da seguinte forma:

```
Projeto_livros_historicos/
├── .venv/                        # Ambiente virtual
├── livros/                       # Pasta que armazena as imagens dos documentos históricos
├── logs/                         # Logs gerados durante a execução
├── src/
│   ├── ai/
│   │   ├── modelo.py             # Treinamento de modelos de aprendizado de máquina
│   │   ├── ocr.py                # Função para aplicar OCR (extração de texto de imagens)
│   │   ├── processar_texto.py    # Processamento e tokenização do texto extraído
│   │   └── test_ai.py            # Script para testar as funções de OCR e processamento de texto
│   ├── data/                     # Dados JSON extraídos dos documentos
│   ├── services/
│   │   ├── api_service.py        # Serviço para baixar e processar dados de APIs históricas
│   │   ├── database_service.py   # Serviço de banco de dados (inserir e consultar dados)
│   │   └── file_service.py       # Manipulação de arquivos e diretórios
└── main.py                       # Script principal de execução
├── livros.db                     # Banco de dados SQLite
├── README.md                     # Documentação do projeto
└── requirements.txt              # Dependências do projeto
```

## Bibliotecas e Dependências

Para garantir o correto funcionamento do projeto, é necessário instalar as seguintes bibliotecas:

- **Pillow (PIL)**: Para manipulação e abertura de imagens.
- **pytesseract**: Para aplicar OCR (Reconhecimento Óptico de Caracteres) nas imagens.
- **NLTK**: Para processamento de linguagem natural, como tokenização de palavras.
- **Scikit-learn**: Para treinar modelos de aprendizado de máquina.
- **InquirerPy**: Para criar interfaces interativas em linha de comando.
- **SQLite3**: Para gerenciar o banco de dados onde os dados históricos serão armazenados.

As dependências estão listadas no arquivo `requirements.txt`. Aqui está o conteúdo do arquivo:

```
Pillow==9.2.0
pytesseract==0.3.10
nltk==3.6.7
scikit-learn==1.0.2
InquirerPy==0.3.4
```

### Instalando Tesseract OCR

Além das bibliotecas Python, você precisará instalar o **Tesseract OCR** no seu sistema:

- **Windows**: Baixe e instale o Tesseract [aqui](https://github.com/tesseract-ocr/tesseract).
- **Linux**: Instale usando o gerenciador de pacotes:
  ```bash
  sudo apt-get install tesseract-ocr
  ```
- **macOS**: Instale usando Homebrew:
  ```bash
  brew install tesseract
  ```

## Instalação do Projeto

### Pré-requisitos

- **Python 3.8+** precisa estar instalado.
- **Tesseract OCR** deve estar instalado (instruções acima).

### Como instalar o projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/projeto_livros_historicos.git
   cd projeto_livros_historicos
   ```

2. Crie e ative um ambiente virtual:
   - **Linux/macOS**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows**:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. Instale as bibliotecas e dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o caminho do **Tesseract OCR** no arquivo `src/ai/ocr.py`:
   - Altere a linha:
     ```python
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
     ```
   - Substitua pelo caminho correto no seu sistema.

5. **(Opcional)**: Para desativar o ambiente virtual quando terminar:
   ```bash
   deactivate
   ```

## Como Executar o Projeto

### Executando o Script Principal

Para rodar o projeto, execute o arquivo `main.py` localizado na raiz do projeto:
```bash
python main.py
```

Esse script principal orquestra todo o processo de download, processamento e armazenamento dos dados históricos.

### Executando o OCR e Processamento de Texto

Para testar a extração de texto via OCR, você pode executar o script `test_ai.py`:
```bash
python src/ai/test_ai.py
```

Este comando permite selecionar uma imagem de documento histórico para aplicar o OCR e processar o texto extraído.

## Logs

Os logs da execução são armazenados na pasta `logs/` e podem ser utilizados para verificar o andamento do processo ou investigar possíveis erros.

## Descrição Detalhada dos Arquivos

### 1. `main.py`

Este é o **arquivo principal** de execução do projeto. Ele orquestra todas as funções e serviços do projeto, incluindo:

- Inicializar o banco de dados.
- Configurar o sistema de logging para monitorar o processo.
- Chamar funções que integram com as APIs históricas, baixar os dados, processá-los e armazená-los.
- Organizar e estruturar os dados baixados em diretórios locais e no banco de dados SQLite.

### 2. `src/ai/ocr.py`

Este arquivo contém funções que utilizam a biblioteca **Tesseract OCR** para extrair texto de imagens. O OCR é aplicado em imagens digitalizadas de documentos históricos.

- **Função principal**:
  - `aplicar_ocr(caminho_imagem)`: Abre uma imagem e aplica OCR para extrair o texto, retornando o conteúdo textual.

### 3. `src/ai/processar_texto.py`

Este arquivo contém funções para o processamento de texto utilizando a biblioteca **NLTK**. Ele realiza a tokenização do texto (separação em palavras), o que facilita a análise subsequente.

- **Função principal**:
  - `processar_texto(texto)`: Realiza a tokenização do texto extraído e exibe o conteúdo para depuração e análise.

### 4. `src/ai/modelo.py`

Este arquivo contém funções para o treinamento de modelos de aprendizado de máquina utilizando a biblioteca **scikit-learn**. Os modelos podem ser usados para reconhecer padrões nos textos extraídos.

- **Função principal**:
  - `treinar_modelo(dados)`: Treina um classificador de **Random Forest** com base nos dados fornecidos, e exibe a precisão do modelo.

### 5. `src/ai/test_ai.py`

Este arquivo é utilizado para testar as funções de OCR e processamento de texto. Ele permite ao usuário selecionar arquivos de imagem e aplicar o OCR, processando o texto extraído.

- **Funções principais**:
  - `listar_livros(pasta)`: Lista arquivos de imagem em uma pasta específica.
  - `teste_aplicar_ocr()`: Permite ao usuário escolher um livro (imagem), aplicar OCR, e processar o texto extraído.

### 6. `src/services/api_service.py`

Este arquivo contém funções para baixar dados históricos de APIs e armazená-los localmente e no banco de dados.

- **Função principal**:
  - `baixar_dados_apis()`: Realiza chamadas para APIs históricas, baixando dados para processamento.

### 7. `src/services/database_service.py`

Este arquivo lida com a conexão ao banco de dados SQLite e contém funções para inserir e consultar dados.

- **Função principal**:
  - `inicializar_banco_dados()`: Cria a estrutura do banco de dados e inicializa a conexão.
  - `inserir_livros(dados)`: Insere os dados processados no banco de dados.

### 8. `src/services/file_service.py`

Este arquivo contém funções para manipular arquivos e diretórios.

- **Função principal**:
  - `processar_livro()`: Processa os livros e organiza os arquivos em pastas específicas.
  - `baixar_imagens()`: Baixa as imagens associadas aos livros.

## Contribuições

Contribuições são bem-vindas! Siga estas etapas para contribuir:

1. **Fork** o repositório.
2. Crie uma **branch** para a sua feature ou correção:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça o commit das suas alterações:
   ```bash
   git commit -m 'Adiciona nova funcionalidade'
   ```
4. Envie as alterações para o repositório remoto:
   ```bash
   git push origin minha-feature
   ```
5. Abra um **pull request** descrevendo suas alterações.

