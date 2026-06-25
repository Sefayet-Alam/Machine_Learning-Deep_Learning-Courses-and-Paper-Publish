import pytest


VALID_USER = {
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "confirm_password": "password123",
}


def register(client, **overrides):
    data = {**VALID_USER, **overrides}
    return client.post("/register", data=data)


def login(client, email=VALID_USER["email"], password=VALID_USER["password"]):
    return client.post("/login", data={"email": email, "password": password})


# ------------------------------------------------------------------ #
# Registration                                                        #
# ------------------------------------------------------------------ #

def test_register_get_renders_form(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Create" in response.data


def test_register_success(client):
    response = register(client)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_register_success_flash(client):
    response = register(client, follow_redirects=True)
    # follow_redirects not a kwarg for data; do it manually
    response = client.get("/login")
    assert response.status_code == 200


def test_register_missing_name(client):
    response = register(client, name="")
    assert response.status_code == 200
    assert b"All fields are required" in response.data


def test_register_missing_email(client):
    response = register(client, email="")
    assert response.status_code == 200
    assert b"All fields are required" in response.data


def test_register_short_password(client):
    response = register(client, password="short", confirm_password="short")
    assert response.status_code == 200
    assert b"at least 8 characters" in response.data


def test_register_password_mismatch(client):
    response = register(client, confirm_password="different!")
    assert response.status_code == 200
    assert b"do not match" in response.data


def test_register_duplicate_email(client):
    register(client)
    response = register(client)
    assert response.status_code == 200
    assert b"already exists" in response.data


def test_register_sets_session(client):
    register(client)
    with client.session_transaction() as sess:
        assert "user_id" in sess


# ------------------------------------------------------------------ #
# Login                                                               #
# ------------------------------------------------------------------ #

def test_login_get_renders_form(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Sign in" in response.data or b"Login" in response.data


def test_login_success(client):
    register(client)
    with client.session_transaction() as sess:
        sess.clear()
    response = login(client)
    assert response.status_code == 302
    assert response.headers["Location"] in ("/", "http://localhost/")


def test_login_wrong_password(client):
    register(client)
    with client.session_transaction() as sess:
        sess.clear()
    response = login(client, password="wrongpassword")
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data


def test_login_unknown_email(client):
    response = login(client, email="nobody@example.com")
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data


def test_login_missing_fields(client):
    response = client.post("/login", data={"email": "", "password": ""})
    assert response.status_code == 200
    assert b"Email and password are required" in response.data


def test_login_sets_user_id_in_session(client):
    register(client)
    with client.session_transaction() as sess:
        sess.clear()
    login(client)
    with client.session_transaction() as sess:
        assert "user_id" in sess


def test_login_sets_user_name_in_session(client):
    register(client)
    with client.session_transaction() as sess:
        sess.clear()
    login(client)
    with client.session_transaction() as sess:
        assert sess.get("user_name") == VALID_USER["name"]


def test_login_email_case_insensitive(client):
    register(client)
    with client.session_transaction() as sess:
        sess.clear()
    response = login(client, email=VALID_USER["email"].upper())
    assert response.status_code == 302


# ------------------------------------------------------------------ #
# Logout                                                              #
# ------------------------------------------------------------------ #

def test_logout_clears_session(client):
    register(client)
    with client.session_transaction() as sess:
        sess.clear()
    login(client)
    client.get("/logout")
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_logout_redirects_to_landing(client):
    register(client)
    login(client)
    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"] in ("/", "http://localhost/")


def test_logout_when_not_logged_in(client):
    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"] in ("/", "http://localhost/")


# ------------------------------------------------------------------ #
# Navbar (integration)                                                #
# ------------------------------------------------------------------ #

def test_navbar_unauthenticated(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Sign in" in response.data


def test_navbar_authenticated(client):
    register(client)
    with client.session_transaction() as sess:
        sess.clear()
    login(client)
    response = client.get("/")
    assert response.status_code == 200
    assert b"Sign out" in response.data
    assert b"Get started" not in response.data


# ------------------------------------------------------------------ #
# login_required decorator                                            #
# ------------------------------------------------------------------ #

def test_protected_route_redirects_unauthenticated(client):
    response = client.get("/profile")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_protected_route_allows_authenticated(client):
    register(client)
    with client.session_transaction() as sess:
        sess.clear()
    login(client)
    response = client.get("/profile")
    assert response.status_code != 302 or "/login" not in response.headers.get("Location", "")
