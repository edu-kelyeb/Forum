from flask import Flask, redirect, render_template_string, request, url_for
import mysql.connector
from werkzeug.security import generate_password_hash

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
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
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            return redirect(url_for('index'))

        cur.execute('SELECT name, text FROM posts ORDER BY id DESC')
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
            <div class="post"><h2>{{ post["name"] }}</h2><p>{{ post["text"] }}</p></div>
        {% endfor %}
        
    ''', posts=posts)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
