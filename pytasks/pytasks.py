import sqlite3 as sql
from contextlib import closing
import datetime


from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash



PYTASKS_SETTINGS = "settings"


app = Flask(__name__)
app.config.from_object(PYTASKS_SETTINGS)


def connect_db():
	return sql.connect(app.config["DATABASE"])


def init_db():
	with closing(connect_db()) as db:
		with app.open_resource("schema.sql", mode="r") as f:
			db.cursor().executescript(f.read())
		db.commit()


@app.before_request
def before_request():
	g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
	db = getattr(g, "db", None)
	if db is not None:
		db.close()


@app.route("/")
def show_tasks():
	cur = g.db.execute("SELECT title, description FROM tasks ORDER BY ID")
	tasks = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
	return render_template("show_tasks.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
	title = request.form["title"]
	description = request.form["description"]
	dt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S:%f")
	g.db.execute("INSERT INTO tasks (title, description, date_of_creation) values (?, ?, ?)",
		[title, description, dt])
	g.db.commit()
	return redirect(url_for("show_tasks"))


if __name__ == "__main__":
	app.run()
