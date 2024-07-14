from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreListCreateAPIView,
    GenreDestroyAPIView,
    ReviewViewSet,
    send_confirmation_code,
    send_token,
    TitleViewSet,
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
router.register('titles', TitleViewSet)
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('genres/', GenreListCreateAPIView.as_view()),
    path('genres/<slug:slug>/', GenreDestroyAPIView.as_view()),
    path('auth/signup/', send_confirmation_code),
    path('auth/token/', send_token),
    path('', include(router.urls)),
]
