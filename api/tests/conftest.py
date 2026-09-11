import pytest

from api.client import JsonPlaceholderClient


@pytest.fixture(scope="session")
def api_client():
    return JsonPlaceholderClient()
