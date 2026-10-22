from flask import Flask, request, render_template_string, sessions
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database=""

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

@app.route('/')
def json_demo():
    return render_template_string(HTML)
