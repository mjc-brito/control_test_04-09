import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.redis_queue import clear_queue, add_to_queue

User = get_user_model()

@pytest.mark.django_db
def test_api_command_permitido_so_para_primeiro(client, monkeypatch):
    clear_queue()
    u1 = User.objects.create_user("u1", password="x", student_number="S1")
    u2 = User.objects.create_user("u2", password="x", student_number="S2")
    # u1 é o primeiro
    add_to_queue("u1"); add_to_queue("u2")

    # simula Celery executar imediatamente
    from core import tasks
    monkeypatch.setattr(tasks, "send_command_task", type("T", (), {"delay": staticmethod(lambda cmd: type("R", (), {"id":"fake"})())}))
    client.login(username="u1", password="x")
    r = client.post(reverse("api-command"), data={"cmd": "PING"}, content_type="application/json")
    assert r.status_code == 200

    client.logout(); client.login(username="u2", password="x")
    r = client.post(reverse("api-command"), data={"cmd": "PING"}, content_type="application/json")
    assert r.status_code == 403
