from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http.response import HttpResponseBase
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]


@swagger_auto_schema(
    method="GET",
    responses={200: UserSerializer},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def users_me_view(request: Request) -> HttpResponseBase:
    """Get the currently authenticated user."""
    response_serializer = UserSerializer(request.user)
    return Response(response_serializer.data)


@swagger_auto_schema(
    method="POST",
    responses={204: no_body},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def users_logout_view(request: Request) -> HttpResponseBase:
    """Log the user out."""
    logout(request)
    return Response(status=204)
