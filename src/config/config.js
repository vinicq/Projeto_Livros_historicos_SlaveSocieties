// src/config/config.js
const path = require('path');

module.exports = {
    apiUrl: 'https://images.slavesocieties.org/iiif/3/', // URL da API principal
    downloadPath: path.join(__dirname, '../../livros'),
    dataPath: path.join(__dirname, '../data/SJDC.json'),
    retryAttempts: 3,
    logPath: './logs',
    databasePath: './pageObject', // Diretório para o banco de dados
    excelOutputPath: './logs', // Diretório para o Excel
    delayBetweenAttempts: 2000, // 2 segundos
    apiOptions: {
        default: 'https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Par%C3%B3quia%20de%20Nossa%20Senhora%20dos%20Milagres%27&q.parser=structured&size=10000',
        forum: 'https://9x6n6cxjaa.execute-api.us-east-1.amazonaws.com/dev/?q=institution:%27Arquivo%20do%20F%C3%B3rum%20Nivaldo%20de%20Farias%20Brito%27&q.parser=structured&size=10000'
    }
};
