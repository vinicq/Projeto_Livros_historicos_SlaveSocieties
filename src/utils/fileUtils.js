const fs = require('fs');

function arquivoExiste(caminho) {
    return fs.existsSync(caminho);
}

function arquivoVazio(caminho) {
    try {
        const stats = fs.statSync(caminho);
        return stats.size === 0;
    } catch (err) {
        return true; // Considera vazio em caso de erro
    }
}

module.exports = {
    arquivoExiste,
    arquivoVazio
};
