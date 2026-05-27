import pytest


class TestRegister:
    def test_register_success(self, client):
        response = client.post("/auth/register", json={
            "username": "new_user",
            "email": "new@example.com",
            "password": "NewPass123",
            "role": "admin",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "new_user"
        assert data["email"] == "new@example.com"
        assert data["role"] == "admin"
        assert data["is_active"] is True
        assert "id" in data

    def test_register_readonly_role(self, client):
        response = client.post("/auth/register", json={
            "username": "reader",
            "email": "reader@example.com",
            "password": "Reader123",
            "role": "readonly",
        })
        assert response.status_code == 201
        assert response.json()["role"] == "readonly"

    def test_register_duplicate_username(self, client):
        payload = {
            "username": "dup_user",
            "email": "dup@example.com",
            "password": "DupPass123",
            "role": "admin",
        }
        client.post("/auth/register", json=payload)
        response = client.post("/auth/register", json=payload)
        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]

    def test_register_invalid_email(self, client):
        response = client.post("/auth/register", json={
            "username": "bad_email_user",
            "email": "not-an-email",
            "password": "Pass123",
            "role": "admin",
        })
        assert response.status_code == 422


class TestLogin:
    def test_login_success(self, client, registered_admin):
        response = client.post("/auth/login", json={
            "username": registered_admin["username"],
            "password": registered_admin["password"],
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 10
        assert len(data["refresh_token"]) > 10

    def test_login_wrong_password(self, client, registered_admin):
        response = client.post("/auth/login", json={
            "username": registered_admin["username"],
            "password": "WrongPass999",
        })
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        response = client.post("/auth/login", json={
            "username": "ghost_user",
            "password": "GhostPass123",
        })
        assert response.status_code == 401

    def test_login_returns_valid_token(self, client, registered_admin, auth_headers):
        response = client.get("/auth/me", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["username"] == registered_admin["username"]


class TestLogout:
    def test_logout_success(self, client, auth_headers):
        response = client.post("/auth/logout", headers=auth_headers)
        assert response.status_code == 200
        assert "Successfully logged out" in response.json()["detail"]

    def test_logout_revokes_token(self, client, admin_token, auth_headers):
        client.post("/auth/logout", headers=auth_headers)
        response = client.get("/students/", headers=auth_headers)
        assert response.status_code == 401
        assert "revoked" in response.json()["detail"].lower()

    def test_logout_without_token(self, client):
        response = client.post("/auth/logout")
        assert response.status_code == 403

    def test_double_logout_fails(self, client, auth_headers):
        client.post("/auth/logout", headers=auth_headers)
        response = client.post("/auth/logout", headers=auth_headers)
        assert response.status_code == 401
