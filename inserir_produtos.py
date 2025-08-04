import sqlite3

conn = sqlite3.Connection('produtos.db')

# Criação da tabela de usuários
conn.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    login TEXT NOT NULL,
    senha TEXT NOT NULL,
    nome TEXT,
    email TEXT
)
''')

# Criação da tabela de categorias
conn.execute('''
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL
)
''')

# Criação da tabela de produtos com desconto e preço como REAL
conn.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY,
    img TEXT NOT NULL,
    preco REAL NOT NULL,
    nome TEXT NOT NULL,
    id_categoria INTEGER NOT NULL,
    desconto INTEGER DEFAULT 0,
    FOREIGN KEY(id_categoria) REFERENCES categorias(id)
)
''')

conn.commit()

# Inserindo categorias
conn.executemany(
    'INSERT INTO categorias (nome) VALUES (?)',
    [
        ('Pestiscos',),
        ('Hamburgueres',),
        ('Drinks/bebidas',)
    ]
)

# Inserindo produtos com alguns descontos
conn.executemany(
    'INSERT INTO produtos (img, preco, nome, id_categoria, desconto) VALUES (?, ?, ?, ?, ?)',
    [
        ('1.jpg', 150.00, 'Coisa 1', 3, 0),
        ('2.jpg', 250.00, 'Coisa 2', 2, 15),
        ('3.jpg', 150.00, 'Coisa 3', 2, 10),
        ('4.jpg', 150.00, 'Coisa 4', 1, 0),
        ('5.jpg', 150.00, 'Coisa 5', 1, 5),
        ('6.jpg', 150.00, 'Coisa 6', 3, 20),
        ('7.jpg', 150.00, 'Coisa 7', 3, 0),
        ('8.jpg', 150.00, 'Coisa 8', 1, 0),
    ]
)

# Inserindo usuários
conn.executemany(
    'INSERT INTO usuarios (login, senha, nome, email) VALUES (?, ?, ?, ?)',
    [
        ('prof','12345', 'Prof. Gustavo', 'lgmaciel@senacrs.com.br'),
        ('grz', 'tech@2025','Gustavo Razzera', 'grz@email.com'),
        ('yzd', '12345', 'Yuri Zambrano', 'yuri@gmail.com')
    ]
)

conn.commit()
conn.close()
