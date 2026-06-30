from django.urls import path
from .views import RecommendProfilesView, RecommendProjectsView

urlpatterns = [
    path(
        'projects/<int:project_id>/recommend-profiles/',
        RecommendProfilesView.as_view(),
        name='recommend-profiles'
    ),
    path(
        'users/me/recommend-projects/',
        RecommendProjectsView.as_view(),
        name='recommend-projects'
    ),
]