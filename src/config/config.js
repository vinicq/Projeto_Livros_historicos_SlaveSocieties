// src/config/config.js
const path = require('path');

module.exports = {
    apiUrl: 'https://images.slavesocieties.org/iiif/3/', // URL da API principal
    downloadPath: path.join(__dirname, '../../livros'), // Diretório para salvar os livros baixados
    dataPath: path.join(__dirname, '../data/SJDC.json'), // Caminho para o arquivo JSON de dados
    retryAttempts: 3, // Número de tentativas de download antes de falhar
    logPath: path.join(__dirname, '../../logs'), // Diretório para os logs
    databasePath: path.join(__dirname, '../../pageObject'), // Diretório para o banco de dados SQLite
    excelOutputPath: path.join(__dirname, '../../logs'), // Diretório para salvar o arquivo Excel
    delayBetweenAttempts: 2000, // 2 segundos de atraso entre as tentativas
    apiOptions: {
        default: 'https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Par%C3%B3quia%20de%20Nossa%20Senhora%20dos%20Milagres%27&q.parser=structured&size=10000',
        alternative: 'https://outra-api.com/v1/livros' // URL alternativa para a API
    }
};
