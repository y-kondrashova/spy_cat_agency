from django.urls import path
from .views import (
    SpyCatListCreateView,
    SpyCatDetailView,
    TargetViewSet
)

urlpatterns = [
    path("cats/", SpyCatListCreateView.as_view(), name="spycat-list"),
    path("cats/<int:pk>/", SpyCatDetailView.as_view(), name="spycat-detail"),
    path(
        "missions/<int:mission_id>/targets/",
        TargetViewSet.as_view({"get": "list", "post": "create"}),
        name="target-list"
    ),
    path(
        "missions/<int:mission_id>/targets/<int:pk>/",
        TargetViewSet.as_view({"get": "retrieve", "put": "update"}),
        name='target-detail'
    ),
    path(
        "missions/<int:mission_id>/targets/<int:pk>/mark-complete/",
        TargetViewSet.as_view({"patch": "mark_complete"}),
        name="target-complete"
    ),
]
