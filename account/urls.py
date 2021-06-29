from django.urls import path
from rest_auth.views import LoginView, PasswordChangeView, LogoutView

from .views import SignUpUserView


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change-password/', PasswordChangeView.as_view()),
    path('signup/', SignUpUserView),
]
