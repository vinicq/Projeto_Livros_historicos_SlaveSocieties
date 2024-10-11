// src/services/downloadService.js
const axios = require('axios');
const fs = require('fs');

// Função para baixar uma imagem com verificação de integridade
async function baixarImagem(url, caminhoArquivo, tentativas = 3) {
    for (let i = 0; i < tentativas; i++) {
        try {
            const response = await axios({
                url,
                method: 'GET',
                responseType: 'stream',
            });

            // Verifica se o diretório existe
            const stream = fs.createWriteStream(caminhoArquivo);
            response.data.pipe(stream);

            // Espera até que o arquivo seja completamente gravado no disco
            await new Promise((resolve, reject) => {
                stream.on('finish', resolve);
                stream.on('error', reject);
            });

            console.log(`Imagem baixada: ${url}`);
            return true; // Indica que o download foi bem-sucedido
        } catch (erro) {
            console.log(`Falha ao baixar ${url}: ${erro.message}`);
            if (i < tentativas - 1) {
                console.log('Tentando novamente...');
                await new Promise(resolve => setTimeout(resolve, 2000)); // Espera 2 segundos antes de tentar novamente
            }
        }
    }
    console.log(`Falhou após ${tentativas} tentativas: ${url}`);
    return false; // Indica que o download falhou
}

// Função para verificar se o arquivo foi baixado corretamente (baseado no tamanho)
function verificarIntegridade(caminhoArquivo) {
    try {
        const stats = fs.statSync(caminhoArquivo);
        // Verifica se o tamanho do arquivo é aceitável (> 10 KB, por exemplo)
        return stats.size > 10240; // 10 KB
    } catch (erro) {
        console.log(`Erro ao verificar o arquivo ${caminhoArquivo}: ${erro.message}`);
        return false;
    }
}

// Função para tentar baixar em diferentes resoluções
async function baixarImagemComResolucao(livroId, numeroPagina, caminhoArquivo) {
    const resolucoes = ['1500,2000', '750,1000', '375,500'];
    for (const resolucao of resolucoes) {
        const urlImagem = `https://images.slavesocieties.org/iiif/3/${livroId}-${numeroPagina}.jpg/full/${resolucao}/0/default.jpg`;
        const sucesso = await baixarImagem(urlImagem, caminhoArquivo);
        if (sucesso && verificarIntegridade(caminhoArquivo)) {
            console.log(`Imagem ${numeroPagina} baixada com sucesso e verificada.`);
            return true; // Baixou e verificou com sucesso em uma das resoluções
        } else {
            console.log(`Falha ao verificar a integridade da imagem ${numeroPagina} para resolução ${resolucao}. Tentando outra resolução...`);
            fs.unlinkSync(caminhoArquivo); // Remove o arquivo corrompido
        }
    }
    console.log(`Nenhuma das resoluções funcionou para a imagem ${numeroPagina}`);
    return false;
}

module.exports = {
    baixarImagemComResolucao,
};
