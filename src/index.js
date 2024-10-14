// src/index.js
const fs = require('fs');
const path = require('path');
const livroService = require('./services/livroService');
const downloadService = require('./services/downloadService');
const gerarSJDC = require('../scripts/gerarSJDC');
const fileUtils = require('./utils/fileUtils');
const config = require('./config/config');

async function inicializar() {
    const baseDirectory = path.join(__dirname, '../Livros', 'Paraiba', 'paroquia_de_nossa_senhora_dos_milagres');
    
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
        const diretorioLivro = path.join(baseDirectory, titulo);

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
            const tamanhoImagem = '1500,2000'; // Definindo o tamanho padrão para a imagem

            // Verifica se a página já foi baixada
            if (paginasExistentes.has(numeroPagina)) {
                console.log(`Página ${numeroPagina} já baixada. Pulando...`);
            } else {
                const sucesso = await downloadService.baixarImagemComResolucao(livroId, numeroPagina, caminhoArquivo, tamanhoImagem);
                if (!sucesso) {
                    console.log(`Falhou ao baixar a página ${numeroPagina}.`);
                }
            }

            numeroPagina = String(parseInt(numeroPagina) + 1).padStart(4, '0');
        }

        // Verifica se todas as páginas foram baixadas
        const totalPaginasBaixadas = fs.readdirSync(diretorioLivro).filter(f => f.endsWith('.jpg')).length;
        const statusDownload = totalPaginasBaixadas === parseInt(ultimaPagina) ? 'completo' : 'incompleto';
        console.log(`Download ${statusDownload} para o livro ${livroId}. Páginas baixadas: ${totalPaginasBaixadas}/${ultimaPagina}`);
    }

    console.log('Todos os livros foram processados. Verifique os logs para detalhes.');
}

inicializar().catch(err => {
    console.error('Erro ao executar o script:', err);
});
