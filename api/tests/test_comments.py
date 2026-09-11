import jsonschema
import pytest

from api.schemas import COMMENT_SCHEMA


@pytest.mark.api
@pytest.mark.regression
def test_get_comments_by_post_id_query_param(api_client):
    response = api_client.get("/comments", params={"postId": 1})

    assert response.status_code == 200
    comments = response.json()
    assert len(comments) > 0
    for comment in comments:
        jsonschema.validate(instance=comment, schema=COMMENT_SCHEMA)
        assert comment["postId"] == 1


@pytest.mark.api
@pytest.mark.regression
def test_comment_emails_are_well_formed(api_client):
    response = api_client.get("/comments", params={"postId": 1})
    comments = response.json()

    for comment in comments:
        assert "@" in comment["email"]


@pytest.mark.api
@pytest.mark.smoke
def test_response_time_is_reasonable(api_client):
    response = api_client.get_posts()

    assert response.elapsed.total_seconds() < 3
