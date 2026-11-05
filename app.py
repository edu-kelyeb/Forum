from webbrowser import get

from flask import Flask, request, render_template_string, sessions
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",

    password="",
    database="forum"
)

app = Flask(__name__)
JSON_FILE = 'data.json'

def load_posts():
    if not os.path.exists(JSON_FILE):
        return[]
    try:
        with open(JSON_FILE, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return[]

@app.route('/', methods=['GET', 'POST'])
def json_demo():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = db.cursor()
        cur = conn.cursor()
        cur.execute(" insert into users (username, password) values (%s, %s)", (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('json_demo'))
    conn = get_db()
    cur = conn.cursor(dictornary=True)
    cur.execute('SELECT name,text FROM posts ORDER BY id DESC')
    posts = cur.fetchall()
    conn.close()

    rows = ''.join()


    








    return render_template_string(HTML)
