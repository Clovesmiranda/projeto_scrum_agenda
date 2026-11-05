import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("dados.db")
    conn.row_factory = sqlite3.Row
    return conn

# ROTAS DE PÁGINAS

@app.get("/login")
def tela_login():
    return render_template("login.html")

@app.get("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.get("/listar_servicos")
def listar_servicos():
    return render_template("listar_servicos.html")


@app.get("/cadastrar_servico")
def tela_cadastrar_servico():
    return render_template("cadastrar_servico.html")

@app.get("/cadastrar_profissional")
def tela_cadastrar_profissional():
    return render_template("cadastrar_profissional.html")

@app.get("/criar_agendamento")
def tela_criar_agendamento():
    conn = get_db()
    servicos = conn.execute("SELECT id, nome FROM servicos").fetchall()
    profissionais = conn.execute("SELECT id, nome FROM profissionais").fetchall()
    conn.close()
    return render_template("criar_agendamento.html",
                           servicos=servicos,
                           profissionais=profissionais)

@app.get("/listar_profissionais")
def listar_profissionais_html():
    return render_template("listar_profissionais.html")


@app.get("/agendamentos")
def listar_agendamentos_html():
    conn = get_db()
    agendamentos = conn.execute("""
        SELECT a.id,
               s.nome AS servico_nome,
               p.nome AS profissional_nome,
               a.data,
               a.horario
        FROM agendamentos a
        JOIN servicos s ON s.id = a.servico_id
        JOIN profissionais p ON p.id = a.profissional_id
    """).fetchall()
    conn.close()
    return render_template("listar_agendamentos.html", agendamentos=agendamentos)

# API SERVIÇOS

@app.post("/servicos")
def cadastrar_servico():
    dados = request.json
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO servicos (nome, preco, duracao) VALUES (?, ?, ?)",
        (dados["nome"], dados["preco"], dados["duracao"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return jsonify({"mensagem": "Serviço cadastrado!", "id": novo_id})

@app.get("/servicos")
def servicos_json():
    conn = get_db()
    servicos = conn.execute("SELECT * FROM servicos").fetchall()
    conn.close()
    lista = [dict(s) for s in servicos]
    return jsonify(lista)

@app.put("/servicos/<int:id>")
def alterar_servico(id):
    dados = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE servicos
        SET nome = ?, preco = ?, duracao = ?
        WHERE id = ?
    """, (dados["nome"], dados["preco"], dados["duracao"], id))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Serviço atualizado!", "id": id})

# API PROFISSIONAIS

@app.post("/profissionais")
def cadastrar_profissional():
    dados = request.json
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO profissionais (nome, especialidade) VALUES (?, ?)",
        (dados["nome"], dados["especialidade"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return jsonify({"mensagem": "Profissional cadastrado!", "id": novo_id})

@app.get("/profissionais")
def listar_profissionais():
    conn = get_db()
    profissionais = conn.execute("SELECT * FROM profissionais").fetchall()
    conn.close()
    lista = [dict(p) for p in profissionais]
    return jsonify(lista)

# API AGENDAMENTOS

@app.post("/agendamentos")
def cadastrar_agendamento():
    dados = request.json
    servico_id = dados["servico_id"]
    profissional_id = dados["profissional_id"]
    data = dados["data"]
    horario = dados["horario"]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO agendamentos (servico_id, profissional_id, data, horario)
        VALUES (?, ?, ?, ?)
    """, (servico_id, profissional_id, data, horario))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    return jsonify({"mensagem": "Agendamento cadastrado!", "id": novo_id})

@app.get("/agendamentos_api")
def listar_agendamentos_api():
    conn = get_db()
    agendamentos = conn.execute("SELECT * FROM agendamentos").fetchall()
    conn.close()
    lista = [dict(a) for a in agendamentos]
    return jsonify(lista)

@app.get("/")
def home():
    return render_template("dashboard.html")


app.run(port=3000)
