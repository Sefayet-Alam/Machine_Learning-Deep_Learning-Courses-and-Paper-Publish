"""
Tests for Spec Step 06: Date Filter on Profile Page.

Spec: .claude/specs/06-date-filter-profile-page.md

Definition of Done coverage (DoD numbers used in comments):
  DoD 1 — GET /profile with no params renders all expenses
  DoD 2 — date_from only: expenses on/after that date
  DoD 3 — date_to only: expenses on/before that date
  DoD 4 — date_from + date_to together: only expenses in range
  DoD 5 — Filter form inputs pre-filled with active filter values
  DoD 6 — Clear link visible when a filter is active
  DoD 7 — Clear link absent when no filter is active
  DoD 8 — Summary stats unaffected by date filter (always full history)
  DoD 9 — Unauthenticated /profile redirects to /login (login_required intact)
  DoD 10 — Empty result set from out-of-range filter shows empty-state UI
"""

import pytest
from database.db import get_db


# ------------------------------------------------------------------ #
# Shared test data                                                     #
# ------------------------------------------------------------------ #

VALID_USER = {
    "name": "Filter Tester",
    "email": "filter@example.com",
    "password": "password123",
    "confirm_password": "password123",
}

# Five expenses placed at distinct dates so each boundary test is unambiguous.
# Amount total: 100 + 200 + 300 + 400 + 500 = 1500.00
SEED_EXPENSES = [
    # (amount, category, date, description)
    (100.00, "Food",          "2026-05-31", "Before range"),
    (200.00, "Transport",     "2026-06-01", "On date_from boundary"),
    (300.00, "Bills",         "2026-06-05", "Mid range"),
    (400.00, "Health",        "2026-06-10", "On date_to boundary"),
    (500.00, "Entertainment", "2026-06-15", "After partial range"),
]


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def _register(client, **overrides):
    data = {**VALID_USER, **overrides}
    return client.post("/register", data=data)


# ------------------------------------------------------------------ #
# Fixtures                                                            #
# ------------------------------------------------------------------ #

@pytest.fixture
def auth_client(client):
    """Register a test user (auto-logs in via the register route) and seed
    five expenses spread across distinct dates for boundary testing."""
    _register(client)

    # The register route sets user_id in session automatically.
    with client.session_transaction() as sess:
        user_id = sess["user_id"]

    conn = get_db()
    try:
        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) "
            "VALUES (?, ?, ?, ?, ?)",
            [(user_id, amt, cat, dt, desc) for amt, cat, dt, desc in SEED_EXPENSES],
        )
        conn.commit()
    finally:
        conn.close()

    return client


# ------------------------------------------------------------------ #
# DoD 9: Authentication guard                                          #
# ------------------------------------------------------------------ #

def test_profile_unauthenticated_redirects_to_login(client):
    """GET /profile while logged out must redirect to /login (login_required intact)."""
    response = client.get("/profile")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_profile_unauthenticated_with_date_params_redirects_to_login(client):
    """Auth guard must apply even when date query params are supplied."""
    response = client.get("/profile?date_from=2026-06-01&date_to=2026-06-10")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


# ------------------------------------------------------------------ #
# DoD 1: No query params → all expenses                               #
# ------------------------------------------------------------------ #

def test_profile_no_filter_returns_200(auth_client):
    """GET /profile with no query params responds 200 OK."""
    response = auth_client.get("/profile")
    assert response.status_code == 200


def test_profile_no_filter_shows_all_expenses(auth_client):
    """GET /profile with no params renders every seeded expense description."""
    response = auth_client.get("/profile")
    assert response.status_code == 200
    for _, _, _, description in SEED_EXPENSES:
        assert description.encode() in response.data, (
            f"Expected '{description}' in unfiltered profile but it was missing."
        )


# ------------------------------------------------------------------ #
# DoD 2: date_from only                                               #
# ------------------------------------------------------------------ #

def test_profile_date_from_excludes_expenses_before_boundary(auth_client):
    """GET /profile?date_from=2026-06-01 must not show the 2026-05-31 expense."""
    response = auth_client.get("/profile?date_from=2026-06-01")
    assert response.status_code == 200
    assert b"Before range" not in response.data  # dated 2026-05-31


def test_profile_date_from_is_inclusive_at_boundary(auth_client):
    """date_from filter is inclusive — the expense exactly on date_from must appear."""
    response = auth_client.get("/profile?date_from=2026-06-01")
    assert response.status_code == 200
    assert b"On date_from boundary" in response.data  # dated 2026-06-01


def test_profile_date_from_retains_all_later_expenses(auth_client):
    """All expenses dated after date_from must still be visible."""
    response = auth_client.get("/profile?date_from=2026-06-01")
    assert response.status_code == 200
    assert b"Mid range" in response.data            # 2026-06-05
    assert b"On date_to boundary" in response.data  # 2026-06-10
    assert b"After partial range" in response.data  # 2026-06-15


# ------------------------------------------------------------------ #
# DoD 3: date_to only                                                 #
# ------------------------------------------------------------------ #

def test_profile_date_to_excludes_expenses_after_boundary(auth_client):
    """GET /profile?date_to=2026-06-10 must not show the 2026-06-15 expense."""
    response = auth_client.get("/profile?date_to=2026-06-10")
    assert response.status_code == 200
    assert b"After partial range" not in response.data  # dated 2026-06-15


def test_profile_date_to_is_inclusive_at_boundary(auth_client):
    """date_to filter is inclusive — the expense exactly on date_to must appear."""
    response = auth_client.get("/profile?date_to=2026-06-10")
    assert response.status_code == 200
    assert b"On date_to boundary" in response.data  # dated 2026-06-10


def test_profile_date_to_retains_all_earlier_expenses(auth_client):
    """All expenses dated before date_to must still be visible."""
    response = auth_client.get("/profile?date_to=2026-06-10")
    assert response.status_code == 200
    assert b"Before range" in response.data           # 2026-05-31
    assert b"On date_from boundary" in response.data  # 2026-06-01
    assert b"Mid range" in response.data              # 2026-06-05


# ------------------------------------------------------------------ #
# DoD 4: date_from + date_to together                                  #
# ------------------------------------------------------------------ #

def test_profile_date_range_includes_expenses_within_window(auth_client):
    """GET /profile?date_from=2026-06-01&date_to=2026-06-10 shows all in-range rows."""
    response = auth_client.get("/profile?date_from=2026-06-01&date_to=2026-06-10")
    assert response.status_code == 200
    assert b"On date_from boundary" in response.data  # 2026-06-01 in range
    assert b"Mid range" in response.data              # 2026-06-05 in range
    assert b"On date_to boundary" in response.data    # 2026-06-10 in range


def test_profile_date_range_excludes_expenses_outside_window(auth_client):
    """The same range filter must exclude expenses that fall outside the window."""
    response = auth_client.get("/profile?date_from=2026-06-01&date_to=2026-06-10")
    assert response.status_code == 200
    assert b"Before range" not in response.data        # 2026-05-31 excluded
    assert b"After partial range" not in response.data  # 2026-06-15 excluded


# ------------------------------------------------------------------ #
# DoD 10: Empty result set                                             #
# ------------------------------------------------------------------ #

def test_profile_out_of_range_filter_returns_200(auth_client):
    """A filter that matches no rows must still return HTTP 200 (no crash)."""
    response = auth_client.get("/profile?date_from=2030-01-01&date_to=2030-12-31")
    assert response.status_code == 200


def test_profile_out_of_range_filter_shows_no_expense_rows(auth_client):
    """A filter that matches no rows must show none of the seeded expense descriptions."""
    response = auth_client.get("/profile?date_from=2030-01-01&date_to=2030-12-31")
    assert response.status_code == 200
    for _, _, _, description in SEED_EXPENSES:
        assert description.encode() not in response.data, (
            f"'{description}' should not appear in an out-of-range filtered view."
        )


def test_profile_inverted_range_returns_200_with_no_expenses(auth_client):
    """When date_from is after date_to, no expense can match; page still renders 200.

    Spec requires parameterised query composition: the SQL appends both clauses
    as-is (AND date >= ? AND date <= ?). An inverted range produces no results
    rather than an error.
    """
    response = auth_client.get("/profile?date_from=2026-06-10&date_to=2026-06-01")
    assert response.status_code == 200
    assert b"Mid range" not in response.data


# ------------------------------------------------------------------ #
# DoD 5: Form inputs pre-filled with active filter values              #
# ------------------------------------------------------------------ #

def test_profile_form_prefilled_with_date_from(auth_client):
    """After submitting date_from, the rendered form must show that value in the input."""
    response = auth_client.get("/profile?date_from=2026-06-01")
    assert response.status_code == 200
    assert b"2026-06-01" in response.data


def test_profile_form_prefilled_with_date_to(auth_client):
    """After submitting date_to, the rendered form must show that value in the input."""
    response = auth_client.get("/profile?date_to=2026-06-10")
    assert response.status_code == 200
    assert b"2026-06-10" in response.data


def test_profile_form_prefilled_with_both_dates(auth_client):
    """Both date inputs must reflect their active values after a joint filter submission."""
    response = auth_client.get("/profile?date_from=2026-06-01&date_to=2026-06-10")
    assert response.status_code == 200
    assert b"2026-06-01" in response.data
    assert b"2026-06-10" in response.data


# ------------------------------------------------------------------ #
# DoD 6: Clear link visible when a filter is active                    #
# ------------------------------------------------------------------ #

def test_profile_clear_link_present_when_date_from_active(auth_client):
    """The Clear link must be rendered when date_from is supplied."""
    response = auth_client.get("/profile?date_from=2026-06-01")
    assert response.status_code == 200
    assert b"Clear" in response.data


def test_profile_clear_link_present_when_date_to_active(auth_client):
    """The Clear link must be rendered when date_to is supplied."""
    response = auth_client.get("/profile?date_to=2026-06-10")
    assert response.status_code == 200
    assert b"Clear" in response.data


def test_profile_clear_link_present_when_both_filters_active(auth_client):
    """The Clear link must be rendered when both date_from and date_to are supplied."""
    response = auth_client.get("/profile?date_from=2026-06-01&date_to=2026-06-10")
    assert response.status_code == 200
    assert b"Clear" in response.data


def test_profile_clear_link_points_to_profile_with_no_params(auth_client):
    """The Clear link must point to /profile (no query params) to reset the filter.

    Spec: 'href=\"{{ url_for(\'profile\') }}\"' with no query params.
    """
    response = auth_client.get("/profile?date_from=2026-06-01")
    assert response.status_code == 200
    assert b'href="/profile"' in response.data


# ------------------------------------------------------------------ #
# DoD 7: Clear link absent when no filter is active                    #
# ------------------------------------------------------------------ #

def test_profile_clear_link_absent_when_no_filter(auth_client):
    """The Clear link must NOT be rendered when no date filter is active."""
    response = auth_client.get("/profile")
    assert response.status_code == 200
    assert b"Clear" not in response.data


def test_profile_clear_link_absent_when_empty_string_params(auth_client):
    """Empty string query params (date_from=&date_to=) must be treated as no filter.

    Spec rule: empty string values from request.args must be converted to None
    before passing to get_user_expenses(). The Clear link must not appear.
    """
    response = auth_client.get("/profile?date_from=&date_to=")
    assert response.status_code == 200
    assert b"Clear" not in response.data


def test_profile_empty_string_params_show_all_expenses(auth_client):
    """Empty string date params must behave like no filter — all expenses returned.

    Verifies the spec rule: '' or None → None before passing to get_user_expenses().
    """
    response = auth_client.get("/profile?date_from=&date_to=")
    assert response.status_code == 200
    for _, _, _, description in SEED_EXPENSES:
        assert description.encode() in response.data


# ------------------------------------------------------------------ #
# DoD 8: Summary stats unaffected by filter                            #
# ------------------------------------------------------------------ #

def test_profile_summary_total_amount_unaffected_by_date_filter(auth_client):
    """Summary total amount must reflect the full expense history, not the active filter.

    Seeded total: 100 + 200 + 300 + 400 + 500 = 1500.00.
    The narrow filter (2026-06-05 only) matches only 300.00 ('Mid range').
    If the summary were filtered, the page would show 300 — not 1500.
    """
    response = auth_client.get("/profile?date_from=2026-06-05&date_to=2026-06-05")
    assert response.status_code == 200
    # 300.00 is the only filtered expense amount — it must NOT replace the summary total.
    # 1500 (or 1,500) must appear, proving the summary is drawn from full history.
    assert b"1500" in response.data or b"1,500" in response.data


def test_profile_summary_present_on_filtered_page(auth_client):
    """The summary stats section must always be present, even when the expense list is empty."""
    response = auth_client.get("/profile?date_from=2030-01-01&date_to=2030-12-31")
    assert response.status_code == 200
    # The page must still render without error; summary block is always shown.
    # Presence of the total amount for full history (1500) confirms summary is intact.
    assert b"1500" in response.data or b"1,500" in response.data


# ------------------------------------------------------------------ #
# Filter form structural requirements (spec rules)                     #
# ------------------------------------------------------------------ #

def test_profile_filter_form_uses_get_method(auth_client):
    """The filter form must use method='get' so results are bookmarkable.

    Spec: 'The filter is submitted as a GET query string so results are
    bookmarkable and the browser Back button works correctly.'
    """
    response = auth_client.get("/profile")
    assert response.status_code == 200
    assert b'method="get"' in response.data or b"method='get'" in response.data


def test_profile_filter_form_action_points_to_profile(auth_client):
    """The filter form action must point to the /profile URL (via url_for)."""
    response = auth_client.get("/profile")
    assert response.status_code == 200
    assert b'action="/profile"' in response.data
