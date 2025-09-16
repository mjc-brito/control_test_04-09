import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_has_number():
    u = User.objects.create_user(username='mat', password='x', student_number='12345')
    assert u.student_number == '12345'