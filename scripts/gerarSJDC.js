// scripts/gerarSJDC.js
const axios = require('axios');
const fs = require('fs-extra');
const path = require('path');

// URL da API para obter os dados
const apiUrl = 'https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Par%C3%B3quia%20de%20Nossa%20Senhora%20dos%20Milagres%27&q.parser=structured&size=10000';

// Função para gerar o arquivo SJDC.json
async function gerarArquivoSJDC() {
    try {
        console.log('Baixando os dados da API...');

        // Faz a requisição para a API
        const response = await axios.get(apiUrl);

        // Verifica se a resposta foi bem-sucedida e possui a estrutura esperada
        if (response.status === 200 && response.data.hits && response.data.hits.hit) {
            const dados = response.data;

            // Caminho para o arquivo SJDC.json
            const caminhoArquivo = path.join(__dirname, '..', 'src', 'data', 'SJDC.json');

            // Salva os dados no arquivo SJDC.json
            await fs.writeJson(caminhoArquivo, dados, { spaces: 2 });

            console.log('Arquivo SJDC.json gerado com sucesso.');
        } else {
            console.error('Erro: A resposta da API não possui o formato esperado.');
        }
    } catch (error) {
        console.error('Ocorreu um erro ao gerar o arquivo SJDC.json:', error.message);
    }
}

// Executa a função para gerar o arquivo
gerarArquivoSJDC();
