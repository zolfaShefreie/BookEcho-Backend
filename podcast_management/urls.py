from django.urls import path

from . import views

urlpatterns = [
    path('request/<int:pk>/podcast/', views.PodcastCreateView.as_view()),
    # path('request/<int:pk>/podcast/update/', views.PodcastUpdateView.as_view()),
    path('request/<int:pk>/podcast/set-active/', views.PodcastActiveView.as_view()),
    path('request/<int:pk>/podcast/set-score/', views.PodcastScoreView.as_view()),
]
