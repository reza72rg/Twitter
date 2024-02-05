from django.urls import path, include
from accounts.views import CustomLoginView, RegisterPageView, CustomLogoutView, LogoutSuccessView
# Set the app name for namespacing
app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    # Logout view
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('logout/success/', LogoutSuccessView.as_view(), name='logout_success'),
    # Register view
    path("register/", RegisterPageView.as_view(), name="register"),

]