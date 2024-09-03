from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, Profile
from blog.models import Category, Post


class Command(BaseCommand):
    help = "Insert dump data into User, Profile, Category, and Post models"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        # Create users and profiles
        for _ in range(5):
            username = self.fake.user_name()
            email = self.fake.email()
            password = "123456789ab"

            # Create a user
            user = User.objects.create_user(username=username, email=email, password=password)

            # Create a profile for the user
            profile, created = Profile.objects.get_or_create(user=user)
            profile.first_name = self.fake.first_name()
            profile.last_name = self.fake.last_name()
            profile.description = self.fake.paragraph(nb_sentences=5)
            profile.save()

            self.stdout.write(self.style.SUCCESS(f"Successfully created user with username: {username}"))

        # Create categories
        for _ in range(5):
            Category.objects.create(name=self.fake.word())

        # Get all created categories and profiles
        categories = list(Category.objects.all())
        profiles = list(Profile.objects.all())

        if not categories:
            self.stdout.write(self.style.ERROR('No categories found. Please create some categories first.'))
            return

        if not profiles:
            self.stdout.write(self.style.ERROR('No profiles found. Please create some profiles first.'))
            return

        # Create posts with random content and a random category
        for _ in range(5):
            category = self.fake.random_element(elements=categories)
            profile = self.fake.random_element(elements=profiles)
            Post.objects.create(
                author=profile,
                content=self.fake.paragraph(nb_sentences=5),
                category=category
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 5 posts with random data.'))
