from rest_framework import viewsets, permissions
from .models import Regulation
from .serializers import RegulationSerializer
from account.permission import IsAdmin, IsSuperAdmin


class RegulationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для регламентов (только чтение).

    GET /api/v1/regulations/ - список активных регламентов
    GET /api/v1/regulations/{id}/ - детали регламента
    """
    permission_classes = [IsAdmin, ]
    serializer_class = RegulationSerializer

    def get_queryset(self):
        return Regulation.objects.filter(is_active=True)

