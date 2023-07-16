from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/codewithme', methods=['GET', 'POST'])
def codewithme():
    if request.method == 'POST':
        problem_name = request.form['problem_name']
        problem_description = request.form['problem_description']
        code = request.form['code']
        category = request.form['category']
        conn = sqlite3.connect('coding_problems.db')
        c = conn.cursor()
        c.execute("INSERT INTO problems (problem_name, problem_description, code, category) VALUES (?, ?, ?, ?)",
                  (problem_name, problem_description, code, category))
        conn.commit()
        conn.close()
        return redirect('/codewithme')

    conn = sqlite3.connect('coding_problems.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT category FROM problems")
    categories = c.fetchall()
    c.execute("SELECT * FROM problems")
    problems = c.fetchall()
    conn.close()

    return render_template('codewithme.html', problems=problems, categories=categories)

@app.route('/delete/<int:problem_id>', methods=['POST'])
def delete(problem_id):
    conn = sqlite3.connect('coding_problems.db')
    c = conn.cursor()
    c.execute("DELETE FROM problems WHERE id = ?", (problem_id,))
    conn.commit()
    conn.close()

    return redirect('/codewithme')

@app.route('/viewcode')
def viewcode():
    conn = sqlite3.connect('coding_problems.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT category FROM problems")
    categories = c.fetchall()
    c.execute("SELECT * FROM problems")
    problems = c.fetchall()
    conn.close()

    return render_template('viewcode.html', problems=problems, categories=categories)

@app.route('/viewcode/<category_filter>')
def viewcode_category(category_filter):
    conn = sqlite3.connect('coding_problems.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT category FROM problems")
    categories = c.fetchall()
    c.execute("SELECT * FROM problems")
    problems = c.fetchall()
    conn.close()

    return render_template('viewcode.html', problems=problems, categories=categories, category_filter=category_filter)

if __name__ == '__main__':
    app.run(debug=True)
