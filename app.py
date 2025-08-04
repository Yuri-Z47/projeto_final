import flask
import sqlite3
from secrets import token_hex

app = flask.Flask(__name__)
app.secret_key = token_hex()

def is_admin():
    return flask.session.get("login") == "yzd"

@app.context_processor
def inject_user():
    return {
        "session": flask.session,
        "is_admin": is_admin()
    }

def format_preco(preco):
    try:
        if isinstance(preco, str):
            preco = preco.replace(',', '.')
        return float(preco)
    except:
        return 0.0
    
def formatar_produto(p):
    preco_float = format_preco(p[1])
    desconto = int(p[4] or 0)
    preco_desconto = preco_float * (1 - desconto / 100)
    preco_original_format = f"{preco_float:,.2f}".replace('.', ',')
    preco_desconto_format = f"{preco_desconto:,.2f}".replace('.', ',')
    return {
        "img": p[0],
        "preco_original": preco_original_format,
        "nome": p[2],
        "id": p[3],
        "desconto": desconto,
        "preco_com_desconto": preco_desconto_format
    }

@app.get("/")
def get_home():
    return flask.render_template("home.html")

@app.get("/login")
def get_login():
    return flask.render_template("login.html", erro=None)

@app.post("/login")
def post_login():
    login = flask.request.form['login']
    senha = flask.request.form['senha']

    sql = "SELECT login, senha, nome, email FROM usuarios WHERE login = ?"
    with sqlite3.Connection('produtos.db') as conn:
        usuario = conn.execute(sql, (login,)).fetchone()

    if usuario and usuario[1] == senha:
        flask.session["login"] = usuario[0]
        flask.session["nome"] = usuario[2]
        flask.session["email"] = usuario[3]
        return flask.redirect("/")
    else:
        return flask.render_template("login.html", erro="Login ou senha incorretos.")

@app.get("/logout")
def get_logout():
    flask.session.clear()
    return flask.redirect('/')

@app.get('/produtos')
def get_produtos():
    sql = "SELECT img, preco, nome, id, desconto FROM produtos ORDER BY preco DESC;"
    with sqlite3.Connection('produtos.db') as conn:
        produtos_raw = conn.execute(sql).fetchall()

    produtos = [formatar_produto(p) for p in produtos_raw]

    return flask.render_template("lista_produtos.html", produtos=produtos)

@app.get("/categoria/<id>")
def get_categoria(id):
    sql = "SELECT img, preco, nome, id, desconto FROM produtos WHERE id_categoria = ? ORDER BY nome;"
    with sqlite3.Connection('produtos.db') as conn:
        produtos_raw = conn.execute(sql, (id,)).fetchall()

    produtos = [formatar_produto(p) for p in produtos_raw]

    return flask.render_template("lista_produtos.html", produtos=produtos)

@app.get("/editar/<id_produto>")
def editar_produto(id_produto):
    if not is_admin():
        return flask.redirect("/")
    with sqlite3.Connection('produtos.db') as conn:
        categorias = conn.execute("SELECT id, nome FROM categorias;").fetchall()
        produto = conn.execute(
            "SELECT id, nome, preco, img, id_categoria, desconto FROM produtos WHERE id = ?",
            (id_produto,)
        ).fetchone()
    if not produto:
        return flask.redirect("/")
    dados_produto = {
        "id": produto[0],
        "nome": produto[1],
        "preco": produto[2],
        "img": produto[3],
        "id_categoria": produto[4],
        "desconto": produto[5] or 0
    }
    return flask.render_template("editar_produto.html", categorias=categorias, produto=dados_produto)

@app.post("/atualizar")
def atualizar_produto():
    if not is_admin():
        return flask.redirect("/")
    id = flask.request.form['id']
    nome = flask.request.form['nome']
    preco = flask.request.form['preco']
    img = flask.request.form['img']
    id_categoria = flask.request.form['categoria']
    desconto = flask.request.form.get('desconto', 0)
    try:
        desconto = int(desconto)
    except:
        desconto = 0

    sql = '''
    UPDATE produtos SET img=?, nome=?, preco=?, id_categoria=?, desconto=? WHERE id=?
    '''
    with sqlite3.Connection('produtos.db') as conn:
        conn.execute(sql, (img, nome, preco, id_categoria, desconto, id))
        conn.commit()
    return flask.redirect("/")

@app.get("/cadastrar")
def get_cadastrar():
    if not is_admin():
        return flask.redirect("/")
    with sqlite3.Connection('produtos.db') as conn:
        categorias = conn.execute("SELECT id, nome FROM categorias;").fetchall()
    return flask.render_template("cadastro_produtos.html", categorias=categorias)

@app.post("/cadastrar")
def post_cadastrar():
    if not is_admin():
        return flask.redirect("/")
    nome = flask.request.form.get("nome")
    preco = flask.request.form.get("preco")
    img = flask.request.form.get("img")
    categoria = flask.request.form.get("categoria")

    sql = "INSERT INTO produtos (nome, preco, img, id_categoria) VALUES (?, ?, ?, ?)"
    with sqlite3.Connection("produtos.db") as conn:
        conn.execute(sql, (nome, preco, img, categoria))
        conn.commit()
    return flask.redirect(f"/categoria/{categoria}")

@app.get('/pesquisar')
def get_pesquisar():
    return flask.render_template("pesquisar.html")

@app.post("/pesquisar")
def post_pesquisar():
    nome = flask.request.form.get("nome", "")
    sql = "SELECT img, preco, nome, id, desconto FROM produtos WHERE nome LIKE ? ORDER BY nome ASC;"
    with sqlite3.Connection('produtos.db') as conn:
        lista_de_produtos = conn.execute(sql, ('%' + nome + '%',)).fetchall()
        if not lista_de_produtos:
            lista_de_produtos = [('', '0,00', 'não encontrado', 0, 0)]

    produtos = [formatar_produto(p) for p in lista_de_produtos]
    return flask.render_template("lista_produtos.html", produtos=produtos)

@app.get("/excluir/<id_produto>")
def excluir_produto(id_produto):
    if not is_admin():
        return flask.redirect("/")
    sql = "DELETE FROM produtos WHERE id = ?"
    with sqlite3.Connection('produtos.db') as conn:
        conn.execute(sql, (id_produto,))
        conn.commit()
    return flask.redirect("/")

@app.get('/comentarios')
def get_comentarios():
    return flask.render_template('comentarios.html', login=flask.session.get('login'),
                                 nome=flask.session.get('nome'), email=flask.session.get('email'))

@app.post('/comentarios')
def post_comentarios():
    if 'login' not in flask.session:
        return flask.redirect('/login')

    nome = flask.session.get('nome')
    email = flask.session.get('email')
    comentario = flask.request.form['comentario']

    print(f'Novo comentário de {nome} ({email}): {comentario}')

    return flask.redirect('/')

@app.get("/cadastrar_usuario")
def get_cadastrar_usuario():
    return flask.render_template("cadastro_usuario.html", erro=None)

@app.post("/cadastrar_usuario")
def post_cadastrar_usuario():
    login = flask.request.form.get("login")
    senha = flask.request.form.get("senha")
    nome = flask.request.form.get("nome")
    email = flask.request.form.get("email")

    if not all([login, senha, nome, email]):
        return flask.render_template("cadastro_usuario.html", erro="Preencha todos os campos!")

    with sqlite3.Connection("produtos.db") as conn:
        cur = conn.execute("SELECT 1 FROM usuarios WHERE login = ?", (login,))
        if cur.fetchone():
            return flask.render_template("cadastro_usuario.html", erro="Login já existe, tente outro.")

        # salva senha em texto puro (mantido conforme sua decisão)
        conn.execute(
            "INSERT INTO usuarios (login, senha, nome, email) VALUES (?, ?, ?, ?)",
            (login, senha, nome, email)
        )
        conn.commit()

    return flask.redirect("/login")

app.run(host='0.0.0.0', debug=True)