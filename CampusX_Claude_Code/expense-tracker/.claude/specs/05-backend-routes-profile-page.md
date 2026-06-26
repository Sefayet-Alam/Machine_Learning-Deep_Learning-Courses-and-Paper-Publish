# Spec: Backend Routes for Profile Page

## Overview
Step 04 built the profile page's visual design with summary stats (total count, total
amount, category breakdown). Step 05 completes the data layer by adding individual
expense transaction history to the profile view. A new `get_user_expenses()` DB
function fetches the full expense list for a user, the `/profile` route is updated
to pass it to the template, and `profile.html` gains a "Recent Transactions" section
showing each expense row. This makes the profile page a real dashboard before CRUD
operations arrive in steps 7-9.

## Depends on
- Step 01 — database setup (expenses table must exist)
- Step 04 — profile page design (profile.html and profile.css must exist)

## Routes
- `GET /profile` — enhanced (already exists) — fetches expense list in addition to
  summary and passes it to the template — logged-in only

No new routes.

## Database changes
New function in `database/db.py`:

```python
def get_user_expenses(user_id: int) -> list:
    """Return all expenses for a user, newest first."""
```

Query:
```sql
SELECT id, amount, category, date, description
FROM expenses
WHERE user_id = ?
ORDER BY date DESC, created_at DESC
```

Returns a list of `sqlite3.Row` objects (empty list when the user has no expenses).
No schema changes — the `expenses` table already has all required columns.

## Templates
- **Modify:** `templates/profile.html`
  - Add a "Recent Transactions" card below the existing category-breakdown card
  - Table columns: Date | Category chip | Description | Amount
  - Empty state: a single centered message when the list is empty
  - Each row must include the expense `id` as a `data-id` attribute on the `<tr>`
    so future edit/delete steps can target it without a second DB call

## Files to change
- `database/db.py` — add `get_user_expenses()`
- `app.py` — import `get_user_expenses`; pass `expenses` to `render_template` in `/profile`
- `templates/profile.html` — add Recent Transactions section
- `static/css/profile.css` — add styles for the transactions table

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — never f-strings in SQL
- Passwords hashed with werkzeug (unchanged, but do not break existing auth)
- Use CSS variables — never hardcode hex values in `profile.css`
- All templates extend `base.html`
- DB logic stays in `database/db.py` — never inline SQL in `app.py`
- The `/profile` route must still `abort(404)` if `get_user_by_id()` returns `None`
- Category chips in the transactions table must reuse the same CSS classes already
  defined in `profile.css` (e.g. `.cat-food`, `.cat-transport`) — no new colour rules
- Amount column must display the ₹ symbol and two decimal places
- Date column must display in `DD Mon YYYY` format (e.g. `22 Jun 2026`) — format in
  the template with a Jinja2 filter or in the DB function using `strftime`

## Definition of done
- [ ] `pytest` passes with no regressions (all 19 existing tests green)
- [ ] Logged-in as `demo@spendly.com` / `demo123`, `/profile` loads without error
- [ ] Recent Transactions section is visible on the profile page with 8 seeded rows
- [ ] Each row shows the correct date, category chip, description, and amount (₹)
- [ ] Rows are ordered newest-first (most recent date at the top)
- [ ] Registering a brand-new user and visiting `/profile` shows the empty state message
- [ ] Visiting `/profile` while logged out redirects to `/login` (login_required still works)
