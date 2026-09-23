from flask import Flask, render_template, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('gastos.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla si no existe
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            hora TEXT,
            descripcion TEXT,
            monto REAL,
            tipo TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/movimientos', methods=['GET', 'POST'])
def gestionar_movimientos():
    conn = get_db_connection()
    
    if request.method == 'POST':
        nuevo = request.json
        conn.execute('INSERT INTO movimientos (fecha, hora, descripcion, monto, tipo) VALUES (?, ?, ?, ?, ?)',
                     (nuevo['fecha'], nuevo['hora'], nuevo['descripcion'], nuevo['monto'], nuevo['tipo']))
        conn.commit()
        conn.close()
        return jsonify({"status": "ok"}), 201

    elif request.method == 'GET':
        movimientos = conn.execute('SELECT * FROM movimientos ORDER BY id DESC').fetchall()
        conn.close()
        return jsonify([dict(ix) for ix in movimientos])

@app.route('/api/movimientos/<int:id>', methods=['DELETE'])
def eliminar_movimiento(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM movimientos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "eliminado"}), 200

if __name__ == '__main__':
    init_db()
    # 0.0.0.0 permite que Tailscale exponga el puerto
    app.run(host='0.0.0.0', port=5000)