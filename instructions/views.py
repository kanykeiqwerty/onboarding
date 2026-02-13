from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Instruction
from .serializers import InstructionSerializer


class InstructionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для инструкций.

    GET /api/v1/instructions/ - список активных инструкций
    GET /api/v1/instructions/{id}/ - детали инструкции
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InstructionSerializer

    def get_queryset(self):
        return Instruction.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        """Возвращаем первую активную инструкцию (основная инструкция платформы)"""
        instruction = self.get_queryset().first()
        if instruction:
            serializer = self.get_serializer(instruction)
            return Response(serializer.data)
        return Response({
            'message': 'Инструкция не найдена'
        }, status=404)

