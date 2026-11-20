import sqlite3
import csv
import io
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura_gastos'
DATABASE = 'gastos.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            monto REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'usuario' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        if usuario == 'admin' and clave == '123':
            session['usuario'] = usuario
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas. Intenta nuevamente.', 'danger')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    if request.method == 'POST':
        fecha = request.form['fecha']
        descripcion = request.form['descripcion']
        monto = float(request.form['monto'])
        
        conn.execute('INSERT INTO gastos (fecha, descripcion, monto) VALUES (?, ?, ?)',
                     (fecha, descripcion, monto))
        conn.commit()
        flash('Gasto registrado correctamente.', 'success')
        return redirect(url_for('dashboard'))
        
    gastos = conn.execute('SELECT * FROM gastos ORDER BY fecha DESC, id DESC').fetchall()
    total = sum(g['monto'] for g in gastos)
    conn.close()
    return render_template('dashboard.html', gastos=gastos, total=total)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM gastos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Registro eliminado.', 'warning')
    return redirect(url_for('dashboard'))

@app.route('/reporte')
def reporte():
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    gastos = conn.execute('SELECT * FROM gastos ORDER BY fecha DESC').fetchall()
    conn.close()
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Fecha', 'Descripcion', 'Monto (S/.)'])
    total = 0
    for g in gastos:
        cw.writerow([g['id'], g['fecha'], g['descripcion'], f"{g['monto']:.2f}"])
        total += g['monto']
    cw.writerow(['', '', 'TOTAL GENERAL', f"{total:.2f}"])
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=reporte_gastos.csv"
    output.headers["Content-type"] = "text/csv; charset=utf-8"
    return output

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)