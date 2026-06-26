import sqlite3
import os
from werkzeug.security import generate_password_hash


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'spendly.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def register_user(name, email, password):
    password_hash = generate_password_hash(password)
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def get_user_by_email(email: str):
    conn = get_db()
    try:
        return conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
    finally:
        conn.close()


def get_user_by_id(user_id: int):
    conn = get_db()
    try:
        return conn.execute(
            "SELECT id, name, email, created_at FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
    finally:
        conn.close()


def get_expense_summary(user_id: int, date_from: str = None, date_to: str = None) -> dict:
    conn = get_db()
    try:
        where = "WHERE user_id = ?"
        params = [user_id]
        if date_from:
            where += " AND date >= ?"
            params.append(date_from)
        if date_to:
            where += " AND date <= ?"
            params.append(date_to)

        row = conn.execute(
            "SELECT COUNT(*) AS total_count, COALESCE(SUM(amount), 0.0) AS total_amount "
            "FROM expenses " + where,
            params
        ).fetchone()
        breakdown = conn.execute(
            "SELECT category, COUNT(*) AS count, SUM(amount) AS total "
            "FROM expenses " + where + " GROUP BY category ORDER BY total DESC",
            params
        ).fetchall()
        top_category = breakdown[0]["category"] if breakdown else None
        return {
            "total_count":        row["total_count"],
            "total_amount":       row["total_amount"],
            "top_category":       top_category,
            "category_breakdown": breakdown,
        }
    finally:
        conn.close()


def get_user_expenses(user_id: int, date_from: str = None, date_to: str = None) -> list:
    conn = get_db()
    try:
        query = (
            "SELECT id, amount, category, date, description "
            "FROM expenses WHERE user_id = ?"
        )
        params = [user_id]
        if date_from:
            query += " AND date >= ?"
            params.append(date_from)
        if date_to:
            query += " AND date <= ?"
            params.append(date_to)
        query += " ORDER BY date DESC, created_at DESC"
        return conn.execute(query, params).fetchall()
    finally:
        conn.close()


def seed_db():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count > 0:
        conn.close()
        return

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cursor.lastrowid

    sample_expenses = [
        (user_id, 450.00,  "Food",          "2026-06-01", "Grocery run"),
        (user_id, 120.00,  "Transport",     "2026-06-03", "Metro card top-up"),
        (user_id, 1200.00, "Bills",         "2026-06-05", "Electricity bill"),
        (user_id, 800.00,  "Health",        "2026-06-08", "Pharmacy"),
        (user_id, 350.00,  "Entertainment", "2026-06-10", "Movie tickets"),
        (user_id, 2200.00, "Shopping",      "2026-06-14", "New shoes"),
        (user_id, 60.00,   "Other",         "2026-06-18", "Parking fee"),
        (user_id, 380.00,  "Food",          "2026-06-22", "Restaurant dinner"),
    ]

    cursor.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        sample_expenses,
    )
    conn.commit()
    conn.close()
