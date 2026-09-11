import jsonschema
import pytest

from api.schemas import POST_SCHEMA


@pytest.mark.api
@pytest.mark.smoke
def test_get_all_posts_returns_200_and_list(api_client):
    response = api_client.get_posts()

    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) == 100


@pytest.mark.api
@pytest.mark.smoke
def test_get_single_post_matches_schema(api_client):
    response = api_client.get_post(1)

    assert response.status_code == 200
    body = response.json()
    jsonschema.validate(instance=body, schema=POST_SCHEMA)
    assert body["id"] == 1


@pytest.mark.api
@pytest.mark.regression
def test_get_nonexistent_post_returns_404(api_client):
    response = api_client.get_post(99999)

    assert response.status_code == 404


@pytest.mark.api
@pytest.mark.regression
def test_get_posts_filtered_by_user_id(api_client):
    response = api_client.get_posts(params={"userId": 1})

    assert response.status_code == 200
    posts = response.json()
    assert len(posts) > 0
    assert all(post["userId"] == 1 for post in posts)


@pytest.mark.api
@pytest.mark.smoke
def test_create_post_returns_201_with_echoed_payload(api_client):
    payload = {"title": "foo", "body": "bar", "userId": 1}

    response = api_client.create_post(**{"title": "foo", "body": "bar", "user_id": 1})

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]
    assert "id" in body


@pytest.mark.api
@pytest.mark.regression
def test_update_post_with_put_replaces_fields(api_client):
    updated_payload = {"id": 1, "title": "updated title", "body": "updated body", "userId": 1}

    response = api_client.update_post(1, updated_payload)

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "updated title"
    assert body["body"] == "updated body"


@pytest.mark.api
@pytest.mark.regression
def test_patch_post_updates_only_given_fields(api_client):
    response = api_client.patch_post(1, {"title": "patched title only"})

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "patched title only"
    assert body["id"] == 1


@pytest.mark.api
@pytest.mark.regression
def test_delete_post_returns_200(api_client):
    response = api_client.delete_post(1)

    assert response.status_code == 200


@pytest.mark.api
@pytest.mark.regression
def test_get_comments_for_post_matches_post_id(api_client):
    response = api_client.get_comments_for_post(1)

    assert response.status_code == 200
    comments = response.json()
    assert len(comments) > 0
    assert all(comment["postId"] == 1 for comment in comments)
