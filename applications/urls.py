from django.urls import path
from .views import (
    ApplicationCreateView,
    ApplicationListView,
    ApplicationUpdateView,
    ApplicationDeleteView
)

urlpatterns = [
    path('projects/<int:project_pk>/apply/', ApplicationCreateView.as_view(), name='application-create'),
    path('projects/<int:project_pk>/applications/', ApplicationListView.as_view(), name='application-list'),
    path('applications/<int:pk>/', ApplicationUpdateView.as_view(), name='application-update'),
    path('applications/<int:pk>/cancel/', ApplicationDeleteView.as_view(), name='application-delete'),
]