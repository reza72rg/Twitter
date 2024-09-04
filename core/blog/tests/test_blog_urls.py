from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import (
    PostListView,
    UserCreatePostView,
    DetailsPostView,
    ArchivePostsView,
    DeletePostView,
    UpdatePostView,
    FollowersView,
    UserFollowListView,
    Aboutpage,
    FollowUserView,
    LikePostView,
    DisLikePostView,
)


class TestUrl(SimpleTestCase):

    def test_blog_index_url_resolve(self):
        url = reverse('blog:home_page')
        self.assertEquals(resolve(url).func.view_class, PostListView)

    def test_blog_post_list_url_resolve(self):
        url = reverse('blog:create-posts')
        self.assertEquals(resolve(url).func.view_class, UserCreatePostView)

    def test_blog_post_detail_url_resolve(self):
        url = reverse('blog:details_post', kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, DetailsPostView)

    def test_archive_posts_url_resolve(self):
        url = reverse('blog:archive_posts')
        self.assertEquals(resolve(url).func.view_class, ArchivePostsView)

    def test_about_page_url_resolve(self):
        url = reverse('blog:about')
        self.assertEquals(resolve(url).func.view_class, Aboutpage)

    def test_delete_post_url_resolve(self):
        url = reverse('blog:delete', kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, DeletePostView)

    def test_update_post_url_resolve(self):
        url = reverse('blog:update_post', kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, UpdatePostView)

    def test_followers_url_resolve(self):
        url = reverse('blog:user-followers', kwargs={'user_id': 1, 'letter': 'A'})
        self.assertEquals(resolve(url).func.view_class, FollowersView)

    def test_user_follow_list_url_resolve(self):
        url = reverse('blog:user-follows', kwargs={'user_id': 1})
        self.assertEquals(resolve(url).func.view_class, UserFollowListView)

    def test_follow_user_url_resolve(self):
        url = reverse('blog:follow')
        self.assertEquals(resolve(url).func.view_class, FollowUserView)

    def test_like_post_url_resolve(self):
        url = reverse('blog:like-post', kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, LikePostView)

    def test_dislike_post_url_resolve(self):
        url = reverse('blog:dislike-post', kwargs={'pk': 1})
        self.assertEquals(resolve(url).func.view_class, DisLikePostView)
