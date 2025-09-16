import pytest
import fakeredis
import core.redis_queue as redis_queue

@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    """Mocka o Redis em todos os testes automaticamente."""
    fake = fakeredis.FakeRedis(decode_responses=True)

    monkeypatch.setattr(redis_queue, "r", fake)
    yield