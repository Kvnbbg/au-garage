from app import create_app
from app.auth.routes import is_safe_url


def test_is_safe_url_allows_relative():
    app = create_app({"TESTING": True})
    with app.test_request_context("/", base_url="http://localhost"):
        assert is_safe_url("/auth/login") is True


def test_is_safe_url_blocks_external():
    app = create_app({"TESTING": True})
    with app.test_request_context("/", base_url="http://localhost"):
        assert is_safe_url("https://evil.example.com") is False
