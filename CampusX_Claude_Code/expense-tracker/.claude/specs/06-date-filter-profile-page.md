# Spec: Date Filter for Profile Page

## Overview
Step 06 adds a date range filter to the Recent Transactions section of the profile
page. Users can supply an optional "From" and/or "To" date to narrow the displayed
expense list. The filter is submitted as a GET query string so results are bookmarkable
and the browser Back button works correctly. A "Clear" link appears when any filter is
active, letting users return to the unfiltered view in one click. This feature prepares
the profile page for larger datasets before the CRUD steps (7-9) add new expenses.

## Depends on
- Step 01 — database setup (`expenses` table, `get_db()`)
- Step 04 — profile page design (`profile.html`, `profile.css`)
- Step 05 — backend routes for profile page (`get_user_expenses()` must exist)

## Routes
No new routes. `GET /profile` is enhanced with two optional query parameters:

- `date_from` — lower bound, inclusive (`YYYY-MM-DD`). Omit or leave blank to skip.
- `date_to`   — upper bound, inclusive (`YYYY-MM-DD`). Omit or leave blank to skip.

Example: `GET /profile?date_from=2026-06-01&date_to=2026-06-15`

## Database changes
No new tables or columns. `get_user_expenses()` in `database/db.py` gains two optional
parameters:

```python
def get_user_expenses(
    user_id: int,
    date_from: str = None,
    date_to: str = None,
) -> list:
```

When `date_from` is not `None`, append `AND date >= ?` to the base query.
When `date_to` is not `None`, append `AND date <= ?`.
Both clauses may be active simultaneously. Use parameterised query composition — never
f-strings in SQL.

## Templates
- **Modify:** `templates/profile.html`
  - Add a filter form (`method="get"`, `action="{{ url_for('profile') }}"`) inside
    the `.breakdown-header` div of the Recent Transactions card, below the title row.
  - Form contains: From date input, To date input, a Filter submit button, and a
    Clear link (`href="{{ url_for('profile') }}"`) that is only rendered when
    `date_from` or `date_to` is truthy.
  - Inputs must be pre-filled with the current filter values so the form reflects
    active state after submission.

## Files to change
- `database/db.py` — add `date_from` / `date_to` optional params to `get_user_expenses()`
- `app.py` — read `date_from` and `date_to` from `request.args` in `/profile`, pass
  them to `get_user_expenses()` and back to `render_template()`
- `templates/profile.html` — add filter form to the Recent Transactions section
- `static/css/profile.css` — add styles for the filter form elements

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — never f-strings in SQL
- Passwords hashed with werkzeug (unchanged — do not break existing auth)
- Use CSS variables — never hardcode hex values in `profile.css`
- All templates extend `base.html`
- DB logic stays in `database/db.py` — never inline SQL in `app.py`
- Empty string values from `request.args` must be converted to `None` before passing
  to `get_user_expenses()` — do not pass empty strings as SQL parameters
- The filter form must use `method="get"` so results are bookmarkable
- The Clear link must point to `url_for('profile')` with no query params
- Summary stats (total count, total amount, category breakdown) are **not** filtered —
  they always reflect the user's full expense history

## Definition of done
- [ ] `GET /profile` with no query params renders all expenses (unchanged baseline)
- [ ] `GET /profile?date_from=2026-06-01` shows only expenses on or after 2026-06-01
- [ ] `GET /profile?date_to=2026-06-10` shows only expenses on or before 2026-06-10
- [ ] `GET /profile?date_from=2026-06-01&date_to=2026-06-10` shows only expenses in that range (5 rows for the seeded demo user)
- [ ] Filter form inputs are pre-filled with the active filter values after submission
- [ ] Clear link is visible when a filter is active and resets to the full list
- [ ] Clear link is absent when no filter is active
- [ ] Summary stats at the top of the page are unchanged by the filter
- [ ] Visiting `/profile` while logged out still redirects to `/login` (login_required intact)
- [ ] An empty result set due to an out-of-range filter shows the existing empty-state UI
