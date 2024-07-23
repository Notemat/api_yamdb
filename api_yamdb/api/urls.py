from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet,
                       send_confirmation_code, send_token)

v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
v1_router.register('titles', TitleViewSet)
v1_router.register('users', UserViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)

urlpatterns = [
    path('auth/', include([
        path('signup/', send_confirmation_code),
        path('token/', send_token)
    ])),
    path('', include(v1_router.urls)),
]
