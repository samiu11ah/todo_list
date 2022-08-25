import pytest
from . import create_app

app = create_app()

client = app.test_client()

def test_login_page_responds():
    response = client.get('/login', content_type='html/text')
    assert response.status_code == 200
    assert b"Nutzername" in response.data
    assert b"Passwort" in response.data

# Ensure that signup page works correctly
def test_signup_page_responds():
    response = client.get('/signup', content_type='html/text')
    assert response.status_code == 200
    assert b"Anmeldung" in response.data
    assert b"Name" in response.data
    assert b"Nutzername" in response.data
    assert b"Email" in response.data
    assert b"Passwort" in response.data

# Ensure that index page requires user login
def test_login_required_for_index_page():
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Bitte melden Sie sich an, um auf diese Seite zuzugreifen." in response.data

# Ensure that categories page requires user login
def test_categories_require_login():
    response = client.get("/categories", follow_redirects=True)
    assert response.status_code == 200
    assert b"Bitte melden Sie sich an, um auf diese Seite zuzugreifen." in response.data

# Ensure that update page requires user login
def test_update_page_requires_login():
    response = client.get("/todos/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Bitte melden Sie sich an, um auf diese Seite zuzugreifen." in response.data

# Ensure that logout requires user login
def test_logout_requires_login():
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Bitte melden Sie sich an, um auf diese Seite zuzugreifen." in response.data



# Ensure that todos show up on the main page
def test_todos_show_up_on_main_page():
    response = client.post('/login', data=dict(username="admin", password="Kingsmen786"),follow_redirects=True)
    assert b'Ihre' in response.data



