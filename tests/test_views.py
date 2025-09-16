import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.redis_queue import clear_queue, add_to_queue

User = get_user_model()

@pytest.mark.django_db
def test_fila_adiciona_usuario(client):
    clear_queue()
    u = User.objects.create_user("u1", password="x", student_number="S1")
    client.login(username="u1", password="x")
    r = client.get(reverse("fila"))
    assert r.status_code == 200

@pytest.mark.django_db
def test_controle_so_primeiro(client):
    clear_queue()
    u1 = User.objects.create_user("u1", password="x", student_number="S1")
    u2 = User.objects.create_user("u2", password="x", student_number="S2")
    # u1 entra na fila primeiro
    client.login(username="u1", password="x")
    client.get(reverse("fila"))
    client.logout()
    # u2 entra na fila depois
    client.login(username="u2", password="x")
    client.get(reverse("fila"))
    # u2 tenta controlo => deve redirecionar
    r = client.get(reverse("controlo"))
    assert r.status_code == 302 and "/core/fila/" in r.url
