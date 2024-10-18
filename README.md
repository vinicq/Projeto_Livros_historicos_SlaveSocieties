# Projeto Livros Históricos / Historical Books Project

Este projeto tem como objetivo automatizar o processo de download, organização e processamento de livros históricos, utilizando APIs públicas para extrair metadados e imagens, e aplicando OCR para converter imagens de documentos históricos em texto pesquisável. Também usamos bancos de dados SQLite para armazenar os dados extraídos.

This project aims to automate the process of downloading, organizing, and processing historical books by utilizing public APIs to extract metadata and images, and applying OCR to convert historical document images into searchable text. We also use SQLite databases to store the extracted data.

## Funcionalidades Principais / Main Features

- **Download de livros históricos / Download of Historical Books**: Requisições automáticas a APIs públicas para baixar metadados e imagens.
- **Processamento de imagens / Image Processing**: Organização das imagens em pastas e aplicação de OCR para conversão em texto.
- **Armazenamento em Banco de Dados SQLite / Storage in SQLite Database**: Armazena os metadados e informações de progresso do download das imagens.
- **Integração com manifestos IIIF / Integration with IIIF Manifests**: Utiliza manifestos IIIF para gerenciar as páginas dos livros.
- **OCR com Tesseract / OCR with Tesseract**: Converte imagens de documentos históricos em texto pesquisável.

## Estrutura do Projeto / Project Structure

O projeto é organizado com base em múltiplos serviços para facilitar o download, processamento de dados e armazenamento.

The project is organized around multiple services to facilitate downloading, data processing, and storage.

### Arquivos Principais / Main Files

1. **`main.py`**: O ponto de entrada principal que coordena o fluxo do projeto, baixando dados, processando-os e armazenando no banco de dados.
   - This is the main entry point that orchestrates the project’s workflow by downloading, processing, and storing data in the database.

2. **`src/services/api_service.py`**: Realiza requisições às APIs para obter dados históricos e salva os resultados localmente e no banco de dados.
   - This file makes requests to public APIs to retrieve historical data and stores it locally and in the database.

3. **`src/services/database_service.py`**: Gerencia o banco de dados SQLite, criando tabelas e inserindo dados.
   - Handles the SQLite database, creating tables and inserting data.

4. **`src/services/file_service.py`**: Gerencia a criação de pastas e o armazenamento de imagens.
   - Manages folder creation and image storage.

5. **`src/services/manifest_service.py`**: Verifica e baixa os manifestos IIIF, além de salvar as imagens associadas.
   - Verifies and downloads IIIF manifests and saves the associated images.

6. **`src/ai/ocr.py`**: Aplica OCR nas imagens baixadas para converter o conteúdo em texto.
   - Applies OCR to downloaded images to convert content into text.

7. **`src/ai/process_text.py`**: Processa o texto extraído usando técnicas de NLP (Processamento de Linguagem Natural).
   - Processes the extracted text using NLP techniques.

8. **`src/ai/model.py`**: Treina modelos de aprendizado de máquina para reconhecer padrões nos textos extraídos.
   - Trains machine learning models to recognize patterns in the extracted text.

9. **`src/ai/test_ai.py`**: Script de teste para o OCR e o processamento de texto.
   - Test script for OCR and text processing.

## Fluxo de Trabalho / Workflow

1. **Download de Dados / Data Download**: O projeto baixa os dados das APIs fornecidas.
   - The project downloads data from provided APIs.

2. **Processamento e Armazenamento / Processing and Storage**: Os dados são processados e armazenados no banco de dados SQLite.
   - Data is processed and stored in the SQLite database.

3. **Download de Imagens e Manifestos / Image and Manifest Download**: Imagens de livros históricos são baixadas e organizadas com base nos manifestos IIIF.
   - Historical book images are downloaded and organized based on IIIF manifests.

4. **Processamento de OCR / OCR Processing**: As imagens baixadas passam por OCR para converter o texto das páginas em texto pesquisável.
   - Downloaded images undergo OCR processing to convert page text into searchable text.

5. **Treinamento de Modelos de Machine Learning / Machine Learning Model Training**: Modelos de machine learning podem ser treinados para analisar e reconhecer padrões nos textos.
   - Machine learning models can be trained to analyze and recognize patterns in the text.

## Tecnologias Utilizadas / Technologies Used

- **Python 3.x**: Linguagem principal usada no projeto.
- **SQLite**: Banco de dados leve para armazenamento de metadados.
- **Tesseract OCR**: Utilizado para extrair texto de imagens.
- **APIs Públicas**: Fonte de dados históricos de livros.
- **IIIF**: Para organizar e baixar imagens de livros históricos.

## Instalação / Installation

### Pré-requisitos / Prerequisites

- **Python 3.x**
- **pip**: Instalador de pacotes do Python.
- **Tesseract OCR**: Para instalar o Tesseract, siga as instruções de instalação no site oficial [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).

### Passos para Instalação / Installation Steps

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/projeto-livros-historicos.git
   ```

2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o caminho para o Tesseract OCR no arquivo `src/ai/ocr.py`:
   - Altere a linha:
     ```python
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
     ```
   - Substitua pelo caminho correto no seu sistema.

5. (Opcional) Para desativar o ambiente virtual quando terminar:
   ```bash
   deactivate
   ```

## Como Executar o Projeto / How to Run the Project

### Executando o Script Principal / Running the Main Script

Execute o arquivo `main.py` localizado na raiz do projeto:
```bash
python main.py
```

Este script principal coordena todo o processo de download, processamento e armazenamento dos dados históricos.

This main script orchestrates the entire process of downloading, processing, and storing historical data.

### Logs

Os logs de execução são armazenados na pasta `logs/` e podem ser usados para monitorar o progresso ou investigar erros.

Execution logs are stored in the `logs/` folder and can be used to check progress or investigate errors.

---

## Licença / License

Este projeto está licenciado sob a [MIT License](LICENSE).
This project is licensed under the [MIT License](LICENSE).

