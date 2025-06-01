import sqlite3

conn = sqlite3.connect("alma_paid.db")
c = conn.cursor()
# Agregamos la columna 'description', tipo TEXT, con valor por defecto ''
try:
    c.execute("""ALTER TABLE courses ADD COLUMN description TEXT DEFAULT '';""")
    conn.commit()
    print("✅ Columna 'description' agregada correctamente en 'courses'.")
except sqlite3.OperationalError as e:
    print("⚠️ No se pudo agregar la columna (quizás ya existe):", e)
finally:
    conn.close()
