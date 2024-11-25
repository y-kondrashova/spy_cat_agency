from django.urls import path
from .views import (
    SpyCatListCreateView,
    SpyCatDetailView,
)

urlpatterns = [
    path('cats/', SpyCatListCreateView.as_view(), name='spycat-list'),
    path('cats/<int:pk>/', SpyCatDetailView.as_view(), name='spycat-detail'),

]
