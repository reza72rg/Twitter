from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Profile
from blog.models import Post, Category


class TestBlogView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test", password="a/@1234567"
        )
        self.profile = Profile.objects.get(user=self.user)
        self.profile.first_name = ("test_first_name",)
        self.profile.last_name = ("test_last_name",)
        self.profile.descriptions = ("test description",)
        self.profile.save()

        category_obj = Category.objects.create(name="hello")
        self.post = Post.objects.create(
            author=self.profile,
            content="description",
            archive=True,
            category=category_obj,
        )

    def test_blog_index_url_successful_response(self):
        self.client.force_login(self.user)
        url = reverse("blog:home_page")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(str(response.content).find("posts"))
        self.assertTemplateUsed(response, template_name="blog/home.html")

    def test_blog_post_detail_logged_in_response(self):
        self.client.force_login(self.user)
        url = reverse("blog:details_post", kwargs={"pk": self.post.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_blog_post_detail_anonymouse_response(self):
        url = reverse("blog:details_post", kwargs={"pk": self.post.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
