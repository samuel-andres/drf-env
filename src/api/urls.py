from django.urls import include, path

urlpatterns = [path("auth/", include("auths.api.urls")), path("users/", include("users.api.urls"))]
