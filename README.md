# Projeto de Livros Históricos

Este projeto automatiza o processo de download, verificação, armazenamento e análise de dados relacionados a livros históricos disponíveis via uma API pública. Ele utiliza Node.js para a automação, manipulação de arquivos e banco de dados, com a integração de bibliotecas específicas para facilitar o processamento das imagens e geração de relatórios.

## Pré-requisitos

Antes de rodar o projeto, certifique-se de que os seguintes itens estão instalados no seu sistema:

1. **Node.js** (v20 ou superior) - [Instale o Node.js](https://nodejs.org/)
2. **Git** (para gerenciamento de código) - [Instale o Git](https://git-scm.com/)

## Dependências do projeto

Este projeto utiliza várias bibliotecas e dependências, listadas no arquivo `package.json`. Aqui estão as principais:

- `axios`: para fazer requisições HTTP para a API de download de livros.
- `fs` e `path`: para manipulação de arquivos e diretórios.
- `sharp`: para manipular imagens e verificar se os arquivos de imagem estão completos ou corrompidos.
- `sqlite3`: para gerenciar o banco de dados local.
- `exceljs`: para gerar arquivos Excel com informações dos livros baixados.
- `dotenv` (opcional): para gerenciar variáveis de ambiente, se necessário.

## Instalação

Siga as instruções abaixo para configurar e rodar o projeto em sua máquina local.

1. **Clone o repositório**

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd Projeto_livros_historicos
   ```

2. **Instale as dependências**

   Execute o seguinte comando para instalar todas as bibliotecas necessárias:

   ```bash
   npm install
   ```

## Configuração

1. **Arquivo de Configuração (`src/config/config.js`)**

   O arquivo de configuração contém os caminhos e URLs principais do projeto. Verifique se os diretórios de download e logs estão corretos:

   ```javascript
   module.exports = {
       apiUrl: 'https://images.slavesocieties.org/iiif/3/',
       downloadPath: './livros', // Pasta onde os arquivos serão baixados
       logPath: './logs', // Pasta para os logs de download
       databasePath: './pageObject', // Diretório para o banco de dados
       excelOutputPath: './logs', // Diretório para os arquivos Excel
       delayBetweenAttempts: 2000, // Intervalo entre tentativas de download (em ms)
       retryAttempts: 3, // Número de tentativas de download
       apiOptions: {
           default: 'https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Par%C3%B3quia%20de%20Nossa%20Senhora%20dos%20Milagres%27&q.parser=structured&size=10000'
       }
   };
   ```

2. **Configuração de variáveis de ambiente (opcional)**

   Se precisar configurar variáveis de ambiente para a API, você pode usar um arquivo `.env`:

   ```bash
   API_KEY=SuaApiKeyAqui
   ```

## Executando o projeto

### 1. Gerando o arquivo `SJDC.json`

Para começar, é necessário gerar o arquivo `SJDC.json`, que contém os metadados dos livros:

```bash
node scripts/gerarSJDC.js
```

Este script irá buscar dados da API e gerar o arquivo `SJDC.json` dentro do diretório `data`.

### 2. Baixando os livros

Após gerar o arquivo `SJDC.json`, execute o seguinte comando para iniciar o download dos livros:

```bash
node src/index.js
```

Este script irá:
- Baixar os livros especificados no `SJDC.json`.
- Salvar os arquivos na pasta `livros`.
- Verificar a integridade das imagens.
- Gerar logs com informações dos arquivos baixados.

### 3. Gerando o banco de dados

Para organizar os dados em um banco de dados SQLite, execute:

```bash
node scripts/gerarBancoDeDados.js
```

Este script irá:
- Ler os arquivos na pasta `livros`.
- Criar um banco de dados SQLite na pasta `pageObject`.
- Armazenar informações sobre cada livro, incluindo nome, quantidade de arquivos e tamanho.

### 4. Exportando para Excel

Para exportar os dados dos livros para um arquivo Excel, o script `gerarBancoDeDados.js` já inclui a funcionalidade de gerar um arquivo `.xlsx` na pasta `logs`. O nome do arquivo incluirá a data de geração para facilitar a organização, por exemplo:

```
logs/livros_info_2024-10-11.xlsx
```

## Estrutura do projeto

O projeto é organizado da seguinte forma:

```
Projeto_livros_historicos/
├── data/                   # Arquivos de dados (e.g., SJDC.json)
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

   Verifique se o `apiUrl` no arquivo `config.js` está correto e acessível. Se necessário, atualize para um URL alternativo.

2. **Falha ao baixar imagens**

   Se uma imagem não baixar corretamente, o script tentará novamente até o limite definido em `retryAttempts`. Verifique se há problemas de rede ou com a API.

3. **Banco de dados não gerado**

   Certifique-se de que a pasta `pageObject` existe e que o script possui permissão para gravar arquivos.

4. **Dependências faltando**

   Se o projeto reclamar de dependências não encontradas, execute `npm install` para instalar novamente todas as dependências.

## Melhorias Futuras

1. **Adição de Testes Automatizados**: Implementar testes para garantir a integridade dos scripts e a funcionalidade dos serviços.
2. **Integração com outras fontes de dados**: Possibilitar o download de livros de outras APIs.
3. **Interface Gráfica**: Criar uma interface para facilitar a interação com o projeto.

## Conclusão

Este projeto fornece uma base para automação de download, verificação e análise de dados históricos. Com as bibliotecas e serviços configurados corretamente, ele facilita o processo de coleta e organização dos dados para fins de estudo ou preservação.
```

```
# Gerar db e arquivo xlsx
node scripts/gerarBancoDeDados.js
```

```
# Rodar o projeto
node src/index.js
```