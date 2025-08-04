import sqlite3

conn = sqlite3.Connection('produtos.db')

# Criação da tabela de usuários
sql_criar_tabela_usuarios = '''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    login TEXT NOT NULL,
    senha TEXT NOT NULL,
    nome TEXT,
    email TEXT
);
'''

# Criação da tabela de categorias
sql_criar_tabela_categoria_produto = '''
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL
);
'''

# Criação da tabela de produtos (com campo desconto e preco como REAL)
sql_criar_tabela_produtos = '''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY,
    img TEXT NOT NULL,
    preco REAL NOT NULL,
    nome TEXT NOT NULL,
    id_categoria INTEGER NOT NULL,
    desconto INTEGER DEFAULT 0,
    FOREIGN KEY(id_categoria) REFERENCES categorias(id)
);
'''

# Executa a criação das tabelas
conn.execute(sql_criar_tabela_usuarios)
conn.execute(sql_criar_tabela_categoria_produto)
conn.execute(sql_criar_tabela_produtos)
conn.commit()

# Cadastrando categorias iniciais
sql_insert_categorias = 'INSERT INTO categorias (nome) VALUES (?)'
lista_de_categorias = [
    ('Pestiscos',),
    ('Hamburgueres',),
    ('Drinks/bebidas',)
]

conn.executemany(sql_insert_categorias, lista_de_categorias)

# Cadastrando produtos iniciais (preço com ponto e desconto = 0)
sql_insert_produtos = '''
INSERT INTO produtos (img, preco, nome, id_categoria, desconto) VALUES (?, ?, ?, ?, ?);
'''
lista_de_produtos = [
    ('1.jpg', 150.00, 'Coisa 1', 3, 0),
    ('2.jpg', 250.00, 'Coisa 2', 2, 10),
    ('3.jpg', 150.00, 'Coisa 3', 2, 5),
    ('4.jpg', 150.00, 'Coisa 4', 1, 0),
    ('5.jpg', 150.00, 'Coisa 5', 1, 0),
    ('6.jpg', 150.00, 'Coisa 6', 3, 20),
    ('7.jpg', 150.00, 'Coisa 7', 3, 0),
    ('8.jpg', 150.00, 'Coisa 8', 1, 0),
]

conn.executemany(sql_insert_produtos, lista_de_produtos)


sql_insert_usuarios = '''
INSERT INTO usuarios (login, senha, nome, email) VALUES (?, ?, ?, ?);
'''
lista_de_usuarios = [
    ('prof', '12345', 'Prof. Gustavo', 'lgmaciel@senacrs.com.br'),
    ('grz', 'tech@2025', 'Gustavo Razzera', 'grz@email.com'),
    ('yzd', '12345', 'Yuri Zambrano', 'yuri@gmail.com')
]

conn.executemany(sql_insert_usuarios, lista_de_usuarios)

conn.commit()
conn.close()