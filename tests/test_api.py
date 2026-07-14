import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def payload():
    return {
        "project_name": "DailyDevLog",
        "project_type": "backend",
        "nombre_tarea": "Test task",
        "horas": "2.5",
        "tecnologias_utilizadas": "Django",
    }


@pytest.mark.django_db
def test_list_is_public(client):
    assert client.get("/api/dailylog/").status_code == 200


@pytest.mark.django_db
def test_create_requires_auth(client, payload):
    r = client.post("/api/dailylog/", payload)
    assert r.status_code in (401, 403)


@pytest.mark.django_db
def test_create_with_jwt(client, payload):
    user = User.objects.create_user("nico", "nico@example.com", "pass-12345")
    client.force_authenticate(user)
    r = client.post("/api/dailylog/", payload)
    assert r.status_code == 201, r.content
