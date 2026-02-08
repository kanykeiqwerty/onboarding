from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.pagination import PageNumberPagination

from django.contrib.auth import get_user_model
from account.serializers import AuthorizationSerializers, UserSerializers, AdminSerielizers
from account.permission import IsAdmin, IsSuperAdmin


class StandartResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


User = get_user_model()


class AdminCreateView(GenericAPIView):
    """
    Создание админа (только суперадмин)
    """
    permission_classes = (IsSuperAdmin,)
    serializer_class = AdminSerielizers.AdminCreateSerializer

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
    serializer_class = UserSerializers.UserSerializer
    pagination_class = StandartResultsPagination

    def get_queryset(self):
        # Возвращаем только пользователей со статусом staff (админы)
        return User.objects.filter(is_staff=True, is_superuser=False).order_by('-date_joined')


class AdminDetailView(RetrieveUpdateDestroyAPIView):
    """
    Просмотр, редактирование и удаление админа (только суперадмин)
    """
    permission_classes = (IsSuperAdmin,)
    serializer_class = UserSerializers.UserSerializer
    queryset = User.objects.filter(is_staff=True, is_superuser=False)
    lookup_field = 'pk'

    def get_serializer_class(self):
        if getattr(self, 'swagger_fake_view', False):
            return UserSerializers.UserSerializer
        if self.request.method in ['PUT', 'PATCH']:
            return UserSerializers.UserUpdateSerializer
        return UserSerializers.UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Admin deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )