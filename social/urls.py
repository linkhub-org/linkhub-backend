from django.urls import path
from .views import (
    FollowView,
    FollowerListView,
    FollowingListView,
    SavedProjectView,
    SavedProjectListView,
)

urlpatterns = [
    path('users/<int:pk>/follow/', FollowView.as_view(), name='user-follow'),
    path('users/<int:pk>/followers/', FollowerListView.as_view(), name='user-followers'),
    path('users/<int:pk>/following/', FollowingListView.as_view(), name='user-following'),
    path('projects/<int:pk>/save/', SavedProjectView.as_view(), name='project-save'),
    path('users/me/saved-projects/', SavedProjectListView.as_view(), name='saved-projects'),
]