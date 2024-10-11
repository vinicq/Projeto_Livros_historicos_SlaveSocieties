// gerarBancoDeDados.js
const fs = require('fs');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();
const ExcelJS = require('exceljs');
const config = require('../src/config/config');
const dayjs = require('dayjs'); // Biblioteca para trabalhar com datas

const dateNow = dayjs().format('YYYY-MM-DD_HH-mm-ss');
const databaseFile = path.join(config.databasePath, `livros_info_${dateNow}.db`);
const excelFile = path.join(config.excelOutputPath, `livros_info_${dateNow}.xlsx`);

if (!fs.existsSync(config.databasePath)) {
  fs.mkdirSync(config.databasePath, { recursive: true });
}

if (!fs.existsSync(config.excelOutputPath)) {
  fs.mkdirSync(config.excelOutputPath, { recursive: true });
}

// Função para criar o banco de dados SQLite
function criarBancoDeDados() {
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(databaseFile, (err) => {
      if (err) {
        console.error(`Erro ao criar o banco de dados: ${err.message}`);
        reject(err);
      } else {
        console.log(`Banco de dados criado com sucesso em: ${databaseFile}`);
        resolve(db);
      }
    });
  });
}

// Função para criar a tabela no banco de dados
function criarTabela(db) {
  return new Promise((resolve, reject) => {
    db.run(`
      CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        quantidade_arquivos INTEGER,
        lista_arquivos TEXT,
        tamanho_total INTEGER
      )
    `, (err) => {
      if (err) {
        console.error(`Erro ao criar a tabela: ${err.message}`);
        reject(err);
      } else {
        console.log('Tabela criada com sucesso.');
        resolve();
      }
    });
  });
}

// Função para inserir dados na tabela
function inserirDados(db, livro) {
  return new Promise((resolve, reject) => {
    const { titulo, quantidadeArquivos, listaArquivos, tamanhoTotal } = livro;
    db.run(`
      INSERT INTO livros (titulo, quantidade_arquivos, lista_arquivos, tamanho_total)
      VALUES (?, ?, ?, ?)
    `, [titulo, quantidadeArquivos, JSON.stringify(listaArquivos), tamanhoTotal], (err) => {
      if (err) {
        console.error(`Erro ao inserir dados: ${err.message}`);
        reject(err);
      } else {
        resolve();
      }
    });
  });
}

// Função para gerar o arquivo Excel
async function gerarExcel(livros) {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet('Livros');

  worksheet.columns = [
    { header: 'Título', key: 'titulo', width: 30 },
    { header: 'Quantidade de Arquivos', key: 'quantidadeArquivos', width: 20 },
    { header: 'Lista de Arquivos', key: 'listaArquivos', width: 60 },
    { header: 'Tamanho Total (bytes)', key: 'tamanhoTotal', width: 20 }
  ];

  livros.forEach((livro) => {
    worksheet.addRow({
      titulo: livro.titulo,
      quantidadeArquivos: livro.quantidadeArquivos,
      listaArquivos: livro.listaArquivos.join(', '),
      tamanhoTotal: livro.tamanhoTotal
    });
  });

  await workbook.xlsx.writeFile(excelFile);
  console.log(`Arquivo Excel gerado com sucesso em: ${excelFile}`);
}

// Função principal para processar os livros
async function processarLivros() {
  try {
    const db = await criarBancoDeDados();
    await criarTabela(db);

    const livrosDir = config.downloadPath;
    const livros = [];

    fs.readdirSync(livrosDir).forEach((livroDir) => {
      const livroPath = path.join(livrosDir, livroDir);
      const arquivos = fs.readdirSync(livroPath).filter((file) => file.endsWith('.jpg'));
      const tamanhoTotal = arquivos.reduce((acc, file) => {
        const filePath = path.join(livroPath, file);
        return acc + fs.statSync(filePath).size;
      }, 0);

      const livro = {
        titulo: livroDir,
        quantidadeArquivos: arquivos.length,
        listaArquivos: arquivos,
        tamanhoTotal
      };

      livros.push(livro);
      inserirDados(db, livro);
    });

    await gerarExcel(livros);

    db.close();
    console.log('Processamento finalizado com sucesso.');
  } catch (error) {
    console.error('Erro ao processar os livros:', error);
  }
}

processarLivros();
