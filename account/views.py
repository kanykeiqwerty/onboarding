from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.pagination import PageNumberPagination

from django.contrib.auth import get_user_model
from . import serializers


class StandartResultsPagination(PageNumberPagination):
    page_size=5
    page_size_query_param='page'
    max_page_size=1000

User = get_user_model()


class RegistrationView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer
    

    def post(self, request):
        serializer = self.get_serializer(data=request.data)  
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(
                {"message": "User registered successfully", "user_id": user.id},
                status=status.HTTP_201_CREATED
            )



class LoginApiView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer


class LogoutApiView(GenericAPIView):
    serializer_class = serializers.LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully loged out', status=204)



# class ForgotPasswordView(APIView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request):
#         serializer = serializers.ForgotPasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         try:
#             user = User.objects.get(email=serializer.data.get('email'))
#             user.create_activation_code()
#             user.save()
#             send_reset_password(user)
#             return Response('Check your mail!', status=200)
#         except User.DoesNotExist:
#             return Response('User with this email does not exist!', status=400)


# class RestorePasswordView(APIView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request):
#         serializer = serializers.RestorePasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('Password changed successfully!', status=200)