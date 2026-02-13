from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import News, Employee, WelcomeBlock
from .serializers import (
    NewsSerializer, NewsListSerializer,
    EmployeeSerializer, WelcomeBlockSerializer
)


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для новостей.

    GET /api/v1/news/ - список активных новостей для слайдера
    GET /api/v1/news/{id}/ - детальная информация о новости (лайтбокс)
    """
    permission_classes = [permissions.AllowAny]  # Новости доступны всем

    def get_queryset(self):
        return News.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return NewsListSerializer
        return NewsSerializer


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для сотрудников.

    GET /api/v1/employees/ - список активных сотрудников для слайдера
    """
    permission_classes = [permissions.AllowAny]  # Сотрудники доступны всем
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return Employee.objects.filter(is_active=True)


class WelcomeBlockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для приветственного блока.

    GET /api/v1/welcome/ - активный приветственный блок
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WelcomeBlockSerializer

    def get_queryset(self):
        return WelcomeBlock.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        """Возвращаем только первый активный блок"""
        queryset = self.get_queryset().first()
        if queryset:
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)
        return Response({'detail': 'Приветственный блок не найден'}, status=404)

