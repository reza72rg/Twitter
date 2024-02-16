from django.contrib import admin
from twitter.models import Post, Like, DisLike, Comment
# Register your models here.



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return ["content", "author","archive"]

    def get_list_display(self, request):
        return ["content", "author","archive"]

    def get_search_fields(self, request):
        return ["author","archive" ]

    def get_list_filter(self, request, filters=None):
        return ["author","archive" ]



@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return ["post", "user"]

    def get_list_display(self, request):
        return ["user","post" ]

    def get_search_fields(self, request):
        return ["user","post" ]

    def get_list_filter(self, request, filters=None):
        return ["user","post" ]
@admin.register(DisLike)
class DisLikeAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return ["post", "user"]

    def get_list_display(self, request):
        return ["user","post" ]

    def get_search_fields(self, request):
        return ["user","post" ]

    def get_list_filter(self, request, filters=None):
        return ["user","post" ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return ["post", "author","content","approach"]

    def get_list_display(self, request):
        return ["post","author","approach" ]

    def get_search_fields(self, request):
        return ["post","author","approach" ]

    def get_list_filter(self, request, filters=None):
        return ["post","author" ,"approach"]
