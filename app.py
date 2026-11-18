from flask import Flask, redirect, render_template_string, request, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash

db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="forum",
    )



app = Flask(__name__)
app.secret_key = 'Forum'

@app.route('/')
def home():
    username = session.get('username')
    if username:
        return f'Välkommen, {username}! <a href="/createpost">Skapa inlägg</a> | <a href="/logout">Logga ut</a>'
    return 'Välkommen! <a href="/login">Logga in</a> | <a href="/register">Registrera</a>'

@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute('SELECT username, password FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and user[1] == password:
            session['username'] = username
            return redirect(url_for('index'))
        return 'Felaktigt användarnamn eller lösenord. <a href="/">Försök igen</a>'

    return '''
        <h1>Inloggning</h1>
        <form method="POST">
            <input type="text" name="username" placeholder="Användarnamn" required>
            <input type="password" name="password" placeholder="Lösenord" required>
            <input type="submit" value="Logga in">
        </form>
        '''

@app.route('/createpost', methods=['GET', 'POST'])
def createpost():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        database="forum",
    )

    cur = None
    if request.method == 'POST':
        username = session.get('username')
        if not username:
            return redirect(url_for('index'))
        content = request.form.get('inlägg', '').strip()

        try:
            cur = db.cursor()
            cur.execute('INSERT INTO posts (inlägg, användernamn) VALUES (%s, %s)', (content, username))
            db.commit()
            return redirect(url_for('createposts'))
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
