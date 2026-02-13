from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from account.permission import IsAdmin
from .models import Feedback
from .serializers import FeedbackSerializer, FeedbackAdminSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    ViewSet для обратной связи.

    POST /api/v1/feedback/ - отправить обратную связь (все авторизованные)
    GET /api/v1/feedback/ - список всех обращений (только админы)
    PATCH /api/v1/feedback/{id}/ - обновить статус/комментарий (только админы)
    """
    queryset = Feedback.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsAdmin()]

    def get_serializer_class(self):
        if self.action == 'create':
            return FeedbackSerializer
        return FeedbackAdminSerializer

    def create(self, request, *args, **kwargs):
        """Создание обратной связи"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Ваше обращение принято. Спасибо за обратную связь!'},
            status=status.HTTP_201_CREATED
        )

