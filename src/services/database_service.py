import sqlite3
import logging

def conectar_banco(caminho_banco):
    try:
        conn = sqlite3.connect(caminho_banco)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabelas(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                livro_id TEXT,
                titulo TEXT,
                descricao TEXT,
                total_paginas INTEGER,
                paginas_baixadas INTEGER,
                completo INTEGER,
                tamanho_total INTEGER
            )
        ''')
        conn.commit()
        logging.info("Tabela de livros criada com sucesso.")
    except sqlite3.Error as e:
        logging.error(f"Erro ao criar tabela de livros: {e}")

def inserir_livros(conn, livros):
    try:
        cursor = conn.cursor()
        for livro in livros:
            cursor.execute('''
                INSERT INTO livros (livro_id, titulo, descricao, total_paginas, paginas_baixadas, completo, tamanho_total)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (livro['id'], livro['fields']['title'], livro['fields'].get('description', 'Sem descrição disponível'),
                  int(livro['fields'].get('images', 0)), 0, 0, 0))
        conn.commit()
        logging.info("Livros inseridos no banco de dados com sucesso.")
    except sqlite3.Error as e:
        logging.error(f"Erro ao inserir livros no banco de dados: {e}")

def atualizar_banco_dados(conn, titulo, paginas_baixadas, completo, tamanho_total):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE livros
            SET paginas_baixadas = ?, completo = ?, tamanho_total = ?
            WHERE titulo = ?
        ''', (paginas_baixadas, completo, tamanho_total, titulo))
        conn.commit()
        logging.info(f"Dados atualizados no banco de dados para o livro '{titulo}'.")
    except sqlite3.Error as e:
        logging.error(f"Erro ao atualizar banco de dados: {e}")

def verificar_todos_livros_baixados(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT livro_id, titulo, paginas_baixadas, total_paginas FROM livros")
        livros = cursor.fetchall()
        for livro in livros:
            livro_id, titulo, paginas_baixadas, total_paginas = livro
            if paginas_baixadas >= total_paginas:
                logging.info(f"Livro '{titulo}' (ID: {livro_id}) já foi completamente baixado.")
            else:
                logging.info(f"Livro '{titulo}' (ID: {livro_id}) ainda está incompleto. {paginas_baixadas}/{total_paginas} páginas baixadas.")
    except sqlite3.Error as e:
        logging.error(f"Erro ao verificar os livros no banco de dados: {e}")

def inicializar_banco_dados():
    caminho_banco = 'livros.db'
    conn = conectar_banco(caminho_banco)
    if conn is not None:
        criar_tabelas(conn)
    return conn