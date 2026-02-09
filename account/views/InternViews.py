from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth import get_user_model
from account.serializers import UserSerializers
from account.permission import IsAdmin, IsSuperAdmin


class StandartResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


User = get_user_model()


class InternCreateView(GenericAPIView):
    """
    Создание стажера (админы и суперадмин)
    """
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializers.InternCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            intern = serializer.save()
            return Response(
                {
                    "message": "Intern created successfully. Check your email for details",
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
    serializer_class = UserSerializers.UserSerializer
    pagination_class = StandartResultsPagination

    def get_queryset(self):
        # Возвращаем только обычных пользователей (не staff и не superuser)
        return User.objects.filter(is_staff=False, is_superuser=False).order_by('-date_joined')


class InternDetailView(RetrieveUpdateDestroyAPIView):
    """
    Просмотр, редактирование и удаление стажера (админы и суперадмин)
    """
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializers.UserSerializer
    queryset = User.objects.filter(is_staff=False, is_superuser=False)
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserSerializers.UserUpdateSerializer
        return UserSerializers.UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Intern deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


class MyProfileView(RetrieveUpdateAPIView):
    """
    Просмотр и обновление своего профиля (стажёр / админ / суперадмин)
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializers.UserSelfSerializer

    def get_object(self):
        return self.request.user