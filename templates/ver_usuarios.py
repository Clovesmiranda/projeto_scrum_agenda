import sqlite3

conn = sqlite3.connect("dados.db")
cursor = conn.cursor()

# Cria a tabela caso ainda não exista
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    senha TEXT NOT NULL,
    perfil TEXT NOT NULL
)
""")
conn.commit()

# Verifica se já existe algum usuário
usuarios = cursor.execute("SELECT * FROM usuarios").fetchall()

if not usuarios:
    print("\n[AVISO] Nenhum usuário encontrado. Criando usuário padrão...")
    cursor.execute(
        "INSERT INTO usuarios (usuario, senha, perfil) VALUES (?, ?, ?)",
        ("admin", "123456", "gerente")
    )
    conn.commit()
    print("-> Usuário criado com sucesso!")
    print("   Usuário: admin")
    print("   Senha: 123456")
    print("   Perfil: gerente\n")
else:
    print("\n--- USUÁRIOS JÁ CADASTRADOS ---")
    for u in usuarios:
        print(f"ID: {u[0]} | Usuário: {u[1]} | Senha: {u[2]} | Perfil: {u[3]}")
    print("--------------------------------\n")

conn.close()
