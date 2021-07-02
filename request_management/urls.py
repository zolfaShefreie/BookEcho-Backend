from django.urls import path

from . import views

urlpatterns = [
    path('producer/<int:pk>/request/', views.RequestCreateView.as_view()),
    path('request/<int:pk>/', views.RequestViewSet.as_view({
        'patch': 'partial_update',
        'get': 'retrieve',
        'delete': 'destroy'
    })),
    path('request/<int:pk>/producer-accept/', views.RequestAcceptByProducerView.as_view()),
    path('request/<int:pk>/producer-reject/', views.RequestRejectByProducerView.as_view()),
    path('request/<int:pk>/deadline-accept/', views.RequestDeadLineAcceptView.as_view()),
    path('request/<int:pk>/deadline-reject/', views.RequestDeadLineRejectView.as_view()),
    path('applicant/requests/', views.ApplicantRequestList.as_view()),
    path('produser/requests/', views.ProducerRequestList.as_view()),
]
