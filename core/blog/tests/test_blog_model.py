from django.test import TestCase
from ..models import Post, Category, Like, DisLike
from accounts.models import User, Profile


class TestPostModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_model", password="a/@1234567"
        )
        self.profile = Profile.objects.get(user=self.user)
        self.profile.first_name = ("test_first_name",)
        self.profile.last_name = ("test_last_name",)
        self.profile.descriptions = ("test description",)
        self.profile.is_verified = True
        self.profile.save()

    def test_create_post_with_valid_data(self):
        category_obj = Category.objects.create(name="hello")
        post = Post.objects.create(
            author=self.profile,
            content="test",
            archive=True,
            category=category_obj,
        )
        self.assertTrue(Post.objects.filter(pk=post.id).exists())
        self.assertEquals(post.content, "test")


class TestLikeModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_model", password="a/@1234567"
        )
        self.profile = Profile.objects.get(user=self.user)
        self.profile.first_name = ("test_first_name",)
        self.profile.last_name = ("test_last_name",)
        self.profile.descriptions = ("test description",)
        self.profile.is_verified = True
        self.profile.save()
        category_obj = Category.objects.create(name="hello")
        self.post = Post.objects.create(
            author=self.profile,
            content="test",
            archive=True,
            category=category_obj,
        )

    def test_create_like_with_valid_data(self):
        like = Like.objects.create(
            user=self.profile,
            post=self.post,
        )
        self.assertTrue(Like.objects.filter(pk=like.id).exists())
        self.assertEquals(like.post.content, "test")

    def test_create_dislike_with_valid_data(self):
        dislike = DisLike.objects.create(
            user=self.profile,
            post=self.post,
        )
        self.assertTrue(DisLike.objects.filter(pk=dislike.id).exists())
        self.assertEquals(dislike.post.content, "test")
