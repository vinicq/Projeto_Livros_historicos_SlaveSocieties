const fs = require('fs');
const path = require('path');
const config = require('../config/config');

function verificarLivroBaixado(livroId, titulo) {
    const diretorioLivro = path.join(config.downloadPath, titulo);
    return fs.existsSync(diretorioLivro);
}

function obterPaginasBaixadas(diretorioLivro) {
    return new Set(fs.readdirSync(diretorioLivro).map(f => f.replace('.jpg', '')));
}

module.exports = {
    verificarLivroBaixado,
    obterPaginasBaixadas
};
