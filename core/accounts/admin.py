from django.contrib import admin
from accounts.models import  Profile, Follow



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return ["user", "first_name","last_name","image","descriptions","active"]

    def get_list_display(self, request):
        return ["user","active" ]

    def get_search_fields(self, request):
        return ["user","active" ]

    def get_list_filter(self, request, filters=None):
        return ["user","active"]
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return ["user", "follow_user"]

    def get_list_display(self, request):
        return ["user","follow_user" ]

    def get_search_fields(self, request):
        return ["user","follow_user" ]

    def get_list_filter(self, request, filters=None):
        return ["user","follow_user"]
