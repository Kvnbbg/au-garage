from datetime import datetime

from config import DEFAULT_MAINTENANCE_START_DATE, load_config


def test_load_config_parses_maintenance_date(monkeypatch):
    monkeypatch.setenv("MAINTENANCE_START_DATE", "2025-05-01 10:30:00")
    monkeypatch.setenv("ADMINS", "admin@example.com")
    config, warnings = load_config("development", load_env=False)
    assert config.maintenance_start_date == datetime(2025, 5, 1, 10, 30, 0)
    assert warnings == []


def test_load_config_invalid_date_falls_back(monkeypatch):
    monkeypatch.setenv("MAINTENANCE_START_DATE", "not-a-date")
    monkeypatch.setenv("ADMINS", "admin@example.com")
    config, warnings = load_config("development", load_env=False)
    assert config.maintenance_start_date == DEFAULT_MAINTENANCE_START_DATE
    assert warnings
