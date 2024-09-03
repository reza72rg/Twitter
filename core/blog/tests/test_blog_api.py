import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User, Profile, Follow
from blog.models import Category, Post, Like, DisLike

# Fixture to create a common user with verified status
@pytest.fixture
def common_user():
    user = User.objects.create_user(
        username="test", password="123456789ab", is_verified=True
    )
    return user

# Fixture to create an API client
@pytest.fixture
def common_category():
    category = Category.objects.create(name="test")
    return category

@pytest.fixture
def api_client():
    client = APIClient()
    return client


# Fixture to create common data for testing
@pytest.fixture
def common_data(common_user, common_category):
    data = {
        "author": common_user,
        "content": "test",
        "category": common_category,
    }
    return data