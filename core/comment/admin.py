from django.contrib import admin
from comment.models import Comment
# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return ["post", "author", "content", "approach"]

    def get_list_display(self, request):
        return ["post", "author", "approach"]

    def get_search_fields(self, request):
        return ["post", "author", "approach"]

    def get_list_filter(self, request, filters=None):
        return ["post", "author" , "approach"]
