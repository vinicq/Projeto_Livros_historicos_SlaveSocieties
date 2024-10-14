const path = require('path');
const downloadForum = require('./downloadForum');
const gerarSJDC = require('./gerarSJDC');
const gerarBancoDeDados = require('./gerarBancoDeDados');

const action = process.argv[2];

switch (action) {
    case 'downloadLivros':
        downloadForum();
        break;
    case 'gerarSJDC':
        gerarSJDC();
        break;
    case 'gerarBancoDeDados':
        gerarBancoDeDados();
        break;
    default:
        console.log('Ação não reconhecida. Use downloadLivros, gerarSJDC ou gerarBancoDeDados.');
        break;
}