import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User
from ..models import Category


# Fixtures
@pytest.fixture
def common_user():
    return User.objects.create_user(
        username="test", password="123456789ab", is_verified=True
    )


@pytest.fixture
def common_category():
    return Category.objects.create(name="test")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def common_url():
    return reverse("blog:api-v1:task-archive")


@pytest.fixture
def common_data(common_user, common_category):
    # Create a sample post data for testing
    return {
        "author": common_user.id,
        "content": "Sample post content",
        "archive": True,
        "category": common_category.id,
    }


# Test class for API tests
@pytest.mark.django_db
class TestBlogApi:
    def test_get_post_response_200_status(self, api_client, common_url):
        response = api_client.get(common_url)
        assert response.status_code == 200

    def test_create_post_response_201_status(
        self, api_client, common_url, common_data
    ):
        # Ensure user is authenticated before posting
        api_client.login(username="test", password="123456789ab")
        response = api_client.post(common_url, common_data, format="json")
        assert response.status_code == 201
