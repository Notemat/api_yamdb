from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    ReviewViewSet,
    CategoryListCreateAPIView,
    CategoryDestroyAPIView,
    CommentViewSet
    GenreListCreateAPIView,
    GenreDestroyAPIView,
    TitleViewSet
)

router = DefaultRouter()
router.register(
    r'/titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(r'titles', TitleViewSet)

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view()),
    path('categories/<slug:slug>/', CategoryDestroyAPIView.as_view()),
    path('genres/', GenreListCreateAPIView.as_view()),
    path('genres/<slug:slug>/', GenreDestroyAPIView.as_view()),
    path('', include(router.urls)),
]
