from flask import Flask, redirect, render_template_string, request, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'Forum'



@app.route('/', methods=['GET', 'POST'])
def index():
    username = session.get('username')

    if username:
        return redirect(url_for('createpost'))

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="forum",
    )
    cur = None

    try:
        cur = db.cursor(dictionary=True)
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')

            cur.execute('SELECT * FROM users WHERE username = %s', (username,))
            user = cur.fetchone()

            if not user:
                return "Användare hittades inte.", 404

            db.commit()
            return redirect(url_for('index'))

        cur.execute('SELECT username FROM users')
        posts = cur.fetchall()
    finally:
        if cur is not None:
            cur.close()
        db.close()

    return render_template_string('''
        <h1>Nytt inlägg</h1>
        <form method="POST">
            <input type="text" name="username" placeholder="Användarnamn" required>
            <input type="password" name="password" placeholder="Lösenord" required>
            <button type="submit">Skicka</button>
        </form>
        <h2>Inlägg</h2>
        {% for post in posts %}
            <div class="post"><h2>{{ post["username"] }}</h2><p>{{ post["content"] }}</p></div>
        {% endfor %}
        
    ''', posts=posts)

@app.route('/createpost', methods=['GET', 'POST'])
def createpost():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database="forum",
    )

    cur = None
    if request.method == 'POST':
        content = request.form.get('inlägg', '').strip()

        try:
            cur = db.cursor()
            cur.execute('INSERT INTO posts (inlägg, användernamn) VALUES (%s, %s)', (content, request.form.get('username', '').strip()))
            db.commit()
            return redirect(url_for('index'))
        finally:
            if cur is not None:
                cur.close()
            db.close()


    return render_template_string('''
        <h1>Skapa nytt inlägg</h1>
        <form method="POST">
            <textarea name="inlägg" placeholder="inlägg" required></textarea>
            <button type="submit">Skicka</button>
        </form>
    ''')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
