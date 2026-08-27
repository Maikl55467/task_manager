from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        priority BOOLEAN DEFAULT FALSE, status TEXT DEFAULT 'pending', date TEXT DEFAULT CURRENT_DATETIME,
                          time TEXT DEFAULT CURRENT_TIMESTAMP
                    )''')
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add-task", methods=["POST"])
def add_task():
    title = request.form["title"]
    description = request.form["description"]
    status = request.form["status"]
    priority = request.form.get("priority")
    date = request.form["date"]
    time = request.form["time"]

    conn = get_db_connection()

    conn.execute("INSERT INTO tasks (title, description, priority, status, date, time) VALUES (?, ?, ?, ?, ?, ?)",
                 (title, description, priority, status, date, time))
    
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form.get("priority")
        status = request.form["status"]
        date = request.form["date"]
        time = request.form["time"]

        conn.execute("UPDATE tasks SET title = ?, description = ?, priority = ?, status = ?, date = ?, time = ? WHERE id = ?",
                     (title, description, priority, status, date, time, task_id))
        conn.commit()
        conn.close()

        return redirect("/")

    conn.close()
    return render_template("edit.html", task=task)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)