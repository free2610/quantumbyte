from unittest.mock import patch
from app.core.security import is_admin
from app.config import settings


def test_is_admin_check():
    with patch.object(settings, "ADMIN_IDS", [111222, 333444]):
        assert is_admin(111222) is True
        assert is_admin(333444) is True
        assert is_admin(999999) is False
        assert is_admin(0) is False
