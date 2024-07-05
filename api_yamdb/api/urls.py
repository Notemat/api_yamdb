from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    ReviewViewSet,
    CategoryListCreateAPIView,
    CategoryDestroyAPIView,
    GenreListCreateAPIView,
    GenreDestroyAPIView
)

router = DefaultRouter()
router.register(
    r'/titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view()),
    path('categories/<slug:slug>/', CategoryDestroyAPIView.as_view()),
    path('genres/', GenreListCreateAPIView.as_view()),
    path('genres/<slug:slug>/', GenreDestroyAPIView.as_view()),
]
