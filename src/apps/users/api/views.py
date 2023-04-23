from auths.api.permissions import IsVerified
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response

from .serializers import UserSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = get_user_model().objects.all()
#     serializer_class = UserSerializer

#     def get_permissions(self):
#         if self.action == "list":
#             permission_classes = [IsVerified]
#         else:
#             permission_classes = self.permission_classes
#         return [permission() for permission in permission_classes]


class ListUsersView(viewsets.ViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsVerified]

    def list(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.queryset, many=True).data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)
