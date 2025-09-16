import core.redis_queue as rq


def test_add_and_get_queue():
    rq.clear_queue()
    rq.add_to_queue("alice")
    rq.add_to_queue("bob")
    q = rq.get_queue()
    assert q == ["alice", "bob"]


def test_no_duplicates():
    rq.clear_queue()
    rq.add_to_queue("alice")
    rq.add_to_queue("alice")
    q = rq.get_queue()
    assert q == ["alice"]


def test_remove_from_queue():
    rq.clear_queue()
    rq.add_to_queue("alice")
    rq.add_to_queue("bob")
    rq.remove_from_queue("alice")
    q = rq.get_queue()
    assert q == ["bob"]


def test_get_first():
    rq.clear_queue()
    rq.add_to_queue("alice")
    rq.add_to_queue("bob")
    first = rq.get_first()
    assert first == "alice"


def test_clear_queue():
    rq.clear_queue()
    rq.add_to_queue("alice")
    rq.clear_queue()
    q = rq.get_queue()
    assert q == []
