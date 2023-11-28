# FILEPATH: /c:/Users/ginom/repo/repo506/othello-ml/Backend/src/routes/test_login_routes.py

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy.orm import Session
from src.routes.login_routes import router
from src.models.login_model import LoginInput, GuestLoginInput
from src.utils.database_utils import get_db
from src.appconfig import app_constants

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_login():
    # Mocking the database session
    with Session() as db:
        # Mocking the login input
        login_input = LoginInput(username="gino", password="CaptainDuck")
        response = client.post(app_constants.Login.apiLoginUrl, json=login_input.dict(), headers={"db": db})
        assert response.status_code == 200
        assert "token" in response.cookies
        assert "username" in response.json()
        assert "user_privileges" in response.json()

def test_login_invalid_credentials():
    # Mocking the database session
    with Session() as db:
        # Mocking the login input
        login_input = LoginInput(username="invalid", password="invalid")
        response = client.post(app_constants.Login.apiLoginUrl, json=login_input.dict(), headers={"db": db})
        assert response.status_code == 400

def test_guest_login():
    # Mocking the guest login input
    guest_login_input = GuestLoginInput(username="guest")
    response = client.post(app_constants.Login.apiGuestLoginUrl, json=guest_login_input.dict())
    assert response.status_code == 200
    assert "token" in response.cookies
    assert "username" in response.json()
    assert "user_privileges" in response.json()

def test_guest_login_invalid_input():
    # Mocking the guest login input
    guest_login_input = GuestLoginInput(username="")
    response = client.post("/guest_login", json=guest_login_input.dict())
    assert response.status_code == 404