import sqlite3

conn = sqlite3.connect("dados.db")
print("SERVICOS:", conn.execute("PRAGMA table_info(servicos)").fetchall())
print("PROFISSIONAIS:", conn.execute("PRAGMA table_info(profissionais)").fetchall())
print("AGENDAMENTOS:", conn.execute("PRAGMA table_info(agendamentos)").fetchall())
conn.close()
