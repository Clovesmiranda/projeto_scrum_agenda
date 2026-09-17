import sqlite3

conn = sqlite3.connect("dados.db")
cursor = conn.cursor()

# Tabela de serviços (com preço e duração)
cursor.execute("""
CREATE TABLE IF NOT EXISTS servicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    duracao TEXT NOT NULL
);
""")

# Tabela de profissionais (com especialidade)
cursor.execute("""
CREATE TABLE IF NOT EXISTS profissionais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    especialidade TEXT NOT NULL
);
""")

# Tabela de agendamentos
cursor.execute("""
CREATE TABLE IF NOT EXISTS agendamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    servico_id INTEGER NOT NULL,
    profissional_id INTEGER NOT NULL,
    data TEXT NOT NULL,
    horario TEXT NOT NULL,
    FOREIGN KEY (servico_id) REFERENCES servicos(id),
    FOREIGN KEY (profissional_id) REFERENCES profissionais(id)
);
""")

# Dados iniciais de serviços
cursor.execute(
    "INSERT INTO servicos (nome, preco, duracao) VALUES (?, ?, ?)",
    ("Corte de cabelo", 50.0, "30 minutos")
)
cursor.execute(
    "INSERT INTO servicos (nome, preco, duracao) VALUES (?, ?, ?)",
    ("Manicure", 35.0, "45 minutos")
)
cursor.execute(
    "INSERT INTO servicos (nome, preco, duracao) VALUES (?, ?, ?)",
    ("Barba", 25.0, "20 minutos")
)

# Dados iniciais de profissionais
cursor.execute(
    "INSERT INTO profissionais (nome, especialidade) VALUES (?, ?)",
    ("João Silva", "Cabeleireiro")
)
cursor.execute(
    "INSERT INTO profissionais (nome, especialidade) VALUES (?, ?)",
    ("Maria Santos", "Manicure")
)
cursor.execute(
    "INSERT INTO profissionais (nome, especialidade) VALUES (?, ?)",
    ("Carlos Pereira", "Barbeiro")
)

conn.commit()
conn.close()

print("Tabelas criadas e dados inseridos com sucesso!")
