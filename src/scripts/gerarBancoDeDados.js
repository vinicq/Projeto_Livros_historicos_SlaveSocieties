const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs-extra');

function gerarBancoDeDados() {
    const dbPath = path.join(__dirname, '../../livros/livros_info.db');

    // Cria o banco de dados e uma conexão
    const db = new sqlite3.Database(dbPath, (err) => {
        if (err) {
            console.error(`Erro ao criar o banco de dados: ${err.message}`);
            return;
        }
        console.log(`Banco de dados criado em: ${dbPath}`);
    });

    // Cria a tabela
    db.serialize(() => {
        db.run(`CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT
        )`, (err) => {
            if (err) {
                console.error(`Erro ao criar a tabela: ${err.message}`);
            }
        });

        // Insere alguns dados de exemplo
        const insert = 'INSERT INTO livros (titulo, descricao) VALUES (?, ?)';
        const livrosDir = path.join(__dirname, '../../livros/Paraiba');

        fs.readdirSync(livrosDir).forEach((file) => {
            if (file.endsWith('.txt')) {
                const titulo = file.replace('.txt', '');
                const descricao = fs.readFileSync(path.join(livrosDir, file), 'utf8');
                db.run(insert, [titulo, descricao], (err) => {
                    if (err) {
                        console.error(`Erro ao inserir dados: ${err.message}`);
                    }
                });
            }
        });
    });

    // Fecha o banco de dados
    db.close((err) => {
        if (err) {
            console.error(`Erro ao fechar o banco de dados: ${err.message}`);
        }
    });
}

module.exports = gerarBancoDeDados;
