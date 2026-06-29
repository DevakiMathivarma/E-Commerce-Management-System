import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import Base,get_db


# test database

SQLALCHEMY_DATABASE_URL="sqlite:///./test.db"

engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})

TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)


# override database

def override_get_db():
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db]=override_get_db

client=TestClient(app)


# create tables

Base.metadata.create_all(bind=engine)


# register success

def test_register_user():

    response=client.post("/api/v1/auth/register",json={"full_name":"Test User","email":"testuser@gmail.com","password":"Password@123"})

    assert response.status_code==201

    data=response.json()

    assert data["email"]=="testuser@gmail.com"

    assert data["role"]=="Customer"

    assert data["is_active"]==True


# duplicate email

def test_duplicate_email():

    response=client.post("/api/v1/auth/register",json={"full_name":"Test User","email":"testuser@gmail.com","password":"Password@123"})

    assert response.status_code==400

    assert response.json()["detail"]=="email already registered"

# login success

def test_login_success():

    response=client.post("/api/v1/auth/login",json={"email":"testuser@gmail.com","password":"Password@123"})

    assert response.status_code==200

    data=response.json()

    assert "access_token" in data

    assert data["token_type"]=="bearer"


# invalid email

def test_login_invalid_email():

    response=client.post("/api/v1/auth/login",json={"email":"invalid@gmail.com","password":"Password@123"})

    assert response.status_code==401

    assert response.json()["detail"]=="invalid email or password"


# invalid password

def test_login_invalid_password():

    response=client.post("/api/v1/auth/login",json={"email":"testuser@gmail.com","password":"WrongPassword"})

    assert response.status_code==401

    assert response.json()["detail"]=="invalid email or password"


# token exists

def test_token_response():

    response=client.post("/api/v1/auth/login",json={"email":"testuser@gmail.com","password":"Password@123"})

    data=response.json()

    assert isinstance(data["access_token"],str)

    assert len(data["access_token"])>0


# cleanup

@pytest.fixture(scope="session",autouse=True)
def cleanup():
    yield
    Base.metadata.drop_all(bind=engine)