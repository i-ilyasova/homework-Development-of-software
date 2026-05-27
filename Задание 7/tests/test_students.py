import pytest


class TestGetStudents:
    def test_get_students_returns_empty_list(self, client, auth_headers):
        response = client.get("/students/", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_get_students_returns_created_students(self, client, auth_headers):
        client.post("/students/", json={"last_name": "Иванов", "first_name": "Иван"}, headers=auth_headers)
        client.post("/students/", json={"last_name": "Петров", "first_name": "Петр"}, headers=auth_headers)
        response = client.get("/students/", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_students_no_auth(self, client):
        response = client.get("/students/")
        assert response.status_code == 403

    def test_get_students_invalid_token(self, client):
        response = client.get("/students/", headers={"Authorization": "Bearer invalid.token.here"})
        assert response.status_code == 401

    def test_readonly_can_get_students(self, client, readonly_headers):
        response = client.get("/students/", headers=readonly_headers)
        assert response.status_code == 200


class TestCreateStudent:
    def test_create_student_success(self, client, auth_headers):
        response = client.post(
            "/students/",
            json={"last_name": "Сидоров", "first_name": "Сидор"},
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["last_name"] == "Сидоров"
        assert data["first_name"] == "Сидор"
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_created_student_appears_in_list(self, client, auth_headers):
        client.post("/students/", json={"last_name": "Козлов", "first_name": "Козьма"}, headers=auth_headers)
        students = client.get("/students/", headers=auth_headers).json()
        last_names = [s["last_name"] for s in students]
        assert "Козлов" in last_names

    def test_create_student_readonly_forbidden(self, client, readonly_headers):
        response = client.post(
            "/students/",
            json={"last_name": "Нельзя", "first_name": "Добавить"},
            headers=readonly_headers,
        )
        assert response.status_code == 403
        assert "Read-only" in response.json()["detail"]

    def test_create_student_no_auth(self, client):
        response = client.post("/students/", json={"last_name": "Без", "first_name": "Токена"})
        assert response.status_code == 403

    def test_create_student_missing_field(self, client, auth_headers):
        response = client.post("/students/", json={"last_name": "Без"}, headers=auth_headers)
        assert response.status_code == 422


class TestGetStudentById:
    def test_get_student_by_id_success(self, client, auth_headers):
        created = client.post(
            "/students/",
            json={"last_name": "Попов", "first_name": "Поп"},
            headers=auth_headers,
        ).json()
        response = client.get(f"/students/{created['id']}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["last_name"] == "Попов"
        assert response.json()["id"] == created["id"]

    def test_get_student_not_found(self, client, auth_headers):
        response = client.get("/students/99999", headers=auth_headers)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_student_no_auth(self, client):
        response = client.get("/students/1")
        assert response.status_code == 403
