const path = require('path');
const config = require('../config/config');
const livroService = require('../services/livroService');
const downloadService = require('../services/downloadService');

// Função para processar o download das páginas de um livro
async function baixarLivro(livro) {
    const livroId = livro.id;
    const titulo = livro.fields.title.replace(/[^\w\s]/gi, '').replace(/\s+/g, '_');
    const diretorioLivro = path.join(config.downloadPath, titulo);

    // Verifica se o livro já foi baixado
    if (livroService.verificarLivroBaixado(livroId, titulo)) {
        console.log(`Livro "${titulo}" já foi baixado. Pulando...`);
        return;
    }

    console.log(`Iniciando o download do livro: ${titulo}`);

    // Número da primeira página
    let numeroPagina = '0001';
    const ultimaPagina = String(livro.fields.images).padStart(4, '0');

    // Laço para baixar as imagens do livro
    while (parseInt(numeroPagina) <= parseInt(ultimaPagina)) {
        const urlImagem = `${config.apiUrl}${livroId}-${numeroPagina}.jpg/full/max/0/default.jpg`;
        const caminhoArquivo = path.join(diretorioLivro, `${numeroPagina}.jpg`);

        // Tenta baixar a imagem com verificação de integridade
        const sucesso = await downloadService.baixarImagem(urlImagem, caminhoArquivo);
        if (!sucesso) {
            console.log(`Falhou ao baixar a página ${numeroPagina}. Encerrando o download do livro.`);
            break; // Sai do laço se falhar ao baixar a página
        }

        // Incrementa para a próxima página
        numeroPagina = String(parseInt(numeroPagina) + 1).padStart(4, '0');
    }

    console.log(`Download concluído para o livro: ${titulo}`);
}

module.exports = { baixarLivro };
