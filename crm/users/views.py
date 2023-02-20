from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


@api_view(['POST'])
def login(request):
    username = request.data['username']
    password = request.data['password']
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {'message': 'Invalid Password'},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {'message': 'User Does Not Exist'},
            status=status.HTTP_400_BAD_REQUEST,
        )
