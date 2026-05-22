import pytest
from unittest.mock import MagicMock, patch
from django.test import RequestFactory
from django_query_watch.middleware import QueryWatchMiddleware


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def middleware():
    get_response = MagicMock(return_value=MagicMock(status_code=200))
    return QueryWatchMiddleware(get_response)


def test_middleware_returns_response(factory, middleware):
    request = factory.get("/api/test/")
    response = middleware(request)
    assert response.status_code == 200


def test_middleware_disabled(factory):
    get_response = MagicMock(return_value=MagicMock(status_code=200))
    mw = QueryWatchMiddleware(get_response)
    with patch("django_query_watch.middleware.is_enabled", return_value=False):
        request = factory.get("/api/test/")
        response = mw(request)
        assert response.status_code == 200


def test_middleware_calls_get_response(factory, middleware):
    request = factory.get("/api/products/")
    middleware(request)
    middleware.get_response.assert_called_once_with(request)
