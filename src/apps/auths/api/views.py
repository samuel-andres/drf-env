from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView as SJWTObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView as SJWTRefreshView

from .permissions import IsVerified
from .serializers import TokenObtainSerializer


class TokenObtainView(SJWTObtainPairView):
    serializer_class = TokenObtainSerializer


class TokenRefreshView(SJWTRefreshView):
    pass


class IsVerifiedView(APIView):
    permission_classes = [IsVerified]

    def get(self, request):
        return Response("Verified account!")


token_obtain_view = TokenObtainView.as_view()
token_refresh_view = TokenRefreshView.as_view()
is_verified_view = IsVerifiedView.as_view()
