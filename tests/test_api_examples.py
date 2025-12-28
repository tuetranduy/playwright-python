import pytest
import requests
from utils.api_client import APIClient
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.api
@pytest.mark.smoke
class TestAPIExamples:
    @pytest.fixture(scope="class")
    def api_client(self):
        client = APIClient(base_url="https://jsonplaceholder.typicode.com")
        yield client
        client.close()

    def test_get_user(self, api_client: APIClient):
        logger.info("Testing GET /users/1")
        response = api_client.get("/users/1")

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert data["id"] == 1
        logger.info(f"User retrieved: {data['name']}")

    def test_get_all_posts(self, api_client: APIClient):
        logger.info("Testing GET /posts")
        response = api_client.get("/posts")

        assert response.status_code == 200
        posts = response.json()
        assert isinstance(posts, list)
        assert len(posts) > 0
        logger.info(f"Retrieved {len(posts)} posts")

    def test_create_post(self, api_client: APIClient):
        logger.info("Testing POST /posts")
        payload = {"title": "Test Post", "body": "This is a test post", "userId": 1}
        response = api_client.post("/posts", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == payload["title"]
        assert data["body"] == payload["body"]
        logger.info(f"Post created with ID: {data.get('id')}")

    def test_update_post(self, api_client: APIClient):
        logger.info("Testing PUT /posts/1")
        payload = {
            "id": 1,
            "title": "Updated Title",
            "body": "Updated body",
            "userId": 1,
        }
        response = api_client.put("/posts/1", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == payload["title"]
        logger.info("Post updated successfully")

    def test_delete_post(self, api_client: APIClient):
        logger.info("Testing DELETE /posts/1")
        response = api_client.delete("/posts/1")

        assert response.status_code == 200
        logger.info("Post deleted successfully")


@pytest.mark.api
@pytest.mark.regression
class TestAPIValidation:
    @pytest.fixture(scope="class")
    def api_client(self):
        client = APIClient(base_url="https://jsonplaceholder.typicode.com")
        yield client
        client.close()

    def test_response_schema_validation(self, api_client: APIClient):
        response = api_client.get("/users/1")

        assert response.status_code == 200
        data = response.json()

        required_fields = ["id", "name", "username", "email"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

        assert isinstance(data["id"], int)
        assert isinstance(data["name"], str)
        logger.info("Schema validation passed")

    @pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
    def test_multiple_users(self, api_client: APIClient, user_id):
        response = api_client.get(f"/users/{user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        logger.info(f"User {user_id} validated successfully")
