from django.urls import path

from .views import is_verified_view, token_obtain_view, token_refresh_view

urlpatterns = [
    path("token-obtain/", token_obtain_view, name="token_obtain"),
    path("token-refresh/", token_refresh_view, name="token_refresh"),
    path("is-verified/", is_verified_view, name="is_verified"),
]
