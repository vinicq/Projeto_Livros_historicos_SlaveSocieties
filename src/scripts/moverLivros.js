const fs = require('fs-extra');
const path = require('path');

function moverLivros() {
    const oldDirectory = path.join(__dirname, '../../livros');
    const newDirectory = path.join(__dirname, '../../livros/Paraiba/arquivo_do_forum_nivaldo_de_farias_brito');

    // Cria a nova estrutura se necessário
    fs.ensureDirSync(newDirectory);

    // Move os arquivos
    fs.readdirSync(oldDirectory).forEach((livro) => {
        const oldPath = path.join(oldDirectory, livro);
        const newPath = path.join(newDirectory, livro);

        if (fs.existsSync(newPath)) {
            console.log(`Livro '${livro}' já está na nova estrutura. Pulando...`);
            return;
        }

        try {
            fs.moveSync(oldPath, newPath);
            console.log(`Livro '${livro}' movido para '${newPath}'`);
        } catch (error) {
            console.error(`Erro ao mover o livro '${livro}': ${error.message}`);
        }
    });

    console.log('Todos os livros foram movidos com sucesso.');
}

module.exports = moverLivros;
