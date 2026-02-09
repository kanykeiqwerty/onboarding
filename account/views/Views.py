from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth import get_user_model
from account.serializers import AuthorizationSerializers, UserSerializers, AdminSerielizers
from account.permission import IsAdmin, IsSuperAdmin
from account.send_email import send_reset_password

class StandartResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


User = get_user_model()

class RegistrationView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthorizationSerializers.RegisterSerializer
    

    def post(self, request):
        serializer = self.get_serializer(data=request.data)  
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(
                {"message": "User registered successfully", "user_id": user.id},
                status=status.HTTP_201_CREATED
            )



class LoginApiView(TokenObtainPairView):
    serializer_class = AuthorizationSerializers.LoginSerializer


class LogoutApiView(GenericAPIView):
    serializer_class = AuthorizationSerializers.LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully loged out', status=204)


class ForgotPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AuthorizationSerializers.ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.data.get('email'))
            user.create_activation_code()
            user.save()
            send_reset_password(user)
            return Response('Check your mail!', status=200)
        except User.DoesNotExist:
            return Response('User with this email does not exist!', status=400)


class RestorePasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AuthorizationSerializers.RestorePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Password changed successfully!', status=200)




class CurrentUserView(APIView):
    """
    Получение информации о текущем пользователе
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = UserSerializers.UserSerializer(user)
        return Response(serializer.data)


from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView


class SuperAdminUserView(ListAPIView, RetrieveUpdateAPIView):
    """
    Общий список пользователей + смена ролей (только суперадмин)
    """
    permission_classes = (IsSuperAdmin,)
    serializer_class = AdminSerielizers.SuperAdminUserSerializer
    pagination_class = StandartResultsPagination
    queryset = User.objects.all().order_by('-date_joined')
    lookup_field = 'pk'
