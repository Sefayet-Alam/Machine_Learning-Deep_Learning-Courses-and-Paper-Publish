from database.db import get_db


def get_expense_by_id(expense_id, user_id):
    conn = get_db()
    row = conn.execute(
        "SELECT id, amount, category, date, description "
        "FROM expenses WHERE id = ? AND user_id = ?",
        (expense_id, user_id),
    ).fetchone()
    conn.close()
    if row is None:
        return None
    return {
        "id": row["id"],
        "amount": row["amount"],
        "category": row["category"],
        "date": row["date"],
        "description": row["description"] or "",
    }


def insert_expense(user_id, amount, category, expense_date, description):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO expenses (user_id, amount, category, date, description)"
        " VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, category, expense_date, description or None),
    )
    conn.commit()
    expense_id = cursor.lastrowid
    conn.close()
    return expense_id


def update_expense(expense_id, user_id, amount, category, expense_date, description):
    conn = get_db()
    conn.execute(
        "UPDATE expenses SET amount = ?, category = ?, date = ?, description = ? "
        "WHERE id = ? AND user_id = ?",
        (amount, category, expense_date, description or None, expense_id, user_id),
    )
    conn.commit()
    conn.close()


def delete_expense_by_id(expense_id, user_id):
    conn = get_db()
    conn.execute(
        "DELETE FROM expenses WHERE id = ? AND user_id = ?",
        (expense_id, user_id),
    )
    conn.commit()
    conn.close()
