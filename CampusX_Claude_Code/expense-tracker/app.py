from functools import wraps
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from werkzeug.security import check_password_hash
from database.db import get_db, init_db, seed_db, register_user, get_user_by_email, \
    get_user_by_id, get_expense_summary, get_user_expenses
from database.queries import (
    get_expense_by_id,
    insert_expense,
    update_expense,
    delete_expense_by_id,
)
import sqlite3

app = Flask(__name__)

CATEGORIES = [
    "Food",
    "Transport",
    "Bills",
    "Health",
    "Entertainment",
    "Shopping",
    "Other",
]


def _parse_date(val):
    try:
        datetime.strptime(val, "%Y-%m-%d")
        return val
    except (ValueError, TypeError):
        return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to access that page.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function
app.secret_key = "dev-secret-change-in-production"


@app.template_filter("fmt_date")
def fmt_date(value):
    from datetime import datetime
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%d %b %Y")
    except (ValueError, TypeError):
        return value


@app.template_filter("fmt_month_year")
def fmt_month_year(value):
    from datetime import datetime
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d").strftime("%B %Y")
    except (ValueError, TypeError):
        return value[:10]


with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name             = request.form.get("name", "").strip()
    email            = request.form.get("email", "").strip().lower()
    password         = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name or not email or not password or not confirm_password:
        flash("All fields are required.", "error")
        return render_template("register.html", name=name, email=email)

    if len(password) < 8:
        flash("Password must be at least 8 characters.", "error")
        return render_template("register.html", name=name, email=email)

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return render_template("register.html", name=name, email=email)

    try:
        user_id = register_user(name, email, password)
    except sqlite3.IntegrityError:
        flash("An account with that email already exists.", "error")
        return render_template("register.html", name=name, email=email)

    session["user_id"] = user_id
    flash("Account created successfully! Please log in.", "success")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("login.html", error="Email and password are required.")

    user = get_user_by_email(email)

    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.")

    session.clear()
    session["user_id"]   = user["id"]
    session["user_name"] = user["name"]

    flash("Welcome back, {}!".format(user["name"]), "success")
    return redirect(url_for("landing"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "success")
    return redirect(url_for("landing"))


@app.route("/profile")
@login_required
def profile():
    from datetime import date, timedelta

    user_id = session["user_id"]
    user    = get_user_by_id(user_id)
    if user is None:
        abort(404)

    preset    = request.args.get("preset", "").strip()
    date_from = request.args.get("date_from", "").strip()
    date_to   = request.args.get("date_to", "").strip()

    today = date.today()

    if preset == "this_month":
        date_from = today.replace(day=1).isoformat()
        date_to   = today.isoformat()
    elif preset == "last_3_months":
        date_from = (today - timedelta(days=90)).isoformat()
        date_to   = today.isoformat()
    elif preset == "last_6_months":
        date_from = (today - timedelta(days=180)).isoformat()
        date_to   = today.isoformat()
    elif preset == "all":
        date_from = ""
        date_to   = ""

    summary  = get_expense_summary(user_id, date_from or None, date_to or None)
    expenses = get_user_expenses(user_id, date_from or None, date_to or None)

    return render_template(
        "profile.html",
        name          = user["name"],
        email         = user["email"],
        created_at    = user["created_at"],
        summary       = summary,
        expenses      = expenses,
        date_from     = date_from,
        date_to       = date_to,
        active_preset = preset,
    )


@app.route("/expenses/add", methods=["GET", "POST"])
@login_required
def add_expense():
    today = datetime.today().strftime("%Y-%m-%d")

    if request.method == "POST":
        amount_raw  = request.form.get("amount", "").strip()
        category    = request.form.get("category", "").strip()
        expense_date = request.form.get("date", "").strip()
        description = request.form.get("description", "").strip()

        try:
            amount = float(amount_raw)
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash("Amount must be a positive number.", "error")
            return render_template("add_expense.html", categories=CATEGORIES, form=request.form, today=today)

        if category not in CATEGORIES:
            flash("Please select a valid category.", "error")
            return render_template("add_expense.html", categories=CATEGORIES, form=request.form, today=today)

        if not _parse_date(expense_date):
            flash("Please enter a valid date.", "error")
            return render_template("add_expense.html", categories=CATEGORIES, form=request.form, today=today)

        insert_expense(session["user_id"], amount, category, expense_date, description)
        flash("Expense added.", "success")
        return redirect(url_for("profile"))

    return render_template("add_expense.html", categories=CATEGORIES, form={}, today=today)


@app.route("/expenses/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_expense(id):
    expense = get_expense_by_id(id, session["user_id"])
    if expense is None:
        abort(404)

    if request.method == "GET":
        return render_template("edit_expense.html", expense=expense, categories=CATEGORIES, form={})

    amount_raw   = request.form.get("amount", "").strip()
    category     = request.form.get("category", "").strip()
    expense_date = request.form.get("date", "").strip()
    description  = request.form.get("description", "").strip()

    try:
        amount = float(amount_raw)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("Amount must be a positive number.", "error")
        return render_template("edit_expense.html", expense=expense, categories=CATEGORIES, form=request.form)

    if category not in CATEGORIES:
        flash("Please select a valid category.", "error")
        return render_template("edit_expense.html", expense=expense, categories=CATEGORIES, form=request.form)

    if not _parse_date(expense_date):
        flash("Please enter a valid date.", "error")
        return render_template("edit_expense.html", expense=expense, categories=CATEGORIES, form=request.form)

    update_expense(id, session["user_id"], amount, category, expense_date, description)
    flash("Expense updated.", "success")
    return redirect(url_for("profile"))


@app.route("/expenses/<int:id>/delete", methods=["POST"])
@login_required
def delete_expense(id):
    expense = get_expense_by_id(id, session["user_id"])
    if expense is None:
        abort(404)
    delete_expense_by_id(id, session["user_id"])
    flash("Expense deleted.", "success")
    return redirect(url_for("profile"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
