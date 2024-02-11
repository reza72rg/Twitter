from django.contrib import admin
from twitter.models import Post, Like, DisLike
# Register your models here.



admin.site.register(Post)
admin.site.register(Like)
admin.site.register(DisLike)
