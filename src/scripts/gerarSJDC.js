const fs = require('fs-extra');
const path = require('path');

function gerarSJDC() {
    const savePath = path.join(__dirname, '../../livros/Paraiba');
    const fileName = 'SJDC.json';
    const filePath = path.join(savePath, fileName);

    const data = {
        institution: "Paróquia de Nossa Senhora dos Milagres",
        description: "Dados gerados automaticamente para SJDC."
    };

    fs.ensureDirSync(savePath);

    try {
        fs.writeJsonSync(filePath, data);
        console.log(`Arquivo ${fileName} gerado em ${filePath}`);
    } catch (error) {
        console.error(`Erro ao gerar SJDC: ${error.message}`);
    }
}

module.exports = gerarSJDC;
