from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.pagination import PageNumberPagination

from django.contrib.auth import get_user_model
from . import serializers
from .permission import IsAdmin, IsSuperAdmin


class StandartResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


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



class AdminCreateView(GenericAPIView):
    """
    Создание админа (только суперадмин)
    """
    permission_classes = (IsSuperAdmin,)
    serializer_class = serializers.AdminCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            admin = serializer.save()
            return Response(
                {
                    "message": "Admin created successfully",
                    "admin": {
                        "id": admin.id,
                        "email": admin.email,
                        "role": "admin"
                    }
                },
                status=status.HTTP_201_CREATED
            )


class AdminListView(ListAPIView):
    """
    Список всех админов (только суперадмин)
    """
    permission_classes = (IsSuperAdmin,)
    serializer_class = serializers.UserSerializer
    pagination_class = StandartResultsPagination

    def get_queryset(self):
        # Возвращаем только пользователей со статусом staff (админы)
        return User.objects.filter(is_staff=True, is_superuser=False).order_by('-date_joined')


class AdminDetailView(RetrieveUpdateDestroyAPIView):
    """
    Просмотр, редактирование и удаление админа (только суперадмин)
    """
    permission_classes = (IsSuperAdmin,)
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_staff=True, is_superuser=False)
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return serializers.UserUpdateSerializer
        return serializers.UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Admin deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# ============= УПРАВЛЕНИЕ СТАЖЕРАМИ (для админов и суперадмина) =============

class InternCreateView(GenericAPIView):
    """
    Создание стажера (админы и суперадмин)
    """
    permission_classes = (IsAdmin,)
    serializer_class = serializers.InternCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            intern = serializer.save()
            return Response(
                {
                    "message": "Intern created successfully",
                    "intern": {
                        "id": intern.id,
                        "email": intern.email,
                        "role": "intern"
                    }
                },
                status=status.HTTP_201_CREATED
            )


class InternListView(ListAPIView):
    """
    Список всех стажеров (админы и суперадмин)
    """
    permission_classes = (IsAdmin,)
    serializer_class = serializers.UserSerializer
    pagination_class = StandartResultsPagination

    def get_queryset(self):
        # Возвращаем только обычных пользователей (не staff и не superuser)
        return User.objects.filter(is_staff=False, is_superuser=False).order_by('-date_joined')


class InternDetailView(RetrieveUpdateDestroyAPIView):
    """
    Просмотр, редактирование и удаление стажера (админы и суперадмин)
    """
    permission_classes = (IsAdmin,)
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_staff=False, is_superuser=False)
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return serializers.UserUpdateSerializer
        return serializers.UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Intern deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# ============= ИНФОРМАЦИЯ О ТЕКУЩЕМ ПОЛЬЗОВАТЕЛЕ =============

class CurrentUserView(APIView):
    """
    Получение информации о текущем пользователе
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)
