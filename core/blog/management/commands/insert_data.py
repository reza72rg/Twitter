from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, Profile, Follow
from blog.models import Category, Post, Like, DisLike

from comment.models import Comment


class Command(BaseCommand):
    help = "Insert dump data into User, Profile, Category, Post, Like, DisLike, and Comment models"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        # Create users and profiles
        users = []
        for _ in range(5):
            username = self.fake.user_name()
            email = self.fake.email()
            password = "123456789ab"

            user = User.objects.create_user(username=username, email=email, password=password)
            profile, created = Profile.objects.get_or_create(user=user)
            profile.first_name = self.fake.first_name()
            profile.last_name = self.fake.last_name()
            profile.description = self.fake.paragraph(nb_sentences=5)
            profile.save()

            users.append(profile)
            self.stdout.write(self.style.SUCCESS(f"Successfully created user with username: {username}"))

        # Create categories
        categories = [Category.objects.create(name=self.fake.word()) for _ in range(5)]

        # Create posts
        posts = []
        for _ in range(5):
            category = self.fake.random_element(elements=categories)
            profile = self.fake.random_element(elements=users)
            post = Post.objects.create(
                author=profile,
                content=self.fake.paragraph(nb_sentences=5),
                category=category
            )
            posts.append(post)

        self.stdout.write(self.style.SUCCESS('Successfully created 5 posts with random data.'))

        # Create likes, dislikes, and comments
        for _ in range(5):
            profile = self.fake.random_element(elements=users)
            profile_follow = self.fake.random_element(elements=users)
            post = self.fake.random_element(elements=posts)

            # Create like
            Like.objects.create(
                user=profile,
                post=post
            )

            # Create dislike
            DisLike.objects.create(
                user=profile,
                post=post
            )

            # Create comment
            Comment.objects.create(
                author=profile,
                post=post,
                content=self.fake.paragraph(nb_sentences=1)
            )
            # Create Follow
            Follow.objects.create(
                user=profile,
                follow_user=profile_follow,
            )

        self.stdout.write(self.style.SUCCESS('Successfully created likes, dislikes, Follow, and comments.'))
