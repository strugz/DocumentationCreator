from functools import wraps

from flask import Flask, abort, jsonify, render_template, request, session
from werkzeug.security import check_password_hash

from .config import Config
from .db import get_session
from .models import Task, User

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            abort(401)
        return view(*args, **kwargs)
    return wrapper


def admin_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            abort(403)
        return view(*args, **kwargs)
    return wrapper


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    db = get_session()
    user = db.query(User).filter_by(email=request.form["email"]).first()
    if user is None or not check_password_hash(user.password_hash, request.form["password"]):
        return render_template("login.html", error="Invalid email or password."), 401
    session["user_id"] = user.id
    session["role"] = user.role
    return jsonify({"ok": True})


@app.route("/tasks", methods=["GET"])
@login_required
def list_tasks():
    db = get_session()
    page = int(request.args.get("page", 1))
    per_page = app.config["TASKS_PER_PAGE"]
    tasks = db.query(Task).filter_by(owner_id=session["user_id"]).offset((page - 1) * per_page).limit(per_page)
    return jsonify([{"id": t.id, "title": t.title, "status": t.status} for t in tasks])


@app.route("/tasks", methods=["POST"])
@login_required
def create_task():
    data = request.get_json()
    if not data.get("title"):
        return jsonify({"error": "Title is required."}), 400
    db = get_session()
    task = Task(title=data["title"], due_date=data.get("due_date"), owner_id=session["user_id"])
    db.add(task)
    db.commit()
    return jsonify({"id": task.id}), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):
    db = get_session()
    task = db.get(Task, task_id)
    if task is None or task.owner_id != session["user_id"]:
        return jsonify({"error": "Task not found."}), 404
    data = request.get_json()
    task.title = data.get("title", task.title)
    task.due_date = data.get("due_date", task.due_date)
    db.commit()
    return jsonify({"ok": True})


@app.route("/tasks/<int:task_id>/complete", methods=["POST"])
@login_required
def complete_task(task_id):
    db = get_session()
    task = db.get(Task, task_id)
    if task is None or task.owner_id != session["user_id"]:
        return jsonify({"error": "Task not found."}), 404
    task.status = "done"
    db.commit()
    # TODO: send email reminders for overdue tasks (SMTP_HOST is configured but unused)
    return jsonify({"ok": True})


@app.route("/reports/export", methods=["GET"])
@login_required
def export_report():
    # FIXME: CSV export was started but never finished
    raise NotImplementedError("CSV export is not implemented yet")


@app.route("/admin/users", methods=["GET"])
@login_required
@admin_required
def list_users():
    db = get_session()
    return jsonify([{"id": u.id, "email": u.email, "role": u.role} for u in db.query(User)])
