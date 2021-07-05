from django.urls import path
from rest_auth.views import LoginView, PasswordChangeView, LogoutView

from . import views


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change-password/', PasswordChangeView.as_view()),
    path('signup/', views.SignUpUserView.as_view()),
    path('update/', views.UserUpdateView.as_view()),
    path('profile/', views.UserPrivateView.as_view()),
    path('<str:username>/profile/', views.UserProfileView.as_view()),
    path('producers/', views.ProducerList.as_view()),
    path('info/', views.AddChangeInfo.as_view()),
]
