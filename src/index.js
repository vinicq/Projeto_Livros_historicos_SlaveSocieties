// src/index.js
const fs = require('fs');
const path = require('path');
const livroService = require('./services/livroService');
const downloadService = require('./services/downloadService');
const gerarSJDC = require('../scripts/gerarSJDC');
const fileUtils = require('./utils/fileUtils');
const config = require('./config/config');
const sharp = require('sharp');

async function inicializar() {
    const logFile = path.join(__dirname, '../logs', `download_log_${new Date().toISOString().replace(/[:.]/g, '_')}.txt`);
    fs.writeFileSync(logFile, 'Log de download de livros:\n', 'utf8');

    if (!fileUtils.arquivoExiste(config.dataPath) || fileUtils.arquivoVazio(config.dataPath)) {
        console.log('Arquivo SJDC.json não encontrado ou vazio. Gerando um novo arquivo...');
        await gerarSJDC();
    }

    const dadosLivros = require(config.dataPath);

    if (!dadosLivros.hits || !dadosLivros.hits.hit) {
        console.error('Formato inesperado no arquivo SJDC.json.');
        return;
    }

    const livros = dadosLivros.hits.hit;

    for (const livro of livros) {
        const livroId = livro.id;
        const titulo = livro.fields.title.replace(/[^\w\s]/gi, '').replace(/\s+/g, '_');
        const diretorioLivro = path.join(config.downloadPath, titulo);

        // Cria o diretório para o livro, se não existir
        if (!fs.existsSync(diretorioLivro)) {
            fs.mkdirSync(diretorioLivro, { recursive: true });
        }

        const descricao = livro.fields.description || 'Sem descrição disponível';
        const caminhoDescricao = path.join(diretorioLivro, `${titulo}.txt`);
        fs.writeFileSync(caminhoDescricao, descricao, 'utf8');
        console.log(`Descrição salva em ${caminhoDescricao}`);

        // Verifica quais páginas já foram baixadas
        const paginasExistentes = new Set(fs.readdirSync(diretorioLivro).map(f => f.replace('.jpg', '')));
        let numeroPagina = '0001';
        const ultimaPagina = String(livro.fields.images).padStart(4, '0');

        // Laço para baixar cada imagem do livro
        while (parseInt(numeroPagina) <= parseInt(ultimaPagina)) {
            const caminhoArquivo = path.join(diretorioLivro, `${numeroPagina}.jpg`);

            // Verifica se a página já foi baixada
            if (paginasExistentes.has(numeroPagina)) {
                console.log(`Página ${numeroPagina} já baixada. Pulando...`);
            } else {
                const sucesso = await downloadService.baixarImagemComResolucao(livroId, numeroPagina, caminhoArquivo);
                if (!sucesso) {
                    console.log(`Falhou ao baixar a página ${numeroPagina}.`);
                    fs.appendFileSync(logFile, `Falhou ao baixar a página ${numeroPagina}\n`);
                } else {
                    try {
                        const { width, height, size } = await sharp(caminhoArquivo).metadata();
                        fs.appendFileSync(logFile, `Imagem ${numeroPagina}.jpg baixada com sucesso. Tamanho: ${size} bytes, Resolução: ${width}x${height}\n`);
                    } catch (error) {
                        console.log(`Erro ao verificar a imagem ${numeroPagina}: ${error.message}`);
                        fs.appendFileSync(logFile, `Erro ao verificar a imagem ${numeroPagina}.jpg: ${error.message}\n`);
                    }
                }
            }

            numeroPagina = String(parseInt(numeroPagina) + 1).padStart(4, '0');
        }
    }

    console.log('Todos os livros foram processados. Verifique os logs para detalhes.');
}

inicializar().catch(err => {
    console.error('Erro ao executar o script:', err);
});
