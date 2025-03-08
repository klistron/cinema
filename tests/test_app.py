from types import NoneType
from flask import Flask, url_for
from flask.testing import FlaskClient
import pytest
from webapp import create_app
from webapp.db import db
from webapp.user.models import User

@pytest.fixture
def app():
    app = create_app("config_test.py")
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app: Flask):
    return app.test_client()


@pytest.fixture
def user():
    user = User(email='test@example.com', username='testuser', password='password')
    db.session.add(user)
    db.session.commit()
    return user

def test_index(client: Flask):
    response = client.get("/")
    assert response.status_code == 200
    assert b"LearnPython-Cinema" in response.data


def test_register(client: Flask):
    assert client.get("/user/register").status_code == 200
    response = client.post(
        "/user/process-registration",
        data={
            "first_name": "Толя",
            "last_name": "Петров",
            "middle_name": "Петрович",
            "username": "kolay",
            "password": "12345",
            "phone": "12345",
            "email": "kolay@mail.ex",
            "submit": True,
        },
    )
    assert response.status_code == 302
    
    with client.application.app_context():
        user = User.query.filter_by(username='kolay').first()
        assert user is not None

def test_login_route(client: FlaskClient):

    response = client.get('/user/login')
    assert response.status_code == 200
    assert 'Войдите в свой аккаунт' in response.data.decode('utf-8')

def test_authenticated_user(client, user):
    with client:
        with client.session_transaction() as session:
            session['_user_id'] = str(user.id)  # Имитация авторизации

        # Теперь вы можете имитировать запросы как авторизованный пользователь
        response = client.get('user/login')
        assert response.status_code == 302  # Проверка перенаправления
        assert response.location == '/user/user_page'


def test_process_login_invalid_credentials(client):
    form_data = {
        'email': 'test@example.com',
        'password': 'wrongpassword'
    }
    response = client.post('/user/process-login', data=form_data)
    print(response.location)
    assert response.status_code == 302  # Проверка перенаправления
    assert response.location == '/user/login'

def test_logout_route(client, user):
    with client.session_transaction() as session:
        session['user_id'] = user.id

    response = client.get('/user/logout', follow_redirects=True)
    assert response.status_code == 200
    assert response.location is None

 
