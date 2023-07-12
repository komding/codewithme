#a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p
from flask import Flask, render_template, request, redirect, session, send_file, make_response
import sqlite3
#from docx import Document
import io 


app = Flask(__name__)
app.secret_key = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p'

def create_table():
    conn = sqlite3.connect('coding_problems.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT,
                 password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS problems
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             problem_name TEXT,
             problem_description TEXT,
             code TEXT,
             category TEXT)''')

    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('coding_problems.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('coding_problems.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['username'] = username
            return redirect('/codewithme')
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@app.route('/codewithme', methods=['GET', 'POST'])
def codewithme():
    if 'username' not in session:
        return redirect('/login')

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
    c.execute("SELECT DISTINCT category FROM problems")  # Retrieve distinct categories from the database
    categories = c.fetchall()
    c.execute("SELECT * FROM problems")
    problems = c.fetchall()
    conn.close()

    return render_template('codewithme.html', problems=problems, categories=categories)



@app.route('/delete/<int:problem_id>', methods=['POST'])
def delete(problem_id):
    if 'username' not in session:
        return redirect('/login')

    conn = sqlite3.connect('coding_problems.db')
    c = conn.cursor()
    c.execute("DELETE FROM problems WHERE id = ?", (problem_id,))
    conn.commit()
    conn.close()

    return redirect('/codewithme')


@app.route('/viewcode')
def viewcode():
    if 'username' not in session:
        return redirect('/login')

    conn = sqlite3.connect('coding_problems.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT category FROM problems")  # Retrieve distinct categories from the database
    categories = c.fetchall()
    c.execute("SELECT * FROM problems")
    problems = c.fetchall()
    conn.close()

    return render_template('viewcode.html', problems=problems, categories=categories)

@app.route('/viewcode/<category_filter>')
def viewcode_category(category_filter):
    if 'username' not in session:
        return redirect('/login')

    conn = sqlite3.connect('coding_problems.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT category FROM problems")
    categories = c.fetchall()
    c.execute("SELECT * FROM problems")
    problems = c.fetchall()
    conn.close()

    return render_template('viewcode.html', problems=problems, categories=categories, category_filter=category_filter)

'''
@app.route('/download/docx', methods=['POST'])
def download_docx():
    conn = sqlite3.connect('coding_problems.db')
    c = conn.cursor()
    # Retrieve coding problems from the database
    c.execute("SELECT * FROM problems")
    problems = c.fetchall()
    conn.close()

    # Create a new document
    doc = Document()
    doc.add_heading('View Code - Coding Problems', level=1)

    # Iterate over the coding problems and add them to the document
    for problem in problems:
        problem_name = problem[1]
        problem_description = problem[2]
        code = problem[3]

        doc.add_heading(problem_name, level=2)
        doc.add_paragraph(problem_description)
        doc.add_paragraph(code)

    # Save the document to a BytesIO object
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)

    # Create a response with the BytesIO object
    response = make_response(doc_io.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=coding_problems.docx'
    response.headers['Content-type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    return response
'''


if __name__ == '__main__':
    create_table()
    app.run(debug=True)
