from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    ReviewViewSet,
    CategoryListCreateAPIView,
    CategoryDestroyAPIView,
    CommentViewSet,
    GenreListCreateAPIView,
    GenreDestroyAPIView,
    TitleViewSet,
    send_confirmation_code,
    send_token,
    UserViewSet
)

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(r'titles', TitleViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view()),
    path('categories/<slug:slug>/', CategoryDestroyAPIView.as_view()),
    path('genres/', GenreListCreateAPIView.as_view()),
    path('genres/<slug:slug>/', GenreDestroyAPIView.as_view()),
    path('api/v1/auth/signup/', send_confirmation_code),
    path('api/v1/auth/token/', send_token),
    path('', include(router.urls)),
]
