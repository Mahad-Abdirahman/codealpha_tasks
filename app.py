from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            type TEXT CHECK(type IN ('Income', 'Expense')) NOT NULL,
            description TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM transactions ORDER BY date DESC")
    transactions = c.fetchall()
    income = sum(t[1] for t in transactions if t[2] == 'Income')
    expense = sum(t[1] for t in transactions if t[2] == 'Expense')
    balance = income - expense
    conn.close()
    return render_template('index.html', transactions=transactions, balance=round(balance, 2))

@app.route('/add', methods=['POST'])
def add():
    amount = float(request.form['amount'])
    type_ = request.form['type']
    description = request.form['description']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (amount, type, description, date) VALUES (?, ?, ?, ?)",
              (amount, type_, description, date))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# ✅ Move this ABOVE __main__
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    if request.method == 'POST':
        amount = float(request.form['amount'])
        type_ = request.form['type']
        description = request.form['description']
        c.execute("UPDATE transactions SET amount=?, type=?, description=? WHERE id=?",
                  (amount, type_, description, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    else:
        c.execute("SELECT * FROM transactions WHERE id=?", (id,))
        transaction = c.fetchone()
        conn.close()
        return render_template('edit.html', transaction=transaction)

# ✅ Always keep this LAST
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
