const axios = require('axios');
const fs = require('fs');
const path = require('path');
const config = require('../config/config');

async function downloadLivros() {
    try {
        const response = await axios.get(config.apiOptions.forum);

        if (response.data && response.data.hits && response.data.hits.hit) {
            const livros = response.data.hits.hit;
            const dirPath = path.join(config.downloadPath, 'Paraiba', 'arquivo_do_forum_nivaldo_de_farias_brito');

            if (!fs.existsSync(dirPath)) {
                fs.mkdirSync(dirPath, { recursive: true });
            }

            // Salva o JSON com os dados dos livros
            const jsonFilePath = path.join(dirPath, 'livros.json');
            fs.writeFileSync(jsonFilePath, JSON.stringify(livros, null, 2), 'utf8');
            console.log(`Arquivo JSON salvo em ${jsonFilePath}`);

            // Processa cada item dos dados retornados
            livros.forEach((livro) => {
                const descricao = livro.fields.description;
                const titulo = livro.fields.title.replace(/[\/\\?%*:|"<>]/g, ''); 

                const filePath = path.join(dirPath, `${titulo}.txt`);
                fs.writeFileSync(filePath, descricao, 'utf8');
                console.log(`Descrição salva em ${filePath}`);
            });
        } else {
            throw new Error('Estrutura de dados inesperada');
        }
    } catch (error) {
        console.error('Erro ao processar os dados:', error.message);
    }
}

module.exports = downloadLivros;
