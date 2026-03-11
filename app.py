from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

create_table()

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("students.db")
        cur = conn.cursor()

        cur.execute(
        "INSERT INTO students(name,email,password) VALUES(?,?,?)",
        (name,email,password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("students.db")
        cur = conn.cursor()

        cur.execute(
        "SELECT * FROM students WHERE email=? AND password=?",
        (email,password))

        user = cur.fetchone()

        conn.close()

        if user:
            return redirect("/dashboard")
        else:
            return "Invalid Login"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

app.run(host="0.0.0.0", port=5000)