import pytest
import tempfile
import os
from app import app as flask_app
import database.db as db_module
from database.db import init_db


@pytest.fixture(scope="function")
def app():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    db_module.DB_PATH = db_path

    flask_app.config.update({"TESTING": True, "SECRET_KEY": "test-secret"})

    with flask_app.app_context():
        init_db()

    yield flask_app

    os.unlink(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()
