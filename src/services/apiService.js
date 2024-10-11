// src/services/apiService.js
const axios = require('axios');
const config = require('../config/config');

// Função para buscar dados de livros a partir da API configurada
async function buscarLivros() {
    try {
        console.log('Baixando os dados da API configurada...');
        const response = await axios.get(config.apiUrl);
        if (response.status === 200) {
            return response.data;
        } else {
            console.error('Erro ao obter os dados da API:', response.status, response.statusText);
            return null;
        }
    } catch (error) {
        console.error('Ocorreu um erro ao acessar a API:', error.message);
        return null;
    }
}

module.exports = {
    buscarLivros
};
