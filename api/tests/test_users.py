import jsonschema
import pytest

from api.schemas import USER_SCHEMA


@pytest.mark.api
@pytest.mark.smoke
def test_get_all_users_returns_200_and_list(api_client):
    response = api_client.get_users()

    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) == 10


@pytest.mark.api
@pytest.mark.smoke
def test_get_single_user_matches_schema(api_client):
    response = api_client.get_user(1)

    assert response.status_code == 200
    body = response.json()
    jsonschema.validate(instance=body, schema=USER_SCHEMA)
    assert body["id"] == 1


@pytest.mark.api
@pytest.mark.regression
def test_get_nonexistent_user_returns_404(api_client):
    response = api_client.get_user(99999)

    assert response.status_code == 404


@pytest.mark.api
@pytest.mark.regression
def test_all_users_have_unique_emails(api_client):
    response = api_client.get_users()
    users = response.json()

    emails = [user["email"] for user in users]
    assert len(emails) == len(set(emails))
