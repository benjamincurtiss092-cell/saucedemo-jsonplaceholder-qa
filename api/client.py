import requests

from config.settings import settings


class JsonPlaceholderClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or settings.API_BASE_URL
        self.session = requests.Session()

    def _url(self, path):
        return f"{self.base_url}{path}"

    def get(self, path, params=None):
        return self.session.get(self._url(path), params=params)

    def post(self, path, json=None):
        return self.session.post(self._url(path), json=json)

    def put(self, path, json=None):
        return self.session.put(self._url(path), json=json)

    def patch(self, path, json=None):
        return self.session.patch(self._url(path), json=json)

    def delete(self, path):
        return self.session.delete(self._url(path))

    # Convenience wrappers for the resources under test

    def get_posts(self, params=None):
        return self.get("/posts", params=params)

    def get_post(self, post_id):
        return self.get(f"/posts/{post_id}")

    def create_post(self, title, body, user_id):
        return self.post("/posts", json={"title": title, "body": body, "userId": user_id})

    def update_post(self, post_id, payload):
        return self.put(f"/posts/{post_id}", json=payload)

    def patch_post(self, post_id, payload):
        return self.patch(f"/posts/{post_id}", json=payload)

    def delete_post(self, post_id):
        return self.delete(f"/posts/{post_id}")

    def get_comments_for_post(self, post_id):
        return self.get(f"/posts/{post_id}/comments")

    def get_users(self):
        return self.get("/users")

    def get_user(self, user_id):
        return self.get(f"/users/{user_id}")
