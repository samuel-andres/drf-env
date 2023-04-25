from django.urls import path

from .views import ListUsersView

# router = DefaultRouter()
# router.register(r"", UserViewSet, basename="users")

# urlpatterns = [
#     path("", include(router.urls)),
# ]

urlpatterns = [
    path("", ListUsersView.as_view({"get": "list"})),
    path("<int:pk>/", ListUsersView.as_view({"get": "retrieve"})),
]
