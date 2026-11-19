import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_settings_read_database_url_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database_url = (
        "postgresql+psycopg://umthombolwazi:local-pass@localhost:5432/"
        "umthombolwazi"
    )
    monkeypatch.setenv("UMTHOMBOLWAZI_DATABASE_URL", database_url)

    settings = Settings(_env_file=None)

    assert str(settings.database_url) == database_url
    assert settings.environment == "development"


def test_settings_require_database_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("UMTHOMBOLWAZI_DATABASE_URL", raising=False)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)
